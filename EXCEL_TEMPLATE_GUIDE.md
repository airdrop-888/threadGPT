# 📋 Schedule Template - Excel Formatted

## 🎨 For Best Experience in Excel:

### After opening in Excel:

**1. Format Header Row (Row 1):**
- Select Row 1
- Font: Bold
- Fill Color: Blue (or your choice)
- Text Color: White
- Font Size: 12

**2. Format Date Column (Column A):**
- Select Column A
- Right-click → Format Cells
- Category: Date
- Type: YYYY-MM-DD

**3. Format Time Column (Column B):**
- Select Column B  
- Right-click → Format Cells
- Category: Time
- Type: HH:MM (24-hour)

**4. Format Content Column (Column C):**
- Select Column C
- Width: Wider (30-40)
- Wrap Text: ON

**5. Auto-size All Columns:**
- Select All (Ctrl+A)
- Double-click column border to auto-fit

---

## 📝 Column Descriptions:

| Column | Format | Example | Required |
|--------|--------|---------|----------|
| **date** | YYYY-MM-DD | 2024-10-07 | ✅ Yes |
| **time** | HH:MM | 19:00 | ✅ Yes |
| **content** | Text | Your post content | ✅ Yes |
| **media** | Filename | image.jpg | ❌ Optional |
| **hashtags** | Space separated | tech AI coding | ❌ Optional |

---

## 🎨 Color Coding Ideas (Optional):

**By Status:**
- 🟢 Green = Ready to post
- 🟡 Yellow = Needs review
- 🔴 Red = Draft/editing
- 🔵 Blue = Posted

**By Category:**
- 🟣 Purple = Promotional
- 🟠 Orange = Educational  
- 🟢 Green = Engagement
- 🔵 Blue = Personal

---

## 💡 Excel Pro Tips:

### Use Data Validation:
1. Select time column
2. Data → Data Validation
3. List: 09:00, 12:00, 19:00, 21:00
4. Now you can pick from dropdown!

### Use Formulas:
```excel
# Auto-generate next day
=A2+1

# Auto-generate same time
=B2

# Character count for content
=LEN(C2)
```

### Freeze Header:
1. Click on Row 2
2. View → Freeze Panes → Freeze Top Row
3. Header stays visible when scrolling!

---

## 📁 Save As Options:

### For ThreadsGPT:
**Save As: CSV UTF-8 (Recommended)**
- File → Save As
- Type: CSV UTF-8 (Comma delimited) (*.csv)

### For Backup:
**Save As: Excel Workbook (*.xlsx)**
- Keeps formatting
- Can edit later with colors
- When ready, export to CSV

---

## ⚠️ Important Notes:

### Content Column:
- Remove or escape commas: "Hello, World" → Hello World
- Remove emoji if Excel shows weird characters
- Keep under 500 characters
- Use quotes if needed: "Content with, comma"

### Date/Time:
- Always use YYYY-MM-DD format for dates
- Always use HH:MM for times (24-hour)
- No AM/PM

### Media:
- Put filename only: image.jpg
- Put full path if needed: C:\photos\image.jpg
- Leave empty if no media

### Hashtags:
- Space separated: tech AI coding
- Script will auto-add # symbol
- Leave empty if no hashtags

---

## 🚀 Quick Start:

1. Open in Excel
2. Format header (blue background, white text)
3. Fill in your content
4. Save As: CSV UTF-8
5. Run: `python bulk_schedule.py your_file.csv`

---

**Happy Scheduling!** 📅
