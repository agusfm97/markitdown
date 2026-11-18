import streamlit as st
from markitdown import MarkItDown
import os
import tempfile

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="MarkItDown Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CUSTOM CSS (Dark Mode Modern) ====================
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }

    /* File info card */
    .file-card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .file-card h4 {
        margin: 0 0 0.5rem 0;
        color: #667eea;
    }

    .file-detail {
        display: flex;
        justify-content: space-between;
        padding: 0.25rem 0;
        border-bottom: 1px solid #333;
        font-size: 0.9rem;
    }

    .file-detail:last-child {
        border-bottom: none;
    }

    .file-detail .label {
        color: #888;
    }

    .file-detail .value {
        color: #fff;
        font-weight: 500;
    }

    /* Success message */
    .success-box {
        background: #1b5e20;
        color: #fff;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Stats cards */
    .stat-card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.25rem;
    }

    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        filter: brightness(1.1);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 2rem;
    }

    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.1);
    }

    /* Sidebar styling */
    .sidebar-section {
        margin-bottom: 1.5rem;
    }

    .sidebar-section h3 {
        color: #667eea;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    /* Warning box */
    .warning-box {
        background: #3e2723;
        border: 1px solid #5d4037;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffccbc;
    }

    .warning-box b {
        color: #ffab91;
    }
</style>
""", unsafe_allow_html=True)

# ==================== JUDUL & DESKRIPSI ====================
st.markdown('<h1 class="main-title">📄 MarkItDown Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Konversi berbagai format file menjadi <b>Markdown</b> menggunakan <a href="https://github.com/microsoft/markitdown" target="_blank">Microsoft MarkItDown</a>.</p>', unsafe_allow_html=True)
st.markdown("""
Dibuat dengan ❤️ untuk manfaat bersama — **gratis untuk semua orang**.  
*Semoga bermanfaat dan menjadi pahala bagi kita semua. Amin.*
""")

st.divider()

# ==================== INISIALISASI KONVERTER ====================
@st.cache_resource
def get_converter():
    return MarkItDown(enable_plugins=False)

converter = get_converter()

# ==================== FORMAT YANG DIDUKUNGI ====================
# Format yang stabil di Streamlit Cloud (Python-only dependencies)
STABLE_FORMATS = [
    "docx", "doc", "pptx", "ppt", "xlsx", "xls",
    "html", "htm", "txt", "csv", "json", "xml", "epub",
    "zip",
]

# Format yang mungkin terbatas di Streamlit Cloud (butuh dependensi sistem)
LIMITED_FORMATS = {
    "pdf": "Butuh poppler-utils (sistem) — mungkin tidak berjalan di Streamlit Cloud gratis",
    "png": "Hanya EXIF metadata, tidak ada OCR",
    "jpg": "Hanya EXIF metadata, tidak ada OCR",
    "jpeg": "Hanya EXIF metadata, tidak ada OCR",
    "webp": "Hanya EXIF metadata, tidak ada OCR",
    "bmp": "Hanya EXIF metadata, tidak ada OCR",
    "mp3": "Hanya metadata, tidak ada transkripsi",
    "wav": "Hanya metadata, tidak ada transkripsi",
    "m4a": "Hanya metadata, tidak ada transkripsi",
    "ogg": "Hanya metadata, tidak ada transkripsi",
}

ALL_EXTENSIONS = STABLE_FORMATS + list(LIMITED_FORMATS.keys())

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📋 Format yang Didukung")

    st.markdown("### ✅ Stabil (direkomendasikan)")
    st.markdown("""
    **Dokumen:** Word (DOC/DOCX), PowerPoint (PPT/PPTX), Excel (XLS/XLSX)  
    **Web & Teks:** HTML, TXT, CSV, JSON, XML, EPUB  
    **Arsip:** ZIP
    """)

    st.markdown("### ⚠️ Terbatas di Streamlit Cloud")
    st.markdown("""
    **PDF:** Butuh poppler-utils (sistem)  
    **Gambar:** Hanya EXIF metadata (tidak ada OCR)  
    **Audio:** Hanya metadata (tidak ada transkripsi)
    """)

    st.divider()

    st.markdown("### ℹ️ Tentang")
    st.info("""
    Aplikasi ini menggunakan [Microsoft MarkItDown](https://github.com/microsoft/markitdown) 
    untuk mengonversi file menjadi Markdown.

    Deploy gratis di [Streamlit Community Cloud](https://streamlit.io/cloud).
    """)

    st.markdown("---")
    st.markdown("Semoga bermanfaat & menjadi pahala. Amin. 🤲")

# ==================== AREA UPLOAD ====================
st.markdown("## 📤 Upload File")

uploaded_file = st.file_uploader(
    "Pilih file yang ingin dikonversi",
    type=ALL_EXTENSIONS,
    help="Ukuran maksimal disesuaikan oleh Streamlit Cloud (biasanya ~200 MB)",
)

if uploaded_file is not None:
    # Cek apakah format dalam limited formats
    file_ext = uploaded_file.name.split(".")[-1].lower()
    is_limited = file_ext in LIMITED_FORMATS

    if is_limited:
        st.markdown(f"""
        <div class="warning-box">
            <b>⚠️ Perhatian:</b> Format <b>{file_ext.upper()}</b> — {LIMITED_FORMATS[file_ext]}
        </div>
        """, unsafe_allow_html=True)

    # Tampilkan info file dalam card
    st.markdown(f"""
    <div class="file-card">
        <h4>📁 File yang Diunggah</h4>
        <div class="file-detail"><span class="label">Nama:</span> <span class="value">{uploaded_file.name}</span></div>
        <div class="file-detail"><span class="label">Tipe:</span> <span class="value">{uploaded_file.type or 'Tidak diketahui'}</span></div>
        <div class="file-detail"><span class="label">Ukuran:</span> <span class="value">{uploaded_file.size / 1024:.2f} KB</span></div>
        <div class="file-detail"><span class="label">Ekstensi:</span> <span class="value">.{file_ext}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol konversi
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        convert_clicked = st.button("🔄 Konversi ke Markdown", type="primary", use_container_width=True)

    if convert_clicked:
        try:
            with st.spinner("🔄 Sedang mengonversi file... mohon tunggu"):
                # Baca file ke bytes
                file_bytes = uploaded_file.read()

                # Simpan ke temporary file (markitdown butuh path)
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=f".{file_ext}"
                ) as tmp_file:
                    tmp_file.write(file_bytes)
                    tmp_path = tmp_file.name

                try:
                    # Konversi
                    result = converter.convert(tmp_path)
                    markdown_text = result.text_content

                    # Tampilkan hasil sukses
                    st.markdown("""
                    <div class="success-box">
                        ✅ <b>Konversi berhasil!</b>
                    </div>
                    """, unsafe_allow_html=True)

                    st.divider()

                    # Header hasil
                    st.markdown("## 📝 Hasil Konversi Markdown")

                    # Text area untuk hasil
                    st.text_area(
                        "Konten Markdown",
                        value=markdown_text,
                        height=500,
                        key="markdown_output",
                        label_visibility="collapsed",
                    )

                    # Tombol unduh
                    st.download_button(
                        label="⬇️ Unduh File Markdown (.md)",
                        data=markdown_text.encode("utf-8"),
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

                    # Statistik dalam cards
                    st.markdown("### 📊 Statistik")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value">{len(markdown_text):,}</div>
                            <div class="stat-label">Karakter</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value">{len(markdown_text.split()):,}</div>
                            <div class="stat-label">Kata</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value">{markdown_text.count(chr(10)) + 1:,}</div>
                            <div class="stat-label">Baris</div>
                        </div>
                        """, unsafe_allow_html=True)

                finally:
                    # Bersihkan temporary file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat konversi: {str(e)}")
            st.markdown("""
            **Kemungkinan penyebab:**
            - File rusak atau tidak valid
            - Format tidak didukung sepenuhnya di Streamlit Cloud
            - Dependensi sistem tidak tersedia (untuk PDF, OCR gambar, transkripsi audio)

            Coba gunakan format lain seperti DOCX, PPTX, XLSX, HTML, TXT, CSV, JSON, atau XML.
            """)

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem 0;">
    Dibuat dengan ❤️ menggunakan <a href="https://streamlit.io" target="_blank" style="color: #667eea;">Streamlit</a> dan 
    <a href="https://github.com/microsoft/markitdown" target="_blank" style="color: #667eea;">Microsoft MarkItDown</a>.<br>
    Deploy gratis di <a href="https://streamlit.io/cloud" target="_blank" style="color: #667eea;">Streamlit Community Cloud</a>.<br>
    Kode sumber di GitHub untuk manfaat bersama.
</div>
""", unsafe_allow_html=True)
