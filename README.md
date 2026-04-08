# 🚀 Data Security API (Python & MongoDB)

Selamat datang! Repositori ini berisi sistem API untuk keamanan data yang dibangun menggunakan **FastAPI** dan **MongoDB**. Panduan ini dibuat untuk membantu Anda menyiapkan lingkungan kerja (environment) agar aplikasi bisa berjalan di komputer masing-masing.

---

## 🛠️ Persiapan Awal
Sebelum memulai, pastikan Anda sudah menginstal:
1. **Python** (Versi 3.9 atau yang lebih baru).
2. **MongoDB** (Pastikan layanan MongoDB sudah aktif di komputer Anda).
3. **VS Code** (Sangat disarankan untuk mengedit dan menjalankan kode).

---

## 💻 Langkah-Langkah Instalasi

Ikuti langkah-langkah di bawah ini secara berurutan menggunakan Terminal di VS Code atau Command Prompt:

### 1. Membuat Lingkungan Virtual (Virtual Environment)
Langkah ini penting agar pustaka (library) aplikasi ini tersimpan rapi dalam satu folder dan tidak mengganggu sistem Python utama di komputer Anda.

* **Buat folder virtual:**
    ```bash
    python -m venv venv
    ```
* **Aktifkan folder tersebut:**
    * **Windows:** 
    ```bash
    .\venv\Scripts\activate
    ```
    * **Linux/Mac:** 
    ```bash
    source venv/bin/activate
    ```

> **Ciri Berhasil:** Jika berhasil, akan muncul tanda `(venv)` di bagian depan baris perintah terminal Anda.

### 2. Instalasi Library (Requirements)
Setelah folder virtual aktif, instal semua alat yang dibutuhkan dengan perintah berikut:

```bash
pip install -r requirement.txt