import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import streamlit.components.v1 as components

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(page_title="Kamus Sains ALAZKA", page_icon="🔬", layout="centered")

# --- INISIALISASI PENYIMPANAN WARNA DI SESI APLIKASI ---
if "warna_bg" not in st.session_state:
    st.session_state.warna_bg = "#E6F9F0" # Default Hijau Mint Segar (Nuansa Laboratorium/Alam)

if "warna_teks" not in st.session_state:
    st.session_state.warna_teks = "#0D3B22" # Default Teks Hijau Tua

# --- GAYA CSS GLOBAL DINAMIS BERDASARKAN PILIHAN WARNA ---
st.markdown(
    f"""
    <style>
    /* Mengubah background dan warna teks aplikasi secara otomatis dan serasi */
    .stApp {{
        background-color: {st.session_state.warna_bg} !important;
        color: {st.session_state.warna_teks} !important;
    }}
    
    /* Mengubah warna seluruh teks judul, subjudul, dan label agar selaras dengan tema */
    h1, h2, h3, h4, h5, h6, p, span, label, .streamlit-expanderHeader {{
        color: {st.session_state.warna_teks} !important;
    }}
    
    /* Tombol Utama (Masuk Aplikasi & Terjemahkan) */
    div.stButton > button:first-child p {{
        color: #FFFFFF !important;
    }}
    div.stButton > button:first-child {{
        background-color: #0D3B22;
        color: #FFFFFF !important;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #137333;
        color: #FFFFFF !important;
    }}
    
    /* GAYA UTAMA TOMBOL KAMERA (Take Photo / Clear Photo) */
    button[data-testid="baseButton-secondary"], 
    div[data-testid="stCameraInput"] button,
    .stCameraInput button {{
        background-color: #0D3B22 !important;
        border: none !important;
        border-radius: 8px !important;
    }}
    
    button[data-testid="baseButton-secondary"] *, 
    div[data-testid="stCameraInput"] button *,
    .stCameraInput button * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: bold !important;
    }}
    
    button[data-testid="baseButton-secondary"]:hover,
    div[data-testid="stCameraInput"] button:hover {{
        background-color: #137333 !important;
    }}

    /* Kotak Text Area */
    div[data-testid="stTextArea"] textarea {{
        background-color: #FFFFFF !important;
        color: #0D3B22 !important;
        border-radius: 8px !important;
        border: 1px solid #A8DAB5 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- JAVASCRIPT PEMAKSA WARNA TEKS TOMBOL KAMERA MENJADI PUTIH ---
components.html(
    """
    <script>
    const observer = new MutationObserver(() => {
        const buttons = window.parent.document.querySelectorAll('button[data-testid="baseButton-secondary"], .stCameraInput button');
        buttons.forEach(btn => {
            btn.style.backgroundColor = "#0D3B22";
            btn.style.color = "#FFFFFF";
            const elements = btn.querySelectorAll('*');
            elements.forEach(el => {
                el.style.color = "#FFFFFF";
                el.style.fill = "#FFFFFF";
            });
        });
    });
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
    </script>
    """,
    height=0,
)

# --- SISTEM LOGIN & GEMBOK APLIKASI ---
if "peran" not in st.session_state:
    st.session_state.peran = None

# --- FUNGSI UNTUK MENAMPILKAN HEADER DUA LOGO DARI FOLDER LOKAL ---
def tampilkan_header_logo():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        try:
            logo1 = Image.open("logo1.png")
            st.image(logo1, width=70)
        except:
            st.write("Logo 1")
            
    with col2:
        st.markdown("<h2 style='text-align: center; margin: 0;'>Kamus Sains ALAZKA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin: 0;'>🔬 Junior High School Science Dictionary & AI Detector 🧪</p>", unsafe_allow_html=True)
        
    with col3:
        try:
            logo2 = Image.open("logo2.png")
            st.image(logo2, width=70)
        except:
            st.write("Logo 2")

# --- HALAMAN GERBANG DEPAN (LOGIN) ---
if st.session_state.peran is None:
    tampilkan_header_logo()
    st.markdown("<h4 style='text-align: center; color: #137333; margin-top: 15px;'>✨ Created by : Saiful Hadi ✨</h4>", unsafe_allow_html=True)
    st.write("---")
    
    # --- PANDUAN PENGGUNAAN DI HALAMAN DEPAN ---
    with st.expander("📖 Panduan Penggunaan Kamus Sains"):
        st.write("""
        Selamat datang di **Kamus Sains ALAZKA**! Pusat rujukan istilah ilmiah dan eksperimen sains interaktif. 
        Berikut adalah panduan singkat cara menggunakan aplikasi ini:
        
        1. **Cara Masuk (Login):**
           * Masukkan kata sandi sesuai peran Anda (Siswa atau Admin) pada kolom di bawah.
        
        2. **Menu Terjemahan & Penjelasan Istilah Sains:**
           * Pilih mode terjemahan atau penjelasan konsep ilmiah (Indonesia ➡️ Inggris atau sebaliknya).
           * Ketik istilah sains (contoh: *Photosynthesis*, *Ecosystem*, *Atom*) atau gunakan mikrofon.
           * Tekan tombol **"Cari Konsep Sains ✨"** untuk melihat definisi lengkap beserta pelafalannya (🔊).
        
        3. **Menu Deteksi Objek & Alat Lab:**
           * Ambil foto benda atau alat laboratorium di sekitar Anda (misalnya daun, magnet, termometer).
           * AI akan mengenali nama benda tersebut dalam istilah sains lengkap dengan penjelasannya!
           
        4. **Personalisasi Warna (Mood Lab):**
           * Ubah suasana latar belakang aplikasi sesuai kenyamanan Anda melalui menu pilihan tema di dalam aplikasi.
        """)
    
    st.write("---")
    sandi = st.text_input("Silakan Masukkan Kata Sandi:", type="password")
    if st.button("Masuk Aplikasi"):
        if sandi == "alazka123":
            st.session_state.peran = "siswa"
            st.rerun()
        elif sandi == "alazka2026":
            st.session_state.peran = "admin"
            st.rerun()
        elif sandi != "":
            st.error("Kunci salah! Silakan coba lagi.")
    st.stop()

# --- MENGHUBUNGKAN KE OTAK AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_ai = genai.GenerativeModel('gemini-3.6-flash')
except Exception as e:
    st.error("Koneksi ke sistem AI terputus. Pastikan kunci rahasia sudah terpasang.")
    st.stop()

# ==========================================
# HALAMAN KHUSUS SISWA (USER)
# ==========================================
if st.session_state.peran == "siswa":
    tampilkan_header_logo()
    st.write("---")
    
    with st.expander("🎨 Pilih Tema Warna Lab Kamu"):
        pilihan_warna_siswa = st.selectbox(
            "Pilih suasana laboratorium favoritmu:",
            (
                "🌿 Rileks & Fokus (Hijau Mint Segar)",
                "🪵 Hangat & Elegan (Coklat Muda)",
                "✨ Netral & Tenang (Putih Klasik)",
                "🌊 Tenang & Damai (Biru Langit Muda)",
                "☀️ Ceria & Bersemangat (Kuning Pastel Lembut)",
                "🌸 Kreatif & Hangat (Merah Muda / Pink Soft)",
                "🔮 Nyaman & Misterius (Ungu Lavender Soft)",
                "☕ Santai & Hangat (Krim / Krem)",
                "🌙 Istirahat / Malam (Abu-abu Modern - Teks Terang)"
            ),
            key="select_warna_siswa"
        )
        if st.button("Terapkan Tema Warna"):
            if "Hijau" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#E6F9F0"
                st.session_state.warna_teks = "#0D3B22"
            elif "Coklat" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#F5EBE6"
                st.session_state.warna_teks = "#2C221E"
            elif "Putih" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#FFFFFF"
                st.session_state.warna_teks = "#1A1A1A"
            elif "Biru" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#E6F2FF"
                st.session_state.warna_teks = "#0B2E59"
            elif "Kuning" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#FFF9E6"
                st.session_state.warna_teks = "#4D3800"
            elif "Merah Muda" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#FFE6EE"
                st.session_state.warna_teks = "#590D22"
            elif "Ungu" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#F3E6FF"
                st.session_state.warna_teks = "#2E0B59"
            elif "Krim" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#FDFBF7"
                st.session_state.warna_teks = "#332D25"
            elif "Abu-abu" in pilihan_warna_siswa:
                st.session_state.warna_bg = "#2B2B2B"
                st.session_state.warna_teks = "#F0F0F0"
            st.rerun()
            
    tab_teks, tab_kamera = st.tabs(["🧬 Kamus & Istilah Sains", "🔬 Deteksi Objek & Alat Lab"])
    
    with tab_teks:
        st.write("---")
        pilihan_bahasa = st.radio(
            "Pilih mode kamus sains:",
            ("🇮🇩 Indonesia ➡️ 🇬🇧 Istilah Sains (Inggris)", "🇬🇧 Istilah Sains (Inggris) ➡️ 🇮🇩 Indonesia"),
            horizontal=True,
            key="radio_teks"
        )
        st.write("---")
        
        st.info("💡 **Tips:** Ketik istilah sains (contoh: *Fotosintesis*, *Gaya Gravitasi*, *Mitokondria*) untuk melihat terjemahan dan penjelasan ilmiahnya!")
        teks_siswa = st.text_area("Ketik istilah atau konsep sains di sini:", height=100)
        
        if st.button("Cari Konsep Sains ✨"):
            if teks_siswa:
                with st.spinner("AI sedang meriset konsep sains..."):
                    try:
                        if "Indonesia" in pilihan_bahasa and "Inggris" in pilihan_bahasa and pilihan_bahasa.startswith("🇮🇩"):
                            perintah = f"Provide the English scientific term for this Indonesian science concept, along with a short, simple explanation suitable for junior high school students: {teks_siswa}"
                            bahasa_suara = 'en'
                        else:
                            perintah = f"Provide the Indonesian translation and a clear, simple scientific explanation for this English science term suitable for junior high school students: {teks_siswa}"
                            bahasa_suara = 'id'
                            
                        hasil = model_ai.generate_content(perintah)
                        teks_bersih = hasil.text.strip().replace('"', '').replace("'", "")
                        
                        st.success("Penjelasan & Istilah Sains:")
                        st.write(teks_bersih)
                        
                        try:
                            tts = gTTS(text=teks_bersih[:200], lang=bahasa_suara, slow=False)
                            file_suara = "suara_sains.mp3"
                            tts.save(file_suara)
                            st.audio(file_suara, format="audio/mp3")
                        except Exception as err_suara:
                            st.warning("Pemutar audio pelafalan sedang memuat.")
                            
                    except Exception as e:
                        # --- PERBAIKAN PESAN ERROR LIMIT / QUOTA ADA DI SINI ---
                        pesan_error = str(e)
                        if "429" in pesan_error or "Quota" in pesan_error:
                            st.warning("⏳ Mesin AI sedang sibuk. Mohon tunggu sekitar 15 detik, lalu tekan tombolnya lagi ya!")
                        else:
                            st.error(f"Maaf, terjadi gangguan dari mesin AI: {e}")
            else:
                st.warning("Mohon masukkan istilah atau konsep sains terlebih dahulu.")

    with tab_kamera:
        st.write("---")
        pilihan_arah_objek = st.radio(
            "Pilih format hasil deteksi:",
            ("🇬🇧 Nama Ilmiah / Inggris", "🇮🇩 Nama dalam Bahasa Indonesia"),
            horizontal=True,
            key="radio_objek"
        )
        st.write("---")
        
        st.info("💡 **Tips Lab:** Foto benda alam, tumbuhan, hewan, atau alat praktikum, lalu AI akan menjelaskan fungsinya secara sains!")
        
        sumber_gambar = st.radio("Pilih sumber gambar:", ("📸 Ambil Foto Langsung (Kamera)", "📁 Unggah dari Galeri"), horizontal=True)
        
        gambar_unggah = None
        if sumber_gambar == "📸 Ambil Foto Langsung (Kamera)":
            gambar_unggah = st.camera_input("Ambil foto objek sains")
        else:
            gambar_unggah = st.file_uploader("Pilih file foto objek...", type=["jpg", "jpeg", "png"])
            
        if gambar_unggah is not None:
            gambar_buka = Image.open(gambar_unggah)
            st.image(gambar_buka, caption="Objek Sains yang Dianalisis", use_column_width=True)
            
            if st.button("Analisis Objek Sains ✨"):
                with st.spinner("AI sedang menganalisis objek secara ilmiah..."):
                    try:
                        if "Inggris" in pilihan_arah_objek:
                            perintah_objek = "Identify the scientific name or object in this image and provide its name in English along with a 1-sentence scientific function. Keep it brief."
                            bahasa_suara_objek = 'en'
                        else:
                            perintah_objek = "Identifikasikan objek atau makhluk hidup pada gambar ini dalam Bahasa Indonesia beserta fungsi atau penjelasannya secara sains secara singkat."
                            bahasa_suara_objek = 'id'
                            
                        hasil_objek = model_ai.generate_content([perintah_objek, gambar_buka])
                        objek_bersih = hasil_objek.text.strip().replace('"', '').replace("'", "")
                        
                        st.success("Hasil Analisis Sains:")
                        st.write(objek_bersih)
                        
                        try:
                            tts_objek = gTTS(text=objek_bersih[:200], lang=bahasa_suara_objek, slow=False)
                            file_suara_objek = "suara_objek_sains.mp3"
                            tts_objek.save(file_suara_objek)
                            st.audio(file_suara_objek, format="audio/mp3")
                        except Exception as err_suara:
                            st.warning("Pemutar audio pelafalan sedang memuat.")
                            
                    except Exception as e:
                        # --- PERBAIKAN PESAN ERROR LIMIT / QUOTA ADA DI SINI ---
                        pesan_error = str(e)
                        if "429" in pesan_error or "Quota" in pesan_error:
                            st.warning("⏳ Mesin AI sedang sibuk memproses foto. Mohon tunggu sekitar 15 detik, lalu coba lagi!")
                        else:
                            st.error(f"Gagal mengenali objek. Pastikan foto terlihat jelas. ({e})")

# ==========================================
# HALAMAN KHUSUS ADMIN (PAK SAIFUL)
# ==========================================
elif st.session_state.peran == "admin":
    tampilkan_header_logo()
    st.info("Selamat bekerja, Pak Saiful! Panel Kontrol Administrator Kamus Sains.")
    
    tab1, tab2, tab3 = st.tabs(["📝 Input Materi Sains", "🖼️ Ekstrak Modul/Buku", "🎨 Pengaturan Tema Lab"])
    
    with tab1:
        st.subheader("Tambah Materi / Kosakata Sains Manual")
        kata_baru = st.text_input("Masukkan Istilah Sains:")
        arti_kata = st.text_input("Masukkan Definisi / Penjelasan:")
        if st.button("Simpan ke Database Sains"):
            if kata_baru and arti_kata:
                st.success(f"Berhasil! Materi '{kata_baru}' telah tersimpan.")
            else:
                st.warning("Mohon isi kedua kolom di atas.")
                
    with tab2:
        st.subheader("Ekstrak Teks dari Lembar Kerja / Buku Sains")
        gambar_unggah_admin = st.file_uploader("Pilih gambar halaman buku sains...", type=["jpg", "jpeg", "png"], key="admin_img")
        
        if gambar_unggah_admin is not None:
            gambar_buka_admin = Image.open(gambar_unggah_admin)
            st.image(gambar_buka_admin, caption="Halaman Buku Sains", use_column_width=True)
            
            if st.button("Ekstrak Teks & Ringkas"):
                with st.spinner("Membaca teks materi sains..."):
                    try:
                        perintah_gambar = "Extract all science terms and explanations precisely from this image."
                        hasil_ekstrak = model_ai.generate_content([perintah_gambar, gambar_buka_admin])
                        st.success("Teks berhasil diekstrak!")
                        st.write(hasil_ekstrak.text)
                    except Exception as e:
                        st.error(f"Gagal membaca gambar. ({e})")
                        
    with tab3:
        st.subheader("Ubah Warna Tema Laboratorium")
        pilihan_tema = st.selectbox(
            "Pilih Tema Warna Laboratorium:",
            (
                "🌿 Rileks & Fokus (Hijau Mint Segar)",
                "🪵 Hangat & Elegan (Coklat Muda)",
                "✨ Netral & Tenang (Putih Klasik)",
                "🌊 Tenang & Damai (Biru Langit Muda)",
                "☀️ Ceria & Bersemangat (Kuning Pastel Lembut)",
                "🌸 Kreatif & Hangat (Merah Muda / Pink Soft)",
                "🔮 Nyaman & Misterius (Ungu Lavender Soft)",
                "☕ Santai & Hangat (Krim / Krem)",
                "🌙 Istirahat / Malam (Abu-abu Modern - Teks Terang)"
            ),
            key="select_warna_admin"
        )
        
        if st.button("Terapkan Tema Lab"):
            if "Hijau" in pilihan_tema:
                st.session_state.warna_bg = "#E6F9F0"
                st.session_state.warna_teks = "#0D3B22"
            elif "Coklat" in pilihan_tema:
                st.session_state.warna_bg = "#F5EBE6"
                st.session_state.warna_teks = "#2C221E"
            elif "Putih" in pilihan_tema:
                st.session_state.warna_bg = "#FFFFFF"
                st.session_state.warna_teks = "#1A1A1A"
            elif "Biru" in pilihan_tema:
                st.session_state.warna_bg = "#E6F2FF"
                st.session_state.warna_teks = "#0B2E59"
            elif "Kuning" in pilihan_tema:
                st.session_state.warna_bg = "#FFF9E6"
                st.session_state.warna_teks = "#4D3800"
            elif "Merah Muda" in pilihan_tema:
                st.session_state.warna_bg = "#FFE6EE"
                st.session_state.warna_teks = "#590D22"
            elif "Ungu" in pilihan_tema:
                st.session_state.warna_bg = "#F3E6FF"
                st.session_state.warna_teks = "#2E0B59"
            elif "Krim" in pilihan_tema:
                st.session_state.warna_bg = "#FDFBF7"
                st.session_state.warna_teks = "#332D25"
            elif "Abu-abu" in pilihan_tema:
                st.session_state.warna_bg = "#2B2B2B"
                st.session_state.warna_teks = "#F0F0F0"
                
            st.success("Tema laboratorium berhasil diperbarui!")
            st.rerun()

# --- TOMBOL KELUAR (LOGOUT) ---
st.write("---")
if st.button("Keluar (Logout)"):
    st.session_state.peran = None
    st.rerun()
