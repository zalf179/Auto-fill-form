# 📋 Google Form Auto Filler

Automates filling a Google Form using respondent data from an Excel file. Built with Python and Playwright.

---

## 🗂️ Project Structure

```
project/
├── fill_form.py
├── data.xlsx
└── README.md
```

---

## ✅ Prerequisites

- Python 3.8 or higher
- Google Chrome (installed on your machine)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Python dependencies

```bash
pip install pandas openpyxl playwright
```

### 3. Install Playwright browser

```bash
playwright install chromium
```

---

## 📊 Prepare the Excel File

Create a file named `data.xlsx` in the project root with the following columns:

| Column | Description | Example |
|---|---|---|
| `nama` | Full name | Raka Arvindra |
| `email` | Email address | raka@email.com |
| `umur` | Age | 25 |
| `jabatan` | Job title | Staff |
| `masa_kerja` | Years of service | 3 tahun |
| `gender` | Gender (`LAKI - LAKI` or `PEREMPUAN`) | LAKI - LAKI |

> ⚠️ Make sure column names match exactly (lowercase, no extra spaces).

---

## ▶️ Running the Script

```bash
python fill_form.py
```

The browser will open automatically and fill out the form for each row in `data.xlsx`.

---

## ⚙️ Configuration

You can adjust the Likert answer distribution at the top of `fill_form.py`:

```python
LIKERT_CHOICES = [
    "Netral",
    "Setuju",
    "Sangat Setuju"
]

LIKERT_WEIGHTS = [
    20,  # Netral      — 20%
    50,  # Setuju      — 50%
    30   # Sangat Setuju — 30%
]
```

Change the weights to control how often each answer is selected.

---

## 📌 Notes

- The script adds a **random delay of 2–5 seconds** between submissions to avoid being flagged.
- If a row fails, the script **skips it and continues** to the next one.
- The browser runs in **headed mode** (visible) by default. To run headlessly, change `headless=False` to `headless=True` in `fill_form.py`.

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install pandas openpyxl playwright` |
| `playwright install` fails | Run as administrator / use `sudo` on Mac/Linux |
| Form options not found | Check if the form URL is still active |
| Wrong number of questions | Verify `likert_start` index in the script matches your form layout |

---

## 📄 License

MIT License — free to use and modify.
