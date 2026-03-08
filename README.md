# TNG RFID Toll Summary

A simple Windows app that reads your TNG eWallet RFID toll transaction PDF and gives you the total in one click — ready to paste into your expense claim.

![TNG Toll Summary screenshot](tng-toll-summary-screenshot.png)

<video src="https://github.com/siewho/tng-rfid-toll-summary/blob/main/tng-toll-summary-video.mp4" controls width="100%"></video>

---

## The Problem

**For employees submitting claims:**
Every month, claiming toll expenses means opening the TNG eWallet PDF, scrolling through every page, and manually adding up each charge one by one — hoping nothing got missed along the way. The PDF spans multiple pages, lists every single transaction individually, and provides no subtotal anywhere. One fat-finger or missed line and the whole claim is wrong.

**For HR processing claims:**
When a colleague submits a TNG RFID toll claim, HR has to open the same PDF and manually verify every transaction against what was submitted. With 20–30+ transactions per person per month, and multiple colleagues submitting at once, this means re-counting every single line item, cross-checking totals, and catching any discrepancies — all by hand. It's slow, repetitive, and mistakes are easy to make.

This app solves both sides: employees get an accurate total in seconds, and HR gets a clean number they can verify instantly.

---

## How to Use

### Step 1 — Download the app

1. Go to the [**Releases**](../../releases/latest) page
2. Under **Assets**, click **`tng_toll_summary.exe`** to download it

> No installation required. Just download and run.

---

### Step 2 — Export your TNG PDF

1. Open the **TNG eWallet** app on your phone
2. Tap **Transactions** → **Recent transaction**
3. Tap the **filter icon** (top right), select RFID
4. Select your vechile plate number
5. Select your date range (e.g. the claim month)
6. Tap the **Send to email**, the **PDF** will send to your inbox
7. Check email and download the pdf

---

### Step 3 — Run the app

Double-click **`tng_toll_summary.exe`** to open it.

You'll see a window like the screenshot above.

**Option A — Drag and drop**
Drag your PDF file from File Explorer and drop it onto the app window.

**Option B — Click to browse**
Click anywhere inside the dashed box and select your PDF file.

---

### Step 4 — Copy the total

The app will read your PDF (this takes 2–5 seconds) and show:

- A numbered list of every successful RFID toll charge
- The **total amount** at the bottom

Click **Copy** next to the total — then paste it directly into your expense claim form.

---

## Frequently Asked Questions

**The app says it can't find transactions.**
Make sure the PDF is a TNG eWallet transaction history export, not a screenshot or a bank statement.

**The total looks wrong.**
The app only counts **Success** RFID toll transactions. Pending, failed, or non-toll transactions are excluded.

**My antivirus flagged the file.**
The `.exe` is built automatically by GitHub Actions from the source code in this repository. This is a common false positive for PyInstaller-packaged apps. You can review the source code here and build it yourself if preferred.

**I'm on Mac or Linux.**
The `.exe` is Windows-only. On Mac/Linux you can run the script directly — see [Build from Source](#build-from-source) below.

---

## Build from Source

Requires Python 3.11+, [uv](https://github.com/astral-sh/uv), and Tesseract OCR.

```bash
git clone https://github.com/siewho/tng-rfid-toll-summary
cd tng-rfid-toll-summary
uv sync
uv run python gui.py
```

The Windows `.exe` is built automatically when you push to `main` via GitHub Actions.

---

## Tech Stack

- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing with built-in OCR support
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — reads image-based pages in the PDF
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) — GUI framework
- [PyInstaller](https://pyinstaller.org/) — packages everything into a single `.exe`
- [GitHub Actions](https://github.com/features/actions) — builds the Windows `.exe` in the cloud
- [uv](https://github.com/astral-sh/uv) — Python package manager

---

## License

[MIT](LICENSE)
