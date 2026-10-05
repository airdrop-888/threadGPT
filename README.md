<div align="center">

# 🤖 ThreadsGPT

### *The Ultimate AI-Powered Threads Automation Engine*

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-ready-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Automate your Threads account. Schedule posts intelligently. Grow your audience effortlessly.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Support](#-support)

---

<img src="https://img.shields.io/badge/Threads-Automation-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads">
<img src="https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" alt="AI">
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">

</div>

---

## 🎯 What is ThreadsGPT?

ThreadsGPT is a **powerful automation tool** that helps you manage your Threads account like a pro. Schedule posts at optimal times, bulk-schedule weeks of content from CSV files, track engagement analytics, and detect viral content—all from your terminal.

**Built for creators, marketers, and developers** who want to **save time** and **grow faster** on Threads.

### ✨ Why ThreadsGPT?

- 🚀 **Dead Simple Setup** - 3 steps, 5 minutes. No HAR files, no complex configs.
- ⏰ **Smart Scheduling** - AI-powered optimal time detection
- 📊 **Bulk Schedule** - Upload 50+ posts from CSV in seconds
- 🔥 **Viral Detector** - Find trending content in your niche
- 💾 **Analytics Engine** - Track growth and engagement
- 🛡️ **Safe & Secure** - Built-in rate limiting, no account bans

---

## 🚀 Quick Start

### Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/airdrop-888/threadGPT.git
cd threadGPT

# Install dependencies
pip install -r requirements.txt
```

### Setup (3 minutes)

**1. Get Your Cookies**
- Open [threads.com](https://threads.com) and login
- Press **F12** → **Application** tab → **Cookies** → **threads.com**
- Copy: `sessionid`, `csrftoken`, `ds_user_id`

**2. Configure**
```bash
# Copy config template
copy config.example.yaml config.yaml

# Edit and paste your cookies
notepad config.yaml
```

**3. Test Setup**
```bash
python setup_cookies.py
```

**4. Test Your Setup** (Optional but Recommended!)
```bash
# Schedule a test post (will post in 2 minutes)
python test_post.py
```
This will schedule a test post to verify everything works! ✅

**5. Start Automating!**
```bash
# Schedule your first real post
python main.py post "Hello from ThreadsGPT! 🚀" --time 19:00

# View your schedule
python main.py schedule

# Check analytics
python main.py analytics
```

**That's it!** You're ready to automate Threads! 🎉

---

## ⚡ Features

<table>
<tr>
<td width="50%">

### 🤖 Smart Automation
- **Auto-Schedule** posts at optimal times
- **Queue Management** for weeks ahead
- **Retry Mechanism** for failed posts
- **Rate Limiting** to stay safe

</td>
<td width="50%">

### 📊 Analytics & Insights
- **Engagement Tracking** (likes, replies, reposts)
- **Follower Growth** monitoring
- **Best Time Detection** using AI
- **Performance Reports** export

</td>
</tr>
<tr>
<td>

### 📝 Bulk Operations
- **Excel & CSV Support** - Use .xlsx or .csv
- **Pre-formatted Template** - Run one command, get clean Excel
- **Media Support** (images, videos)
- **Hashtag Automation**

</td>
<td>

### 🔥 Viral Content
- **Trending Detector** find viral posts
- **Content Scoring** (0-10 viral score)
- **Pattern Analysis** what works in your niche
- **Competitor Tracking**

</td>
</tr>
</table>

---

## 📖 Documentation

### Basic Commands

```bash
# Schedule a post
python main.py post "Your content" --time 19:00

# Auto-detect best time
python main.py post "Your content" --time auto

# Schedule with image
python main.py post "Check this out!" --media photo.jpg --time 21:00

# View scheduled posts
python main.py schedule

# Check analytics
python main.py analytics --days 7

# System status
python main.py status
```

### Bulk Schedule from Excel (Recommended!) 📊

```bash
# Step 1: Generate pre-formatted Excel template
python create_excel_template.py

# Step 2: Open the file, fill in your posts (clean & structured!)
# → schedule_template.xlsx opens in Excel
# → Blue header, proper column widths, text wrapping
# → Instructions sheet included

# Step 3: Schedule all posts at once
python bulk_schedule.py schedule_template.xlsx
```

**Excel Template Preview:**

| date | time | content | media | hashtags |
|------|------|---------|-------|----------|
| 2024-10-07 | 09:00 | Good morning! Starting the week strong! | | motivation monday |
| 2024-10-07 | 19:00 | Evening update: Progress over perfection! | photo.jpg | motivation |
| 2024-10-08 | 12:00 | Quick tip: Automate repetitive tasks! | | productivity |

> 💡 **Tip**: Also supports `.csv` format → `python bulk_schedule.py schedule.csv`

### Configuration

Edit `config.yaml` to customize:

```yaml
# Posting times
scheduler:
  timezone: "Asia/Jakarta"
  posting_times:
    - "09:00"  # Morning
    - "12:00"  # Noon
    - "19:00"  # Evening (best!)
    - "21:00"  # Night

# Safety limits
limits:
  posts_per_day: 5        # Max posts per day
  min_delay_hours: 2      # Min gap between posts

# Your niche
niche:
  keywords:
    - "AI"
    - "Tech"
    - "Programming"
```

---

## 📚 Full Guides

- 📘 [**Setup Guide**](SETUP_GUIDE.md) - Detailed step-by-step setup
- 📗 [**Bulk Schedule Guide**](BULK_SCHEDULE_GUIDE.md) - Master CSV bulk scheduling
- 📙 [**Quick Start**](QUICKSTART.md) - Get started in 5 minutes
- 📕 [**Contributing**](CONTRIBUTING.md) - How to contribute

---

## 🎯 Use Cases

<details>
<summary><b>👨‍💼 For Content Creators</b></summary>

- Schedule a week of content in 10 minutes
- Auto-post at peak engagement times
- Track which posts perform best
- Never miss posting due to busy schedule

</details>

<details>
<summary><b>📈 For Marketers</b></summary>

- Plan campaigns weeks ahead
- A/B test different posting times
- Track competitor content
- Analyze what resonates with audience

</details>

<details>
<summary><b>💻 For Developers</b></summary>

- Learn automation & web scraping
- Extend with custom features
- Integrate with other tools
- Build on top of the API

</details>

<details>
<summary><b>🚀 For Side Hustlers</b></summary>

- Maintain presence while working full-time
- Grow personal brand on autopilot
- Schedule promotional content
- Save 10+ hours per week

</details>

---

## 🔥 Pro Tips

### 📅 Best Posting Times
- **Morning**: 9:00-10:00 AM (commute time)
- **Lunch**: 12:00-1:00 PM (lunch break)
- **Evening**: 7:00-9:00 PM ⭐ **(BEST!)**
- **Night**: 9:00-11:00 PM (relaxing time)

### 📝 Content That Works
- ✅ 100-280 characters (optimal length)
- ✅ 1-3 relevant hashtags
- ✅ Images = 2x more engagement
- ✅ Questions = more replies

### 🎯 Growth Strategy
1. Schedule posts for whole week on Monday
2. Use `--time auto` for optimal scheduling
3. Check analytics every Friday
4. Adjust based on what works

---

## ⚠️ Important Notes

### 🔐 Security
- **Keep your cookies secure** - Never share `config.yaml`
- **Cookies expire** - Re-copy every 30-60 days
- **Use strong passwords** - For your Threads account

### 🛡️ Safety
- **Respect rate limits** - Default: 5 posts/day (safe!)
- **Don't spam** - Quality over quantity
- **Follow ToS** - Use responsibly

### ⚖️ Legal
- **Educational purposes only** - Use at your own risk
- **No guarantees** - Results may vary
- **Terms of Service** - Automation may violate Threads ToS

---

## 🆘 Troubleshooting

<details>
<summary><b>Config file not found</b></summary>

```bash
copy config.example.yaml config.yaml
```
Then edit `config.yaml` and add your cookies.

</details>

<details>
<summary><b>Invalid session / Cookie expired</b></summary>

Your cookies expired. Get fresh cookies:
1. Open threads.com (make sure you're logged in)
2. Press F12 → Application → Cookies
3. Copy new sessionid, csrftoken, ds_user_id
4. Paste into config.yaml

</details>

<details>
<summary><b>Rate limited error</b></summary>

You're posting too much. Solutions:
- Wait a few hours
- Reduce `posts_per_day` in config.yaml
- Increase `min_delay_hours`

</details>

<details>
<summary><b>Import errors</b></summary>

```bash
pip install -r requirements.txt
```

</details>

---

## 🤝 Contributing

We love contributions! Here's how you can help:

- 🐛 **Report bugs** - [Open an issue](https://github.com/airdrop-888/threadGPT/issues)
- 💡 **Suggest features** - [Start a discussion](https://github.com/airdrop-888/threadGPT/discussions)
- 🔧 **Submit PRs** - Check [Contributing Guide](CONTRIBUTING.md)
- ⭐ **Star the repo** - Show your support!

---

## 📊 Stats & Roadmap

<div align="center">

### ⭐ GitHub Stats

[![Star History](https://img.shields.io/github/stars/airdrop-888/threadGPT?style=social)](https://github.com/airdrop-888/threadGPT/stargazers)
[![Forks](https://img.shields.io/github/forks/airdrop-888/threadGPT?style=social)](https://github.com/airdrop-888/threadGPT/network/members)
[![Issues](https://img.shields.io/github/issues/airdrop-888/threadGPT)](https://github.com/airdrop-888/threadGPT/issues)

</div>

### 🗺️ Roadmap

- [x] Core scheduling engine
- [x] CSV bulk schedule
- [x] Analytics tracking
- [x] Viral content detector
- [ ] AI content generation (OpenAI integration)
- [ ] Web dashboard UI
- [ ] Multi-account support
- [ ] Mobile app companion
- [ ] Browser extension

---

## 💬 Community

Join our growing community:

- 💬 [GitHub Discussions](https://github.com/airdrop-888/threadGPT/discussions)
- 📺 [YouTube Tutorials](https://youtube.com/@yourusername)
- 🐦 [Twitter Updates](https://twitter.com/yourusername)

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**Disclaimer**: This tool is for educational purposes only. Use responsibly and at your own risk. The authors are not responsible for any consequences resulting from the use of this software.

---

## 💖 Support the Project

If ThreadsGPT helped you grow your Threads account:

- ⭐ **Star this repo** - It helps others find it!
- 🐦 **Share on social media** - Spread the word
- ☕ **Buy me a coffee** - [Support development](https://ko-fi.com/yourusername)
- 📝 **Write a review** - Share your experience

---

## 🙏 Acknowledgments

Built with ❤️ by the community, for the community.

Special thanks to:
- All contributors who made this possible
- The amazing Python & open-source community
- Everyone who starred, forked, and shared this project

---

<div align="center">

### 🚀 Ready to Automate Threads?

**[Get Started Now](#-quick-start)** | **[Read Docs](#-documentation)** | **[Join Community](#-community)**

---

**Made with 🔥 and ☕ by [@airdrop-888](https://github.com/airdrop-888)**

*Star ⭐ this repo if you find it useful!*

</div>
