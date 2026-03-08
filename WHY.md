# Why Not Just Ask an AI?

A natural question: why build a dedicated tool when you can just upload the PDF to ChatGPT, Claude, or Gemini and ask for the total?

We tested the same `sample.pdf` (correct answer: **RM 104.20**) across five AI assistants with the same prompt:

| AI | Result | Correct? |
|---|---|---|
| ChatGPT | RM 89.70 | ❌ |
| Claude | RM 14.50 | ❌ |
| Gemini | RM 93.41 | ❌ |
| DeepSeek | RM 108.35 | ❌ |
| Grok | RM 104.20 | ✅ |

4 out of 5 got it wrong. Only one got lucky.

## Why AI Chat Gets It Wrong

**The TNG PDF is a mixed document.** Page 1 is image-based (no selectable text), while the remaining pages are text-based. Most AI chat interfaces handle this inconsistently:

- **Skip image pages entirely** — missing all transactions on page 1
- **Use basic OCR that misreads amounts** — small font, dense layout, similar-looking numbers
- **Hallucinate numbers** to fill gaps they cannot read
- **Include wrong transaction types** — counting pending, failed, or non-toll transactions

AI assistants are designed to *understand* documents, not *parse* them with precision. For financial data, that distinction matters.

## Why This Tool Gets It Right

`extract_amount_mupdf.py` is purpose-built for this exact PDF format:

- **Detects image-based pages** and automatically switches to Tesseract OCR for those pages
- **Only counts `Success` RFID transactions** — pending, failed, and non-toll entries are excluded
- **Deterministic** — the same PDF always produces the same result, every time
- **No guessing** — it either finds a transaction or it doesn't

For expense claims, you need a number you can stand behind. This tool gives you that.
