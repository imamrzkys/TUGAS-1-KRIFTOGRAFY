# 🔐 Aplikasi Web Simulasi Kriptografi Klasik

> **TUGAS 1 KRIPTOGRAFI** · Semester 6 · Tahun Ajaran 2025/2026 Genap

---

## 📋 Deskripsi

Aplikasi web interaktif untuk mempelajari dan mensimulasikan **5 algoritma kriptografi klasik**. Dibangun dengan **Flask (Python)** dan mengusung tema premium **"Aurora Glass Cryptography Lab"** dengan tampilan glassmorphism, animasi aurora, dan desain responsif.

Setiap algoritma menampilkan:
- Proses enkripsi **dan** dekripsi
- **Step-by-step calculation** per karakter/blok
- **Rumus matematis** yang digunakan
- **Visualisasi matriks dan tabel** (Hill & Playfair)
- Riwayat operasi tersimpan dalam **session history**

---

## ✨ Fitur Utama

| Fitur | Keterangan |
|---|---|
| 5 Cipher Klasik | Caesar, Vigenere, Affine, Hill, Playfair |
| Enkripsi & Dekripsi | Untuk semua algoritma |
| Step-by-step | Detail kalkulasi per karakter / blok |
| Formula Matematis | Rumus ditampilkan dengan jelas |
| Matrix Visualization | Hill 2×2/3×3 + Invers modulo 26 |
| Playfair 5×5 Table | Grid interaktif dengan hover effect |
| History | 20 riwayat tersimpan di session |
| Dark/Light Mode | Tersimpan di localStorage |
| Copy Result | Clipboard API + fallback |
| Validasi Input | Error message ramah pengguna |
| Responsive UI | Mobile 360px – Desktop 4K |
| Aurora Glass Theme | Glassmorphism + animated gradient |

---

## 🔑 Algoritma yang Tersedia

### 1. Caesar Cipher
- **Enkripsi:** `C = (P + k) mod 26`
- **Dekripsi:** `P = (C - k) mod 26`
- Kunci: angka shift 1–25

### 2. Vigenere Cipher
- **Enkripsi:** `C_i = (P_i + K_i) mod 26`
- **Dekripsi:** `P_i = (C_i - K_i) mod 26`
- Kunci: kata kunci (keyword) huruf A–Z

### 3. Affine Cipher
- **Enkripsi:** `C = (a·P + b) mod 26`
- **Dekripsi:** `P = a⁻¹·(C - b) mod 26`
- Kunci: integer `a` (coprime dengan 26) dan `b`

### 4. Hill Cipher
- **Enkripsi:** `C = K × P (mod 26)`
- **Dekripsi:** `P = K⁻¹ × C (mod 26)`
- Kunci: matriks 2×2 atau 3×3 yang invertibel modulo 26

### 5. Playfair Cipher
- Grid 5×5 dari keyword (J = I)
- Aturan: same row, same column, rectangle
- Kunci: kata kunci (keyword) huruf

---

## 🛠 Teknologi

- **Backend:** Python 3, Flask, Werkzeug
- **Templating:** Jinja2
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **UI Framework:** Bootstrap 5 (CDN)
- **Icons:** Font Awesome 6 (CDN)
- **Fonts:** Google Fonts (Outfit, JetBrains Mono)
- **Deployment:** Gunicorn

---

## 📁 Struktur Folder

```
TUGAS-1-KRIPTOGRAFI/
├── app.py                    # Entry point Flask
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment (Koyeb/Heroku)
├── README.md
├── .gitignore
├── test_ciphers.py           # Unit tests semua cipher
│
├── ciphers/                  # Modul algoritma (modular)
│   ├── __init__.py
│   ├── caesar.py
│   ├── vigenere.py
│   ├── affine.py
│   ├── hill.py
│   └── playfair.py
│
├── templates/                # HTML Jinja2
│   ├── base.html
│   ├── index.html
│   ├── history.html
│   └── partials/
│       ├── result_card.html
│       ├── steps.html
│       └── matrix_table.html
│
└── static/                   # Aset statis
    ├── css/
    │   └── style.css         # Aurora Glass custom CSS
    ├── js/
    │   └── main.js           # JavaScript frontend
    └── img/
        └── .gitkeep
```

---

## 🚀 Cara Menjalankan Lokal

### 1. Clone Repository
```bash
git clone https://github.com/imamrzkys/TUGAS-1-KRIFTOGRAFY.git
cd TUGAS-1-KRIFTOGRAFY
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
```

### 3. Aktivasi Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
```bash
python app.py
```

### 6. Buka di Browser
```
http://127.0.0.1:5000
```

---

## 🧪 Cara Menjalankan Test

```bash
python test_ciphers.py
```

Atau dengan unittest verbose:
```bash
python -m unittest test_ciphers -v
```

**43 test case** mencakup semua algoritma: encrypt, decrypt, roundtrip, validasi input, edge case.

---

## ☁️ Deploy ke Koyeb

### Persiapan

Pastikan file berikut ada di root project:
- `requirements.txt` (berisi Flask + gunicorn)
- `Procfile` (berisi perintah run gunicorn)

### Langkah Deploy

1. **Push ke GitHub:**
   ```bash
   git add .
   git commit -m "feat: Flask + Jinja2 cryptography lab"
   git push origin main
   ```

2. **Buka [Koyeb](https://app.koyeb.com)** → Login

3. **Create Web Service:**
   - Pilih **GitHub** sebagai sumber
   - Pilih repository Anda

4. **Konfigurasi Build:**
   - Build type: **Buildpack** (otomatis deteksi Python)
   - Atau gunakan Dockerfile jika tersedia

5. **Run Command:**
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
   ```

6. **Environment Variables:**
   | Variable | Value |
   |---|---|
   | `SECRET_KEY` | *(string acak panjang)* |
   | `FLASK_DEBUG` | `0` |
   | `PORT` | *(otomatis dari Koyeb)* |

7. **Deploy!** Koyeb akan build dan deploy otomatis.

### Jalankan dengan Gunicorn Lokal (untuk verifikasi)
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

---

## ✅ Catatan Validasi Algoritma

| Algoritma | Aturan Kunci |
|---|---|
| **Caesar** | Shift: angka **1–25** |
| **Vigenere** | Keyword: **hanya huruf** A–Z |
| **Affine** | `a` harus **coprime dengan 26** · Valid: 1,3,5,7,9,11,15,17,19,21,23,25 |
| **Hill** | det(K) mod 26 **≠ 0** dan **coprime 26** · Matriks 2×2 atau 3×3 |
| **Playfair** | Keyword: **hanya huruf** A–Z · J digabung I |

**Catatan umum:**
- Teks tidak boleh kosong
- Spasi dan tanda baca dipertahankan (kecuali Hill & Playfair yang hanya proses huruf)
- Hill & Playfair otomatis menambahkan padding `X` jika diperlukan

---

## 📸 Screenshot

![Screenshot Aplikasi](static/img/screenshot.png)

*(Tambahkan screenshot aplikasi ke `static/img/screenshot.png`)*

---

## 👤 Identitas Tugas

| | |
|---|---|
| **Mata Kuliah** | Kriptografi |
| **Tugas** | Tugas 1 |
| **Semester** | 6 |
| **Tahun Ajaran** | 2025/2026 Genap |
