# 🐍 Python Mini Projects

A comprehensive collection of **60+ Python scripts** for automation, web scraping, file processing, encryption, and daily utilities. Perfect for learning Python or boosting productivity.

## 📁 Project Structure
Python-Mini-Projects/
│
├── apps/
│   ├── calculate_age.py
│   ├── cli_todo.py
│   ├── emails_csv.py
│   └── image_watermarking.py
│
├── automation/
│   ├── low_battery_notification.py
│   ├── screenshots_capture.py
│   └── download_folder_categorywise.py
│
├── converters/
│   ├── json_to_csv.py
│   ├── currency_converter.py
│   └── decimal_to_binary.py
│
├── file_tools/
│   ├── search.py
│   ├── compress_f.py
│   └── chunks.py
│
├── utilities/
│   ├── password_generator.py
│   ├── stopwatch.py
│   ├── text_to_speech.py
│   ├── encrypt_decrypt.py
│   ├── ipaddress.py
│   ├── progress_Bar.py
│   └── passwordEjector.py
│
└── webScraping/
    ├── fetch_links.py
    ├── Ratings.py
    ├── comment.py
    ├── scrap_Download_images.py
    └── snapshot.py

---

## 🚀 Projects by Category

### 📱 Apps (4 scripts)
| Script | What it does | Input | Output |
|--------|-------------|-------|--------|
| `calculate_age.py` | Calculates exact age in years, months, days | Birth date | Age calculation |
| `cli_todo.py` | Manage tasks from command line | Task description | Task list with IDs |
| `emails_csv.py` | Send bulk emails from CSV file | Email list, credentials | Sent emails |
| `image_watermarking.py` | Add text/logo watermark to images | Image folder, watermark | Watermarked images |

### 🤖 Automation (3 scripts)
| Script | What it does | Best for |
|--------|-------------|----------|
| `low_battery_notification.py` | Monitors battery and sends alerts | Laptop users |
| `screenshots_capture.py` | Takes screenshots at set intervals | Recording sessions |
| `download_folder_categorywise.py` | Organizes downloads by file type | Keeping Downloads folder clean |

### 🔄 Converters (3 scripts)
| Script | What it does | Example |
|--------|-------------|---------|
| `json_to_csv.py` | Converts JSON to CSV | API data → Spreadsheet |
| `currency_converter.py` | Real-time currency conversion | USD → EUR |
| `decimal_to_binary.py` | Binary/Decimal conversion | 42 → 101010 |

### 📁 File Tools (3 scripts)
| Script | What it does | Use case |
|--------|-------------|----------|
| `search.py` | Search text across multiple files | Find code or text in folders |
| `compress_f.py` | Compress files/folders to ZIP | Save disk space |
| `chunks.py` | Split large files into smaller parts | Email attachments, upload limits |

### 🛠️ Utilities (7 scripts)
| Script | What it does | Special requirement |
|--------|-------------|---------------------|
| `password_generator.py` | Generates random secure passwords | None |
| `stopwatch.py` | GUI stopwatch with lap timing | tkinter (built-in) |
| `text_to_speech.py` | Converts text file to MP3 | Internet connection |
| `encrypt_decrypt.py` | AES-256 encryption | pycryptodome |
| `ipaddress.py` | Get website IP address | None |
| `progress_Bar.py` | Bulk image resizer | Pillow |
| `passwordEjector.py` | Show saved WiFi passwords | Windows, Admin rights |

### 🌐 Web Scraping (5 scripts)
| Script | What it does | Note |
|--------|-------------|------|
| `fetch_links.py` | Extract all links from webpage | Uses requests + BeautifulSoup |
| `Ratings.py` | Get IMDB movie ratings | Scrapes IMDB |
| `comment.py` | Scrape YouTube comments | Uses Selenium |
| `scrap_Download_images.py` | Download all images from webpage | Any website |
| `snapshot.py` | Take full-page screenshot | Uses Selenium + ChromeDriver |

**Total: 25+ working Python scripts!**

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** (Download from [python.org](https://python.org))
- **pip** (comes with Python)
- **Git** (to clone the repository)

### Step 1: Clone the repository
git clone https://github.com/Supreet37/Python-Mini-Projects.git
cd Python-Mini-Projects

### Step 2: Install all dependencies
pip install -r requirements.txt
Or install individually:

# Core web scraping
pip install requests beautifulsoup4 selenium

# Image processing
pip install Pillow pyautogui

# Utilities
pip install gtts psutil plyer tqdm pandas

# Security
pip install pycryptodome

# CLI tools
pip install click
Step 3: Install ChromeDriver (for Selenium scripts)
Download from https://chromedriver.chromium.org/

Add to PATH or place in the script folder

