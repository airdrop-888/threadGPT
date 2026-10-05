# ThreadsGPT - Quick Start Guide

## 🚀 Installation (5 Minutes!)

### Step 1: Install Dependencies
```bash
pip install requests pyyaml apscheduler rich click
```

### Step 2: Get Your Cookies
1. Buka Threads.com di browser
2. Login ke akun Anda
3. Tekan **F12** untuk buka DevTools
4. Klik tab **Application**
5. Di sidebar kiri, klik **Cookies** > **https://www.threads.com**
6. Copy nilai dari cookies ini:
   - `sessionid`
   - `csrftoken`
   - `ds_user_id`

### Step 3: Setup Configuration
1. Copy file `config.example.yaml` → `config.yaml`
2. Edit `config.yaml` dan isi:
   ```yaml
   account:
     username: "username_anda"
     
   cookies:
     sessionid: "paste_sessionid_disini"
     csrftoken: "paste_csrftoken_disini"
     ds_user_id: "paste_ds_user_id_disini"
   ```

### Step 4: Run!
```bash
# Lihat analytics
python main.py analytics

# Schedule post
python main.py post "Konten thread anda" --time 19:00
```

---

## 📝 Quick Commands

### Schedule Posts
```bash
# Post pada waktu tertentu
python main.py post "Your content" --time 19:00

# Post otomatis di waktu terbaik
python main.py post "Your content" --time auto

# Post dengan gambar
python main.py post "Your content" --media path/to/image.jpg
```

### View Schedule
```bash
python main.py schedule
```

### Analytics
```bash
python main.py analytics --days 7
```

---

## ⚙️ Configuration

Edit `config.yaml` untuk customize:

```yaml
# Posting Schedule
scheduler:
  timezone: "Asia/Jakarta"
  posting_times:
    - "09:00"  # Pagi
    - "12:00"  # Siang
    - "19:00"  # Sore
    - "21:00"  # Malam

# Safety Limits
limits:
  posts_per_day: 5
  min_delay_hours: 2

# Your Niche
niche:
  keywords:
    - "AI"
    - "Tech"
    - "Programming"
  target_audience: "Tech enthusiasts"
```

---

## 🎯 Common Use Cases

### 1. Schedule Week of Content
```bash
python main.py post "Monday content" --time "2024-10-07 09:00"
python main.py post "Tuesday content" --time "2024-10-08 19:00"
python main.py post "Wednesday content" --time "2024-10-09 21:00"
```

### 2. Auto-Post at Best Times
```bash
python main.py post "Your content" --time auto
```

### 3. Track Performance
```bash
python main.py analytics
```

---

## ⚠️ Important Notes

- **Cookies expire**: Re-copy cookies setiap 30-60 hari
- **Rate limits**: Jangan post lebih dari 5x sehari
- **Use responsibly**: Tool ini untuk personal use only

---

## 🆘 Troubleshooting

**Problem**: "Session file not found"
**Solution**: Copy cookies dulu dari browser

**Problem**: "Invalid session"
**Solution**: Cookies expired, copy yang baru

**Problem**: "Rate limited"
**Solution**: Tunggu beberapa jam, jangan spam

---

## 🎉 That's It!

ThreadsGPT siap digunakan! Mulai schedule posts Anda sekarang!
