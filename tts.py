import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TTS Alkitab Nyeleneh", page_icon="🧩", layout="centered")

# --- CUSTOM CSS UNTUK TAMPILAN ---
st.markdown("""
    <style>
    /* Desain Header Berwarna di Tengah */
    .main-header {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F00 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        padding: 0;
        font-size: 38px;
        font-weight: 900;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 18px;
        font-style: italic;
        opacity: 0.9;
    }
    
    /* Desain Input Kotak TTS (Satu Input tapi Renggang) */
    div[data-testid="stTextInput"] input {
        text-align: center !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        letter-spacing: 30px !important; /* Membuat huruf saling berjauhan */
        text-transform: uppercase !important;
        background-color: #F8F9FA;
        border: 3px solid #D1D5DB;
        border-radius: 12px;
        padding: 15px;
        color: #1F2937;
    }
    
    /* Desain Teks Hint */
    .hint-text {
        text-align: center;
        font-size: 32px;
        letter-spacing: 30px;
        font-weight: bold;
        color: #FF4B4B;
        margin-bottom: -15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA SOAL ---
questions = [
    {"q": "Karena tidak mau pergi ke Niniwe, Nabi Yunus akhirnya ditelan oleh ikan...", "normal": "BESAR", "lontong": "HIDUP", "reason": "Kalau ikannya udah mati, dia ngambang doang di laut, mana bisa buka mulut buat nelen orang."},
    {"q": "Saat dikejar pasukan Firaun, dengan tongkatnya Nabi Musa membelah laut...", "normal": "MERAH", "lontong": "DALAM", "reason": "Justru karena lautnya dalam makanya harus dibelah biar bisa lewat. Kalau cetek tinggal nyeker aja."},
    {"q": "Hukuman untuk Daniel karena tetap berdoa kepada Allah adalah dilempar ke dalam gua...", "normal": "SINGA", "lontong": "GELAP", "reason": "Gua zaman dulu ditutup batu atasnya, ya pasti gelap gulita. Kalau terang banyak lampu itu minimarket."},
    {"q": "Simson akhirnya kehilangan semua kekuatannya setelah rambutnya di...", "normal": "POTONG", "lontong": "PENDEK", "reason": "Setelah dicukur ya rambutnya jadi pendek. Coba kalau potong ujungnya doang dikit, kekuatannya nggak hilang."},
    {"q": "Karena badannya pendek, Zakheus memanjat pohon ara supaya bisa melihat...", "normal": "YESUS", "lontong": "JELAS", "reason": "Kalau lihat dari bawah ketutupan kepala orang, buram! Makanya manjat supaya bisa melihat dengan jelas."},
    {"q": "Saat berjalan di atas air menuju Yesus lalu melihat tiupan angin sakal, Petrus menjadi...", "normal": "TAKUT", "lontong": "BASAH", "reason": "Karena mulai tenggelam ke dalam air, ya otomatis baju sampai sepatunya basah kuyup!"},
    {"q": "Tindakan Yudas Iskariot rela menyerahkan Yesus kepada imam-imam kepala demi mendapatkan 30 keping...", "normal": "PERAK", "lontong": "SALAH", "reason": "Ya jelas tindakannya salah! Masa mengkhianati Guru sendiri cuma demi materi."},
    {"q": "Meskipun diuji dengan kehilangan seluruh hartanya dan anak-anaknya meninggal, Ayub tetap...", "normal": "SETIA", "lontong": "HIDUP", "reason": "Yang mati anak dan ternaknya. Ayubnya sendiri kan saat itu masih hidup."},
    {"q": "Esau rela menjual hak kesulungannya kepada Yakub hanya demi semangkuk sayur kacang...", "normal": "MERAH", "lontong": "PANAS", "reason": "Kuahnya pasti masih panas dan ngebul. Kalau udah dingin dari kemarin, Esau juga mikir dua kali."},
    {"q": "Nabi Elia sendirian menantang 450 nabi palsu dewa Baal di atas Gunung...", "normal": "KARMEL", "lontong": "BERANI", "reason": "Satu lawan empat ratus lima puluh orang, ya jelas Elia itu berani! Kalau penakut mending ngumpet."},
    {"q": "Sebelum merayakan Paskah, Yesus memberi teladan kerendahan hati dengan membasuh kaki...", "normal": "MURID", "lontong": "KOTOR", "reason": "Zaman dulu jalanan berdebu dan cuma pakai sandal, kakinya pasti kotor. Kalau bersih ngapain dibasuh lagi."},
    {"q": "Martir pertama di gereja mula-mula yang mati syahid karena dilempari batu bertubi-tubi oleh orang Yahudi...", "normal": "STEFANUS", "lontong": "BERDARAH", "reason": "Dilempar batu sekepalan tangan beramai-ramai, ya pasti badannya berdarah semua."},
    {"q": "Untuk bisa masuk ke tanah Kanaan, bangsa Israel yang dipimpin Yosua berjalan menyeberangi sungai...", "normal": "YORDAN", "lontong": "KERING", "reason": "Kalau airnya lagi deres mana berani bawa anak-anak nyeberang. Nunggu air berhenti dan tanahnya kering baru nyeberang!"}
]

# --- INISIALISASI STATE TERSIMPAN ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [""] * len(questions)
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = [False] * len(questions)
if 'hint_shown' not in st.session_state:
    st.session_state.hint_shown = [False] * len(questions)
if 'hint_indices' not in st.session_state:
    st.session_state.hint_indices = [-1] * len(questions)

def calculate_hint(normal, lontong):
    matches = [i for i in range(len(lontong)) if i < len(normal) and normal[i] == lontong[i]]
    if matches:
        return matches[0]
    return random.randint(1, len(lontong) - 1) if len(lontong) > 1 else 0

# --- HEADER UTAMA ---
st.markdown("""
<div class="main-header">
    <h1>🧩 TTS Alkitab</h1>
    <p>Gunakan Logika di Luar Nalar!</p>
</div>
""", unsafe_allow_html=True)

# Ambil data soal yang aktif
idx = st.session_state.current_idx
q_data = questions[idx]
ans_lontong = q_data['lontong'].upper()
ans_normal = q_data['normal'].upper()

# Navigasi Dropdown Soal
selected_q = st.selectbox(
    "Pilih Daftar Soal:", 
    range(1, len(questions) + 1), 
    index=idx, 
    format_func=lambda x: f"Contoh Soal {x}" if x <= 2 else f"Soal Nomor {x-2}"
)
if selected_q - 1 != idx:
    st.session_state.current_idx = selected_q - 1
    st.rerun()

st.write(f"**Pertanyaan:** {q_data['q']}")

# Hitung letak Hint jika belum ada
if st.session_state.hint_indices[idx] == -1:
    st.session_state.hint_indices[idx] = calculate_hint(ans_normal, ans_lontong)

# Menampilkan Hint Teks (Muncul di atas kotak input jika hint diminta)
hint_display = []
for i in range(len(ans_lontong)):
    if st.session_state.hint_shown[idx] and i == st.session_state.hint_indices[idx]:
        hint_display.append(ans_lontong[i])
    else:
        hint_display.append("_")

if st.session_state.hint_shown[idx]:
    st.markdown(f"<div class='hint-text'>{''.join(hint_display)}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='hint-text' style='color: transparent;'>{''.join(hint_display)}</div>", unsafe_allow_html=True)

# --- KOLOM INPUT JAWABAN TUNGGAL (AUTO NEXT & DELETE) ---
# Menggunakan satu text_input tapi dimaksimalkan batas karakternya sesuai jawaban
user_input = st.text_input(
    label="Jawaban",
    value=st.session_state.user_answers[idx],
    max_chars=len(ans_lontong),
    key=f"input_{idx}",
    label_visibility="collapsed",
    disabled=st.session_state.is_correct[idx]
).upper()

# Simpan progress ketikan ke memori
st.session_state.user_answers[idx] = user_input

st.caption(f"*Jumlah huruf: {len(ans_lontong)} | Ketik hurufnya bersambung, akan otomatis berjarak!*")

# --- TOMBOL AKSI JAWAB & HINT ---
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if not st.session_state.is_correct[idx]:
        if st.button("Kunci Jawaban ✅", use_container_width=True):
            if len(user_input) < len(ans_lontong):
                st.warning(f"Isi semua {len(ans_lontong)} huruf dulu, ya!")
            elif user_input == ans_lontong:
                st.session_state.is_correct[idx] = True
                st.rerun()
            else:
                st.error("Tetooot! ❌ Salah! Coba pakai logika Cak Lontong.")

with col_btn2:
    if not st.session_state.is_correct[idx] and not st.session_state.hint_shown[idx]:
        if st.button("Minta Hint 💡", use_container_width=True):
            st.session_state.hint_shown[idx] = True
            st.rerun()

# --- ALERT JIKA BENAR ---
if st.session_state.is_correct[idx]:
    st.success("BENAR! 🎉")
    st.warning(f"**Alasan Logis:** {q_data['reason']}")

st.write("")

# --- TOMBOL NAVIGASI BAWAH ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if idx > 0:
        if st.button("⬅️ Soal Sebelumnya", use_container_width=True):
            st.session_state.current_idx -= 1
            st.rerun()
with col_nav2:
    if idx < len(questions) - 1:
        if st.button("Soal Berikutnya ➡️", use_container_width=True):
            st.session_state.current_idx += 1
            st.rerun()
