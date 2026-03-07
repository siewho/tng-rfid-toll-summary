# TNG Toll Summary

Extracts and totals RFID toll charges from TNG eWallet transaction history PDFs.

## The Problem

Submitting toll expenses for reimbursement means opening the TNG eWallet app, downloading the transaction history PDF, and then manually going through every single line item, copying amounts into a calculator, and hoping nothing got missed or fat-fingered.

The PDF spans multiple pages, mixes image-based and text-based content, and lists every transaction with no subtotal in sight. One missed entry and the whole claim is wrong. It's tedious, error-prone, and a waste of time to repeat every single month.

This tool automates that.

## What It Does

- Opens any TNG eWallet transaction history PDF
- Reads all pages, including image-based pages using OCR
- Extracts every `Success` RFID toll transaction amount
- Prints a numbered list and a grand total

## Usage

### Option 1 — Double-click
Place `extract_amount.exe` in the same folder as your PDF (named `sample.pdf`) and double-click it.

### Option 2 — Drag and drop
Drag your PDF file onto `extract_amount.exe`.

### Option 3 — Command line
```
extract_amount.exe path\to\your_statement.pdf
```

### Example output
```
No.    Amount (RM)
--------------------
1             4.67
2             1.17
3             3.50
...
--------------------
Total       104.20

Total transactions: 27
```

## Download

Download the latest `extract_amount.exe` from the [Actions](../../actions) tab:

1. Click the latest successful workflow run
2. Scroll down to **Artifacts**
3. Download `extract_amount-windows`

No Python installation required.

## How to Get Your TNG PDF

1. Open TNG eWallet app
2. Go to **Transaction History**
3. Tap the download / export icon
4. Select your date range and export as PDF
5. Transfer the PDF to your Windows PC

## Build from Source

Requires Python 3.11+ and Tesseract OCR installed.

```bash
pip install pymupdf
python extract_amount_mupdf.py path/to/statement.pdf
```

To build the Windows `.exe` locally on a Windows machine:

```bash
pip install pymupdf pyinstaller
pyinstaller --onefile --console --add-data "C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata;tessdata" --name extract_amount extract_amount_mupdf.py
```

Or just push to `main` and let GitHub Actions build it for you.

## Tech Stack

- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing and built-in OCR support
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — reads image-based pages in the PDF
- [PyInstaller](https://pyinstaller.org/) — packages everything into a single `.exe`
- [GitHub Actions](https://github.com/features/actions) — builds the Windows `.exe` in the cloud
