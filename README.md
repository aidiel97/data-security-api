# 🚀 Data Security API (Python & MongoDB)

Selamat datang! Repositori ini berisi sistem API untuk keamanan data yang dibangun menggunakan **FastAPI** dan **MongoDB**. Panduan ini dibuat untuk membantu Anda menyiapkan lingkungan kerja (*environment*) agar aplikasi bisa berjalan di komputer masing-masing.

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
Langkah ini penting agar pustaka (*library*) aplikasi ini tersimpan rapi dalam satu folder dan tidak mengganggu sistem Python utama di komputer Anda.

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

> **💡 Ciri Berhasil:** Jika berhasil, akan muncul tanda `(venv)` di bagian depan baris perintah terminal Anda.

### 2. Instalasi Library (Requirements)
Setelah folder virtual aktif, instal semua alat yang dibutuhkan dengan perintah berikut:

```bash
pip install -r requirement.txt
```

---

## 🏃 Cara Menjalankan API
Setelah proses instalasi selesai, Anda bisa menjalankan server API dengan perintah:

```bash
uvicorn app.main:app --reload
```

Jika terminal menampilkan pesan `Uvicorn running on http://127.0.0.1:8000`, artinya server Anda sudah berjalan dengan sukses!

---

## 🔍 Cara Menguji API (Interaktif)
Salah satu keunggulan FastAPI adalah fitur dokumentasi otomatisnya. Anda tidak perlu aplikasi tambahan untuk mencoba API ini:

1. Buka browser (Chrome/Edge/Firefox).
2. Buka alamat: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Anda akan melihat halaman **Swagger UI**.
4. Pilih salah satu fungsi (*endpoint*), klik **"Try it out"**, lalu klik **"Execute"** untuk melihat hasilnya.

---

## 📁 Struktur Project
* **`app/`** : Folder utama yang berisi seluruh kode program.
* **`app/main.py`** : File utama untuk menjalankan aplikasi.
* **`requirement.txt`** : Daftar semua library Python yang digunakan.
* **`venv/`** : Folder lingkungan virtual (jangan diedit manual).

---

## 💡 Troubleshooting (Solusi Masalah)
* **Error "ModuleNotFoundError"**: Pastikan Anda sudah menjalankan perintah `activate` pada langkah nomor 1.
* **Error MongoDB Connection**: Pastikan aplikasi MongoDB Compass atau *service* MongoDB Anda sudah dalam posisi *Connected/Running*.
* **Script Execution Policy (Windows)**: Jika tidak bisa menjalankan `activate`, coba jalankan perintah ini di PowerShell (Run as Administrator):
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
```