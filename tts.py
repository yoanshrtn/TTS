import streamlit as st
import random

# --- KONFIGURASI HALAMAN & CSS ---
st.set_page_config(page_title="TTS Alkitab Nyeleneh", page_icon="🧩", layout="centered")

# Custom CSS agar input box mirip kotak TTS (teks di tengah, besar, dan tebal)
st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
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

# --- INISIALISASI STATE (Agar bisa pindah soal tanpa kehilangan jawaban) ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'user_answers' not in st.session_state:
    # Simpan jawaban tiap huruf untuk setiap soal (List of Lists)
    st.session_state.user_answers = [["" for _ in range(len(q['lontong']))] for q in questions]
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

# Ambil index aktif
idx = st.session_state.current_idx
q_data = questions[idx]
ans_lontong = q_data['lontong'].upper()
ans_normal = q_data['normal'].upper()

# --- TAMPILAN UTAMA ---
st.title("🧩 TTS Alkitab")

# Menu Dropdown untuk lompat ke soal tertentu
selected_q = st.selectbox(
    "Pilih Daftar Soal:", 
    range(1, len(questions) + 1), 
    index=idx, 
    format_func=lambda x: f"Contoh Soal {x}" if x <= 2 else f"Soal Nomor {x-2}"
)

# Deteksi jika dropdown diganti
if selected_q - 1 != idx:
    st.session_state.current_idx = selected_q - 1
    st.rerun()

st.markdown("---")
st.write(f"**Pertanyaan:** {q_data['q']}")

# Hitung letak Hint (hanya 1 kali per soal)
if st.session_state.hint_indices[idx] == -1:
    st.session_state.hint_indices[idx] = calculate_hint(ans_normal, ans_lontong)

# --- KOLOM KOTAK JAWABAN (SATU HURUF PER KOTAK) ---
cols = st.columns(len(ans_lontong))

for i in range(len(ans_lontong)):
    with cols[i]:
        # Jika peserta minta Hint, otomatis isi kotaknya dengan huruf yang benar
        if st.session_state.hint_shown[idx] and i == st.session_state.hint_indices[idx]:
            st.session_state.user_answers[idx][i] = ans_lontong[i]
            
        # Text input (max_chars=1) agar mirip TTS sungguhan
        val = st.text_input(
            label=f"box_{idx}_{i}",
            value=st.session_state.user_answers[idx][i],
            max_chars=1,
            key=f"input_{idx}_{i}",
            label_visibility="collapsed",
            disabled=st.session_state.is_correct[idx] # Kunci kotak jika jawaban sudah benar
        )
        st.session_state.user_answers[idx][i] = val.upper()

st.caption(f"*Jumlah kotak: {len(ans_lontong)} huruf*")

# Gabungkan huruf dari kotak-kotak
user_full_answer = "".join(st.session_state.user_answers[idx])

# --- TOMBOL AKSI JAWAB & HINT ---
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if not st.session_state.is_correct[idx]:
        if st.button("Kunci Jawaban ✅", use_container_width=True):
            if len(user_full_answer) < len(ans_lontong):
                st.warning("Isi semua kotak dulu, ya!")
            elif user_full_answer == ans_lontong:
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
st.write("")

# --- TOMBOL NAVIGASI BAWAH (SEBELUMNYA / BERIKUTNYA) ---
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
