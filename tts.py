
import streamlit as st
import streamlit.components.v1 as components
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Teka-teki Alkitab", page_icon="🧩", layout="centered")

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
    
    /* Desain Input Kotak TTS (Terpisah) */
    div[data-testid="stTextInput"] input {
        text-align: center !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        background-color: #F8F9FA;
        border: 2px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px !important;
        color: #1F2937;
    }
    
    /* Input disabled (Saat jawaban benar/hint/lihat jawaban) */
    div[data-testid="stTextInput"] input:disabled {
        background-color: #E5E7EB;
        color: #047857; /* Warna hijau tua */
        border: 2px solid #34D399;
    }
    
    /* Menyembunyikan Label di atas kotak */
    div[data-testid="stTextInput"] label {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA SOAL ---
questions = [
    {"q": "Karena tidak mau pergi ke Niniwe, Nabi Yunus akhirnya ditelan oleh ikan...", "normal": "BESAR", "lontong": "HIDUP"},
    {"q": "Saat dikejar pasukan Firaun, dengan tongkatnya Nabi Musa membelah laut...", "normal": "MERAH", "lontong": "DALAM"},
    {"q": "Hukuman untuk Daniel karena tetap berdoa kepada Allah adalah dilempar ke dalam gua...", "normal": "SINGA", "lontong": "GELAP"},
    {"q": "Simson akhirnya kehilangan semua kekuatannya setelah rambutnya di...", "normal": "POTONG", "lontong": "PENDEK"},
    {"q": "Karena badannya pendek, Zakheus memanjat pohon ara supaya bisa melihat...", "normal": "YESUS", "lontong": "JELAS"},
    {"q": "Saat berjalan di atas air menuju Yesus lalu melihat tiupan angin sakal, Petrus menjadi...", "normal": "TAKUT", "lontong": "BASAH"},
    {"q": "Tindakan Yudas Iskariot rela menyerahkan Yesus kepada imam-imam kepala demi mendapatkan 30 keping...", "normal": "PERAK", "lontong": "SALAH"},
    {"q": "Meskipun diuji dengan kehilangan seluruh hartanya dan anak-anaknya meninggal, Ayub tetap...", "normal": "SETIA", "lontong": "HIDUP"},
    {"q": "Esau rela menjual hak kesulungannya kepada Yakub hanya demi semangkuk sayur kacang...", "normal": "MERAH", "lontong": "PANAS"},
    {"q": "Nabi Elia sendirian menantang 450 nabi palsu dewa Baal di atas Gunung...", "normal": "KARMEL", "lontong": "BERANI"},
    {"q": "Sebelum merayakan Paskah, Yesus memberi teladan kerendahan hati dengan membasuh kaki...", "normal": "MURID", "lontong": "KOTOR"},
    {"q": "Martir pertama di gereja mula-mula yang mati syahid karena dilempari batu bertubi-tubi oleh orang Yahudi...", "normal": "STEFANUS", "lontong": "BERDARAH"},
    {"q": "Untuk bisa masuk ke tanah Kanaan, bangsa Israel yang dipimpin Yosua berjalan menyeberangi sungai...", "normal": "YORDAN", "lontong": "KERING"}
]

# --- INISIALISASI STATE TERSIMPAN ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = [False] * len(questions)
if 'is_revealed' not in st.session_state:
    st.session_state.is_revealed = [False] * len(questions)
if 'hint_shown' not in st.session_state:
    st.session_state.hint_shown = [False] * len(questions)
if 'hint_indices' not in st.session_state:
    st.session_state.hint_indices = [-1] * len(questions)
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = ""
if 'warning_msg' not in st.session_state:
    st.session_state.warning_msg = ""

def calculate_hint(normal, lontong):
    matches = [i for i in range(len(lontong)) if i < len(normal) and normal[i] == lontong[i]]
    if matches:
        return matches[0]
    return random.randint(1, len(lontong) - 1) if len(lontong) > 1 else 0

# Set up state input kotak untuk semua soal
for i, q in enumerate(questions):
    ans_lontong = q['lontong'].upper()
    if st.session_state.hint_indices[i] == -1:
        st.session_state.hint_indices[i] = calculate_hint(q['normal'].upper(), ans_lontong)
    for j in range(len(ans_lontong)):
        key = f"box_{i}_{j}"
        if key not in st.session_state:
            st.session_state[key] = ""

# --- FUNGSI CALLBACKS ---
def check_answer():
    idx = st.session_state.current_idx
    ans_lontong = questions[idx]['lontong'].upper()
    
    # Gabungkan jawaban dari kotak-kotak
    user_ans = "".join([st.session_state[f"box_{idx}_{i}"].upper() for i in range(len(ans_lontong))])
    
    if len(user_ans) < len(ans_lontong):
        st.session_state.warning_msg = f"Isi semua {len(ans_lontong)} huruf dulu, ya!"
        st.session_state.error_msg = ""
    elif user_ans == ans_lontong:
        st.session_state.is_correct[idx] = True
        st.session_state.error_msg = ""
        st.session_state.warning_msg = ""
    else:
        st.session_state.error_msg = "Tetooot! ❌ Salah! Coba pakai logika Cak Lontong."
        st.session_state.warning_msg = ""
        # Bersihkan semua kotak kecuali hint
        for i in range(len(ans_lontong)):
            if not (st.session_state.hint_shown[idx] and i == st.session_state.hint_indices[idx]):
                st.session_state[f"box_{idx}_{i}"] = ""

def get_hint():
    idx = st.session_state.current_idx
    ans_lontong = questions[idx]['lontong'].upper()
    st.session_state.hint_shown[idx] = True
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""
    
    # Bersihkan kotak lain, isi kotak hint
    for i in range(len(ans_lontong)):
        if i == st.session_state.hint_indices[idx]:
            st.session_state[f"box_{idx}_{i}"] = ans_lontong[i]
        else:
            st.session_state[f"box_{idx}_{i}"] = ""

def reveal_answer():
    idx = st.session_state.current_idx
    ans_lontong = questions[idx]['lontong'].upper()
    
    # Isi semua kotak dengan jawaban benar & ubah status jadi REVEALED
    for i in range(len(ans_lontong)):
        st.session_state[f"box_{idx}_{i}"] = ans_lontong[i]
    st.session_state.is_revealed[idx] = True
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""

def go_prev():
    st.session_state.current_idx -= 1
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""

def go_next():
    st.session_state.current_idx += 1
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""


# --- HEADER UTAMA ---
st.markdown("""
<div class="main-header">
    <h1>🧩 TTS Alkitab</h1>
    <p>Gunakan Logika di Luar Nalar!</p>
</div>
""", unsafe_allow_html=True)

idx = st.session_state.current_idx
q_data = questions[idx]
ans_lontong = q_data['lontong'].upper()

# --- PASTIKAN KOTAK TETAP TERISI JIKA SOAL SUDAH DIJAWAB BENAR / DIBUKA JAWABANNYA ---
if st.session_state.is_correct[idx] or st.session_state.is_revealed[idx]:
    for i in range(len(ans_lontong)):
        st.session_state[f"box_{idx}_{i}"] = ans_lontong[i]

# --- NAVIGASI DROPDOWN YANG SINKRON ---
selected_q = st.selectbox(
    "Pilih Daftar Soal:", 
    range(1, len(questions) + 1), 
    index=idx, 
    format_func=lambda x: f"Contoh Soal {x}" if x <= 2 else f"Soal Nomor {x-2}"
)

# Jika ada perubahan dari dropdown manual, kita reroute
if (selected_q - 1) != idx:
    st.session_state.current_idx = selected_q - 1
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""
    st.rerun()

st.write(f"**Pertanyaan:** {q_data['q']}")

# --- KOLOM KOTAK JAWABAN MISAH ---
cols = st.columns(len(ans_lontong))

for i in range(len(ans_lontong)):
    with cols[i]:
        is_hint = st.session_state.hint_shown[idx] and i == st.session_state.hint_indices[idx]
        is_disabled = st.session_state.is_correct[idx] or st.session_state.is_revealed[idx] or is_hint
        
        # Penambahan autocomplete="off" untuk mencegah munculnya history input dari browser
        st.text_input(
            label=f"hidden_{idx}_{i}",
            max_chars=1,
            key=f"box_{idx}_{i}",
            disabled=is_disabled,
            autocomplete="off" 
        )

st.caption(f"*Jumlah kotak: {len(ans_lontong)} huruf*")

# --- INJEKSI JAVASCRIPT ---
# Memastikan event listener global dipasang agar selalu auto-focus saat pindah soal
# Serta menambahkan setting atribut "autocomplete = off" secara paksa ke HTML
js_code = """
<script>
const doc = window.parent.document;

// Paksa semua input kotak untuk matiin suggestion/autocomplete browser
const disableAutocomplete = () => {
    const allInputs = doc.querySelectorAll('div[data-testid="stTextInput"] input');
    allInputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('spellcheck', 'false');
    });
};
disableAutocomplete();
// Panggil lagi kalau-kalau Streamlit render ulang elemennya
setTimeout(disableAutocomplete, 500); 

if (!doc.getElementById("tts-listener-installed")) {
    const marker = doc.createElement("div");
    marker.id = "tts-listener-installed";
    marker.style.display = "none";
    doc.body.appendChild(marker);

    // Event saat mengetik
    doc.addEventListener('input', function(e) {
        const isTextInput = e.target.closest('div[data-testid="stTextInput"]');
        if (isTextInput && e.target.tagName === 'INPUT') {
            const allInputs = Array.from(doc.querySelectorAll('div[data-testid="stTextInput"] input'));
            const index = allInputs.indexOf(e.target);
            
            if (index > -1 && e.target.value.length === 1 && index < allInputs.length - 1) {
                let next_input = allInputs[index + 1];
                if (next_input && next_input.disabled && index + 2 < allInputs.length) {
                    allInputs[index + 2].focus();
                } else if (next_input && !next_input.disabled) {
                    next_input.focus();
                }
            }
        }
    });

    // Event saat menghapus (Backspace)
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'Backspace') {
            const isTextInput = e.target.closest('div[data-testid="stTextInput"]');
            if (isTextInput && e.target.tagName === 'INPUT' && e.target.value.length === 0) {
                const allInputs = Array.from(doc.querySelectorAll('div[data-testid="stTextInput"] input'));
                const index = allInputs.indexOf(e.target);
                
                if (index > 0) {
                    let prev_input = allInputs[index - 1];
                    if (prev_input && prev_input.disabled && index - 2 >= 0) {
                        allInputs[index - 2].focus();
                        e.preventDefault(); 
                    } else if (prev_input && !prev_input.disabled) {
                        prev_input.focus();
                        e.preventDefault();
                    }
                }
            }
        }
    });
}
</script>
"""
components.html(js_code, height=0)


# --- TOMBOL AKSI JAWAB, HINT, & LIHAT JAWABAN ---
if not (st.session_state.is_correct[idx] or st.session_state.is_revealed[idx]):
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        st.button("Cek Jawaban ✅", use_container_width=True, on_click=check_answer)
        
    with col_btn2:
        if not st.session_state.hint_shown[idx]:
            st.button("Minta Hint 💡", use_container_width=True, on_click=get_hint)
            
    with col_btn3:
        st.button("Lihat Jawaban 🏳️", use_container_width=True, on_click=reveal_answer)


# --- ALERT MESSAGE ---
if st.session_state.is_correct[idx]:
    st.success("BENAR! 🎉")
elif st.session_state.is_revealed[idx]:
    st.info("Kamu menyerah, jawaban telah ditampilkan.")
    
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)
if st.session_state.warning_msg:
    st.warning(st.session_state.warning_msg)

st.write("")

# --- TOMBOL NAVIGASI BAWAH ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if idx > 0:
        st.button("⬅️ Soal Sebelumnya", use_container_width=True, on_click=go_prev)
with col_nav2:
    if idx < len(questions) - 1:
        st.button("Soal Berikutnya ➡️", use_container_width=True, on_click=go_next)
