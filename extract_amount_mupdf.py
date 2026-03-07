import fitz  # PyMuPDF
import re
import sys
import os

RM_PATTERN = re.compile(r"RM(\d+\.\d+)")


def get_tessdata():
    """Return tessdata path. When frozen by PyInstaller, use bundled tessdata."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'tessdata')
    return None  # let PyMuPDF auto-detect from system Tesseract


def get_page_text(page, tessdata):
    """Extract text from page, using OCR if the page is image-based."""
    text = page.get_text()
    if text.strip():
        return text
    # No selectable text — page is image-based, use OCR
    tp = page.get_textpage_ocr(dpi=300, language="eng", full=True, tessdata=tessdata)
    return page.get_text(textpage=tp)


def extract_amounts(pdf_path):
    amounts = []
    tessdata = get_tessdata()
    doc = fitz.open(pdf_path)
    for page in doc:
        text = get_page_text(page, tessdata)
        # Split on transaction boundaries: date line followed by status
        blocks = re.split(r"(?=\d{1,2}/\d{1,2}/\d{4}\n(?:Success|Pending|Failed)\n)", text)
        for block in blocks:
            if "Success" not in block:
                continue
            success_count = block.count("Success")
            non_zero = [float(v) for v in RM_PATTERN.findall(block) if float(v) > 0]
            # Take one amount per Success (handles both per-row and columnar PDF layouts)
            amounts.extend(non_zero[:success_count])
    doc.close()
    return amounts


def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        pdf_path = os.path.join(base_dir, "sample.pdf")

    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        input("Press Enter to exit...")
        sys.exit(1)

    amounts = extract_amounts(pdf_path)

    print(f"{'No.':<5} {'Amount (RM)':>12}")
    print("-" * 20)
    for i, amt in enumerate(amounts, 1):
        print(f"{i:<5} {amt:>12.2f}")
    print("-" * 20)
    print(f"{'Total':<5} {sum(amounts):>12.2f}")
    print(f"\nTotal transactions: {len(amounts)}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
