import streamlit as st
from markitdown import MarkItDown
import os
import tempfile

st.set_page_config(
    page_title="MarkItDown Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
}

.hero p {
    font-size: 1.25rem;
    margin: 0;
    opacity: 0.9;
}

.feature-grid {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.feature-card {
    flex: 1;
    min-width: 200px;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.feature-card .icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
}

.feature-card h3 {
    color: #667eea;
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
}

.feature-card p {
    color: #888;
    font-size: 0.9rem;
    margin: 0;
}

.upload-section {
    background: #1e1e1e;
    border: 2px dashed #333;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
}

.upload-section h2 {
    color: #fff;
    margin: 0 0 1rem 0;
}

.upload-section p {
    color: #888;
    margin: 0;
}

.stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.stat-card {
    flex: 1;
    min-width: 150px;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    display: block;
}

.stat-label {
    color: #888;
    font-size: 0.85rem;
    margin-top: 0.25rem;
    display: block;
}

.result-box {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 0.9rem;
    border-top: 1px solid #333;
    margin-top: 2rem;
}

/* Hide Streamlit default elements */
.stDeployButton {visibility: hidden;}
.stDecoration {visibility: hidden;}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.75rem 2rem;
    color: white;
    width: 100%;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(1.1);
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
}

.stDownloadButton > button:hover {
    filter: brightness(1.1);
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

/* Success box */
.success-box {
    background: #1b5e20;
    color: #fff;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

/* Stat card */
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

# ==================== INISIALISASI KONVERTER ====================
@st.cache_resource
def get_converter():
    return MarkItDown(enable_plugins=False)

converter = get_converter()

# Format stabil di Streamlit Cloud
STABLE_FORMATS = [
    "docx", "doc", "pptx", "ppt", "xlsx", "xls",
    "html", "htm", "txt", "csv", "json", "xml", "epub",
    "zip",
]

LIMITED_FORMATS = {
    "pdf": "Butuh poppler-utils (sistem)",
    "png": "Hanya EXIF metadata",
    "jpg": "Hanya EXIF metadata",
    "jpeg": "Hanya EXIF metadata",
    "webp": "Hanya EXIF metadata",
    "bmp": "Hanya EXIF metadata",
    "mp3": "Hanya metadata",
    "wav": "Hanya metadata",
    "m4a": "Hanya metadata",
    "ogg": "Hanya metadata",
}

ALL_EXTENSIONS = STABLE_FORMATS + list(LIMITED_FORMATS.keys())

# ==================== HERO SECTION ====================
st.markdown("""
<div class="hero">
    <h1>📄 MarkItDown Converter</h1>
    <p>Konversi berbagai format file menjadi Markdown secara gratis untuk semua orang</p>
</div>
""", unsafe_allow_html=True)

# ==================== FEATURES ====================
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="icon">📘</div>
        <h3>Word</h3>
        <p>DOC, DOCX</p>
    </div>
    <div class="feature-card">
        <div class="icon">📊</div>
        <h3>Excel</h3>
        <p>XLS, XLSX</p>
    </div>
    <div class="feature-card">
        <div class="icon">📽️</div>
        <h3>PowerPoint</h3>
        <p>PPT, PPTX</p>
    </div>
    <div class="feature-card">
        <div class="icon">🌐</div>
        <h3>HTML & Web</h3>
        <p>HTML, HTM</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="icon">📝</div>
        <h3>Teks & Data</h3>
        <p>TXT, CSV, JSON, XML</p>
    </div>
    <div class="feature-card">
        <div class="icon">📚</div>
        <h3>EPUB</h3>
        <p>E-book format</p>
    </div>
    <div class="feature-card">
        <div class="icon">🗜️</div>
        <h3>ZIP</h3>
        <p>Arsip terkompresi</p>
    </div>
    <div class="feature-card">
        <div class="icon">📄</div>
        <h3>PDF</h3>
        <p>*terbatas di cloud gratis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== UPLOAD SECTION ====================
st.markdown("""
<div class="upload-section">
    <h2>📤 Upload File Anda</h2>
    <p>Pilih file dan klik tombol konversi di bawah</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Pilih file",
    type=ALL_EXTENSIONS,
    label_visibility="collapsed",
)

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    is_limited = file_ext in LIMITED_FORMATS

    if is_limited:
        st.markdown(f"""
        <div class="warning-box">
            <b>⚠️ Perhatian:</b> Format {file_ext.upper()} — {LIMITED_FORMATS[file_ext]}
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="result-box">
            <strong>📁 {uploaded_file.name}</strong><br>
            Ukuran: {uploaded_file.size / 1024:.2f} KB | Tipe: {uploaded_file.type or 'Tidak diketahui'}
        </div>
        """, unsafe_allow_html=True)

    convert_clicked = st.button("🔄 Konversi ke Markdown", type="primary", use_container_width=True)

    if convert_clicked:
        try:
            with st.spinner("Sedang mengonversi..."):
                file_bytes = uploaded_file.read()

                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
                    tmp_file.write(file_bytes)
                    tmp_path = tmp_file.name

                try:
                    result = converter.convert(tmp_path)
                    markdown_text = result.text_content

                    st.markdown("""
                    <div class="success-box">
                        ✅ Konversi berhasil!
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("## 📝 Hasil Markdown")
                    st.text_area(
                        "Konten",
                        value=markdown_text,
                        height=500,
                        key="markdown_output",
                        label_visibility="collapsed",
                    )

                    st.download_button(
                        label="⬇️ Unduh File Markdown",
                        data=markdown_text.encode("utf-8"),
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

                    st.markdown("### 📊 Statistik")
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.markdown(f"""
                        <div class="stat-card">
                            <span class="stat-value">{len(markdown_text):,}</span>
                            <span class="stat-label">Karakter</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <span class="stat-value">{len(markdown_text.split()):,}</span>
                            <span class="stat-label">Kata</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with s3:
                        st.markdown(f"""
                        <div class="stat-card">
                            <span class="stat-value">{markdown_text.count(chr(10)) + 1:,}</span>
                            <span class="stat-label">Baris</span>
                        </div>
                        """, unsafe_allow_html=True)

                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

        except Exception as e:
            st.error(f"❌ Kesalahan: {str(e)}")
            st.info("Coba format lain seperti DOCX, XLSX, PPTX, HTML, TXT, CSV, JSON, XML.")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    Dibuat dengan ❤️ menggunakan <a href="https://streamlit.io" target="_blank" style="color: #667eea;">Streamlit</a> dan 
    <a href="https://github.com/microsoft/markitdown" target="_blank" style="color: #667eea;">Microsoft MarkItDown</a>.<br>
    Deploy gratis di <a href="https://streamlit.io/cloud" target="_blank" style="color: #667eea;">Streamlit Community Cloud</a>.<br>
    Semoga bermanfaat dan menjadi pahala bagi kita semua. Amin. 🤲
</div>
""", unsafe_allow_html=True)
</style>
""", unsafe_allow_html=True)
