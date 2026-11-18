import streamlit as st
from markitdown import MarkItDown
import io
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="MarkItDown Converter",
    page_icon="📄",
    layout="wide",
)

# Judul dan deskripsi
st.title("📄 MarkItDown Converter")
st.markdown("""
Konversi berbagai format file menjadi **Markdown** menggunakan [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

Dibuat untuk manfaat bersama — gratis untuk semua orang.  
*Semoga bermanfaat dan menjadi pahala bagi kita semua. Amin.*
""")

st.divider()

# Inisialisasi MarkItDown
@st.cache_resource
def get_converter():
    return MarkItDown(enable_plugins=False)

converter = get_converter()

# Format yang didukung
SUPPORTED_EXTENSIONS = [
    "pdf", "docx", "doc", "pptx", "ppt", "xlsx", "xls",
    "html", "htm", "txt", "csv", "json", "xml", "epub",
    "zip", "png", "jpg", "jpeg", "webp", "bmp",
    "mp3", "wav", "m4a", "ogg",
]

# Sidebar
with st.sidebar:
    st.header("📋 Format yang Didukung")
    st.markdown("""
    - **Dokumen:** PDF, Word (DOC/DOCX), PowerPoint (PPT/PPTX), Excel (XLS/XLSX)
    - **Web & Teks:** HTML, TXT, CSV, JSON, XML, EPUB
    - **Arsip:** ZIP
    - **Gambar:** PNG, JPG, WEBP, BMP (EXIF metadata)
    - **Audio:** MP3, WAV, M4A, OGG (metadata)
    """)
    st.info("""
    **Catatan:** Fitur OCR gambar dan transkripsi audio memerlukan dependensi sistem tambahan 
    (seperti Tesseract, FFmpeg) yang tidak tersedia di Streamlit Community Cloud gratis. 
    Konversi dokumen dan teks tetap berjalan normal.
    """)

# Area upload file
st.subheader("📤 Upload File")
uploaded_file = st.file_uploader(
    "Pilih file yang ingin dikonversi",
    type=SUPPORTED_EXTENSIONS,
    help="Maksimal ukuran file disesuaikan oleh Streamlit Cloud (biasanya ~200 MB)",
)

if uploaded_file is not None:
    # Tampilkan info file
    file_details = {
        "Nama": uploaded_file.name,
        "Tipe": uploaded_file.type,
        "Ukuran": f"{uploaded_file.size / 1024:.2f} KB",
    }
    st.json(file_details)

    # Tombol konversi
    if st.button("🔄 Konversi ke Markdown", type="primary"):
        try:
            with st.spinner("Sedang mengonversi file... mohon tunggu"):
                # Simpan file upload ke temporary buffer
                file_bytes = uploaded_file.read()
                
                # Buat temporary file karena markitdown membutuhkan path file
                import tempfile
                with tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix=f".{uploaded_file.name.split('.')[-1]}"
                ) as tmp_file:
                    tmp_file.write(file_bytes)
                    tmp_path = tmp_file.name

                try:
                    # Konversi menggunakan markitdown
                    result = converter.convert(tmp_path)
                    markdown_text = result.text_content

                    # Tampilkan hasil
                    st.success("✅ Konversi berhasil!")
                    st.divider()

                    st.subheader("📝 Hasil Markdown")
                    st.text_area(
                        "Konten Markdown",
                        value=markdown_text,
                        height=400,
                        key="markdown_output",
                    )

                    # Tombol unduh
                    st.download_button(
                        label="⬇️ Unduh file Markdown",
                        data=markdown_text.encode("utf-8"),
                        file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.md",
                        mime="text/markdown",
                        type="secondary",
                    )

                    # Statistik
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Karakter", len(markdown_text))
                    with col2:
                        st.metric("Kata", len(markdown_text.split()))
                    with col3:
                        st.metric("Baris", markdown_text.count("\n") + 1)

                finally:
                    # Bersihkan temporary file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat konversi: {str(e)}")
            st.info("Coba pastikan file tidak rusak dan format didukung.")

# Footer
st.divider()
st.markdown("""
---
Dibuat dengan ❤️ menggunakan [Streamlit](https://streamlit.io) dan [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

Deploy gratis di [Streamlit Community Cloud](https://streamlit.io/cloud).  
Kode sumber tersedia di GitHub untuk manfaat bersama.
""")
