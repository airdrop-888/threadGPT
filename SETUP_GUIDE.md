# 📖 Setup Guide - Panduan Lengkap ThreadsGPT

## 🎯 Total Waktu: 5 Menit!

---

## 📋 Step 1: Install Dependencies (1 menit)

Buka Command Prompt atau PowerShell, ketik:

```bash
pip install requests pyyaml apscheduler rich click
```

Tunggu sampai selesai install.

---

## 🍪 Step 2: Get Cookies dari Browser (2 menit)

### A. Buka Threads.com
1. Buka browser (Chrome/Edge/Firefox)
2. Pergi ke **https://threads.com**
3. **Login** ke akun Threads Anda

### B. Buka Developer Tools
1. Tekan tombol **F12** di keyboard
   - Atau klik kanan → Inspect
   - Atau Menu → More Tools → Developer Tools

2. Akan muncul panel DevTools di bagian bawah/samping

### C. Buka Tab Application
1. Di DevTools, klik tab **Application** (paling atas)
   - Kalau tidak ada, cari icon >> untuk show more tabs

2. Di sidebar kiri, cari **Storage** section

3. Expand **Cookies**

4. Klik **https://www.threads.com**

### D. Copy Cookies
Anda akan lihat tabel dengan banyak cookies. Copy 3 nilai ini:

1. **sessionid**
   - Cari row dengan Name: `sessionid`
   - Double-click pada kolom Value
   - Ctrl+A (select all) → Ctrl+C (copy)
   - Paste ke Notepad sementara
   - Contoh: `23675880534%3AHVYXwuyuQBdgRF%3A7%3AAYkM...`

2. **csrftoken**
   - Cari row dengan Name: `csrftoken`
   - Copy Value-nya
   - Contoh: `YRmsDfbny6CArRArlhlJiBlPa7f9Q8S0`

3. **ds_user_id**
   - Cari row dengan Name: `ds_user_id`
   - Copy Value-nya
   - Contoh: `23675880534`

**TIPS**: Simpan dulu 3 nilai ini di Notepad!

---

## ⚙️ Step 3: Setup Config File (2 menit)

### A. Copy Config Template

**Cara 1 - Via Command Prompt:**
```bash
cd "C:\Users\Admin\Documents\MARIO\PROJECT\List BOT\autoThreader"
copy config.example.yaml config.yaml
```

**Cara 2 - Manual:**
1. Buka folder ThreadsGPT
2. Klik kanan pada `config.example.yaml`
3. Pilih **Copy**
4. Klik kanan di folder yang sama
5. Pilih **Paste**
6. Rename file hasil copy menjadi `config.yaml`

### B. Edit Config File

**Buka config.yaml:**
```bash
notepad config.yaml
```

Atau:
- Klik kanan `config.yaml`
- Pilih "Edit with Notepad" atau "Open with VSCode"

### C. Paste Cookies

Cari bagian ini di file (sekitar baris 17-20):

```yaml
cookies:
  sessionid: ""  # Paste sessionid disini
  csrftoken: ""  # Paste csrftoken disini
  ds_user_id: ""  # Paste ds_user_id disini
```

**UBAH MENJADI** (paste nilai dari Notepad Anda):

```yaml
cookies:
  sessionid: "23675880534%3AHVYXwuyuQBdgRF%3A7%3AAYkMSOZ"
  csrftoken: "YRmsDfbny6CArRArlhlJiBlPa7f9Q8S0"
  ds_user_id: "23675880534"
```

⚠️ **PENTING**: 
- Tetap ada tanda petik `" "`
- Jangan ada spasi ekstra
- Paste HANYA nilai cookie-nya

### D. (Optional) Customize Settings

Scroll ke bawah untuk ubah:

**Username Anda:**
```yaml
account:
  username: "username_anda"  # Ganti dengan username Threads Anda
```

**Timezone:**
```yaml
scheduler:
  timezone: "Asia/Jakarta"  # Sesuaikan timezone Anda
```

**Waktu Posting:**
```yaml
posting_times:
  - "09:00"  # Ubah sesuai keinginan
  - "12:00"
  - "19:00"  # Biasanya paling ramai
  - "21:00"
```

### E. Save File

- Tekan **Ctrl+S** untuk save
- Atau File → Save
- Tutup Notepad

---

## ✅ Step 4: Test Setup (1 menit)

Buka Command Prompt di folder ThreadsGPT:

```bash
cd "C:\Users\Admin\Documents\MARIO\PROJECT\List BOT\autoThreader"
python setup_cookies.py
```

**Jika BERHASIL**, Anda akan lihat:
```
============================================================
ThreadsGPT - Simple Cookie Loader
============================================================
[OK] Cookies loaded successfully!
[OK] User: username_anda

[SUCCESS] Ready to use ThreadsGPT!
```

**Jika GAGAL**, akan ada pesan error yang jelas:
- Missing cookies → Cek config.yaml, pastikan sudah paste
- Invalid config → Cek syntax YAML (indentasi, quotes)

---

## 🚀 Step 5: Start Using!

### Schedule Post Pertama Anda:

```bash
python main.py post "Hello from ThreadsGPT! 🚀" --time 19:00
```

### Lihat Status:

```bash
python main.py status
```

### Lihat Schedule:

```bash
python main.py schedule
```

---

## 🎯 RECAP - Apa yang Harus Dilakukan:

1. ✅ Install dependencies → `pip install ...`
2. ✅ Buka threads.com → Login
3. ✅ Tekan F12 → Tab Application → Cookies
4. ✅ Copy 3 cookies: sessionid, csrftoken, ds_user_id
5. ✅ Copy `config.example.yaml` → `config.yaml`
6. ✅ Edit `config.yaml` → Paste 3 cookies
7. ✅ Save file
8. ✅ Test: `python setup_cookies.py`
9. ✅ Done! Start scheduling posts!

---

## 🆘 Troubleshooting

### "Config file not found"
**Problem**: File `config.yaml` belum dibuat

**Solution**: 
```bash
copy config.example.yaml config.yaml
```

### "Missing cookies"
**Problem**: Cookies belum di-paste atau masih kosong

**Solution**: 
1. Buka `config.yaml`
2. Cek bagian cookies
3. Pastikan ada nilai di dalam `" "`
4. Jangan lupa save!

### "Invalid session"
**Problem**: Cookies salah atau expired

**Solution**:
1. Buka threads.com lagi
2. F12 → Get cookies baru
3. Paste cookies baru ke config.yaml

### "Can't find sessionid"
**Problem**: Mungkin belum login

**Solution**:
1. Pastikan sudah login ke threads.com
2. Refresh page (F5)
3. F12 lagi → Cookies harus muncul

---

## 💡 TIPS

### Cookies Expire
- Cookies bertahan 30-60 hari
- Kalau error "invalid session" = get cookies baru
- Simpan cookies di Notepad untuk backup

### Security
- **JANGAN** share cookies dengan orang lain!
- Cookies = akses ke akun Anda
- Simpan `config.yaml` di tempat aman

### Multiple Accounts
Untuk manage multiple accounts:
1. Buat folder terpisah untuk tiap akun
2. Copy ThreadsGPT ke folder baru
3. Setup config.yaml dengan cookies berbeda

---

## 📞 Butuh Bantuan?

- 📺 **YouTube**: [Link tutorial video]
- 💬 **GitHub Issues**: [Report problems]
- 📖 **README.md**: Dokumentasi lengkap

---

**Selamat! Anda siap menggunakan ThreadsGPT! 🎉**
