# 📅 Bulk Schedule Guide - Schedule Banyak Posts Sekaligus

## 🎯 Keuntungan Bulk Schedule

- ⏱️ **Hemat Waktu** - Schedule 50+ posts dalam 5 menit!
- 📊 **Organized** - Plan konten dalam spreadsheet
- 🔄 **Reusable** - Simpan template untuk bulan depan
- ✅ **Easy Review** - Lihat semua konten sebelum schedule

---

## 📝 Format CSV

### Columns (5 kolom):

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `date` | ✅ Yes | Tanggal posting | `2024-10-07` |
| `time` | ✅ Yes | Jam posting | `19:00` |
| `content` | ✅ Yes | Isi konten thread | `"Hello World!"` |
| `media` | ❌ No | Path ke gambar/video | `image.jpg` |
| `hashtags` | ❌ No | Hashtags (pisah dengan spasi) | `tech AI coding` |

---

## 🚀 Cara Menggunakan

### Step 1: Buat File CSV

**Option A - Copy Template:**
```bash
copy schedule.example.csv my_schedule.csv
```

**Option B - Buat Baru di Excel/Google Sheets:**

1. Buat spreadsheet baru
2. Buat 5 kolom dengan header:
   ```
   date | time | content | media | hashtags
   ```
3. Isi data
4. Save as CSV (File → Save As → CSV)

### Step 2: Isi Data

**Contoh di Excel:**

| date | time | content | media | hashtags |
|------|------|---------|-------|----------|
| 2024-10-07 | 09:00 | Good morning! 🌅 | | motivation |
| 2024-10-07 | 19:00 | Evening update 🌙 | sunset.jpg | photo evening |
| 2024-10-08 | 12:00 | Lunch time tips! 💡 | | tips productivity |

**Tips:**
- Gunakan quotes `" "` untuk content yang panjang
- Date format: `YYYY-MM-DD`
- Time format: `HH:MM` (24 jam)
- Hashtags: pisah dengan spasi (auto tambah `#`)

### Step 3: Run Bulk Schedule

```bash
python bulk_schedule.py my_schedule.csv
```

### Step 4: Review & Confirm

Script akan show preview:
```
============================================================
Preview:
============================================================
1. 2024-10-07 09:00 - Good morning! 🌅
2. 2024-10-07 19:00 - Evening update 🌙
3. 2024-10-08 12:00 - Lunch time tips! 💡
... and 7 more

============================================================
Schedule these posts? (yes/no):
```

Ketik `yes` untuk confirm!

### Step 5: Done!

```
============================================================
Summary
============================================================
[OK] Successfully scheduled: 10
[ERROR] Failed: 0

Next steps:
  python main.py schedule  # View all scheduled posts
```

---

## 📋 Template Examples

### 1. Weekly Content Plan

```csv
date,time,content,media,hashtags
2024-10-07,09:00,"Monday Motivation! 💪",,,motivation monday
2024-10-08,09:00,"Tech Tuesday Tips 🚀",,,tech tips
2024-10-09,09:00,"Wednesday Wisdom 💡",,,wisdom
2024-10-10,09:00,"Throwback Thursday 📸",,,throwback
2024-10-11,09:00,"Friday Feeling 🎉",,,friday weekend
```

### 2. Product Launch Campaign

```csv
date,time,content,media,hashtags
2024-10-07,10:00,"Big announcement coming! 👀",teaser.jpg,announcement
2024-10-08,10:00,"Countdown: 2 days! ⏰",countdown.jpg,launch
2024-10-09,10:00,"Countdown: 1 day! 🔥",countdown2.jpg,launch
2024-10-10,10:00,"It's LIVE! 🚀 Check it out",product.jpg,launch newproduct
2024-10-11,10:00,"Thank you for the support! ❤️",,thankyou
```

### 3. Educational Series

```csv
date,time,content,media,hashtags
2024-10-07,14:00,"Thread series: AI Basics (1/5) 🤖",,,AI education
2024-10-08,14:00,"Thread series: Machine Learning (2/5) 📊",chart.jpg,AI ML
2024-10-09,14:00,"Thread series: Neural Networks (3/5) 🧠",diagram.jpg,AI deeplearning
2024-10-10,14:00,"Thread series: Applications (4/5) 💡",,,AI tech
2024-10-11,14:00,"Thread series: Future of AI (5/5) 🚀",,,AI future
```

---

## 🎨 Excel Tips

### Format Cells:
1. **Date column** → Format: `YYYY-MM-DD`
2. **Time column** → Format: `HH:MM` (24-hour)
3. **Content column** → Text (allow multi-line with Alt+Enter)

### Use Formulas:
```excel
# Auto-generate dates (drag down)
=A2+1

# Auto-generate times
=TIME(9,0,0)  # 09:00
=TIME(19,0,0) # 19:00
```

### Color Coding:
- 🟢 Green = Scheduled
- 🟡 Yellow = Pending review
- 🔴 Red = Needs edit

---

## ⚠️ Common Issues

### "Invalid date/time format"
**Problem**: Date atau time format salah

**Solution**: 
- Date: `YYYY-MM-DD` (e.g., `2024-10-07`)
- Time: `HH:MM` (e.g., `19:00`)
- Jangan tambah detik atau AM/PM

### "Missing content"
**Problem**: Content kosong atau missing quotes

**Solution**:
- Pastikan ada isi di kolom content
- Gunakan quotes untuk content panjang: `"Content here"`

### "File encoding error"
**Problem**: CSV encoding salah

**Solution**:
- Save CSV dengan encoding UTF-8
- Excel: Save As → CSV UTF-8

### "Daily limit reached"
**Problem**: Terlalu banyak posts di satu hari

**Solution**:
- Check `config.yaml` → `posts_per_day` limit
- Spread posts ke beberapa hari

---

## 💡 Pro Tips

### 1. Plan Monthly Content
```bash
# Buat folder untuk tiap bulan
mkdir October_2024
# Simpan CSV per week
schedule_week1.csv
schedule_week2.csv
...
```

### 2. Use Templates
Simpan template untuk recurring content:
- `template_weekly.csv` - Weekly series
- `template_product.csv` - Product launches
- `template_tips.csv` - Daily tips

### 3. Batch Review
- Plan content di weekend
- Schedule untuk whole week
- Review analytics di Friday

### 4. Content Calendar
Use Google Sheets untuk:
- Collaborate dengan team
- Track post performance
- Plan ahead dengan color coding

---

## 📊 Example Workflow

### Monday Morning (10 minutes):
1. Buka `content_ideas.txt` (ide yang sudah dikumpulkan)
2. Buat `week_schedule.csv` di Excel
3. Isi 10-15 posts untuk seminggu
4. Run: `python bulk_schedule.py week_schedule.csv`
5. Done! Autopilot untuk seminggu 🎉

### Friday Afternoon (5 minutes):
1. Check analytics: `python main.py analytics`
2. Note what worked
3. Plan next week content based on insights

---

## 🎯 Advanced: Google Sheets Integration

Want to schedule directly from Google Sheets?

1. Export Sheets to CSV (File → Download → CSV)
2. Or use Google Sheets API (coming soon!)

---

## 📞 Need Help?

- 📖 See: `SETUP_GUIDE.md`
- 💬 Issues: GitHub Issues
- 📺 Tutorial: [YouTube Link]

---

**Happy Bulk Scheduling! 🚀**

*Plan once, post automatically all week!*
