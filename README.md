# MarkItDown Converter 📄

Aplikasi web gratis untuk mengonversi berbagai format file menjadi **Markdown** menggunakan [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

Dibuat untuk manfaat bersama — gratis untuk semua orang, di-deploy melalui [Streamlit Community Cloud](https://streamlit.io/cloud).

## Format yang Didukung

| Kategori | Format |
|----------|--------|
| Dokumen | PDF, Word (DOC/DOCX), PowerPoint (PPT/PPTX), Excel (XLS/XLSX) |
| Web & Teks | HTML, TXT, CSV, JSON, XML, EPUB |
| Arsip | ZIP |
| Gambar | PNG, JPG, WEBP, BMP (EXIF metadata) |
| Audio | MP3, WAV, M4A, OGG (metadata) |

## Cara Deploy ke Streamlit Community Cloud (Gratis)

1. **Buat akun GitHub** jika belum punya: https://github.com
2. **Push kode ini ke repositori GitHub publik**
3. **Buka Streamlit Community Cloud**: https://streamlit.io/cloud
4. **Login dengan GitHub**, lalu klik "New app"
5. Pilih repositori, branch, dan file utama: `app.py`
6. Klik **Deploy**

Aplikasi akan online di URL seperti: https://markitdown-app.streamlit.app

## Struktur Proyek

```
markitdown-app/
├── app.py                 # Aplikasi Streamlit utama
├── requirements.txt       # Dependensi Python
├── .streamlit/
│   └── config.toml        # Konfigurasi Streamlit
└── README.md              # Panduan ini
```

## Catatan Penting

- Streamlit Community Cloud gratis hanya untuk **repositori publik**
- Aplikasi akan tidur (sleep) setelah beberapa waktu tidak diakses, dan akan otomatis nyala kembali ketika ada pengunjung
- Fitur OCR gambar dan transkripsi audio memerlukan dependensi sistem (Tesseract, FFmpeg) yang tidak tersedia di Streamlit Cloud gratis. Konversi dokumen dan teks tetap berjalan normal.
- Ukuran file upload maksimal sekitar 200 MB

## Lisensi

Open source untuk manfaat bersama.

Semoga bermanfaat dan menjadi pahala bagi kita semua. Amin. 🤲
