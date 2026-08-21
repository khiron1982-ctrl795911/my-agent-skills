---
name: "pdf"
description: "Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction."
---


# PDF Skill

Use this skill for PDF work where the visual page matters, not just raw text extraction.

## Workflow
1. Identify the task type: inspect, extract, create, merge/split, annotate, convert, or visual QA.
2. Prefer visual review: render PDF pages to PNGs and inspect them.
   - Use `pdftoppm` if available.
   - If unavailable, install Poppler or ask the user to review the output locally.
3. Use `reportlab` to generate PDFs when creating new documents.
4. Use `pdfplumber` for table/text inspection and `pypdf` for structure, page operations, metadata, and merging; do not rely on extracted text for layout fidelity.
5. After each meaningful update, re-render pages and verify alignment, spacing, and legibility.
6. When the PDF will be edited further in Word, PowerPoint, or Excel, preserve an editable source artifact when practical and export the PDF last.

## Temp and output conventions
- Use `tmp/pdfs/` for intermediate files; delete when done.
- Write final artifacts under `output/pdf/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install reportlab pdfplumber pypdf
```
If `uv` is unavailable:
```
python3 -m pip install reportlab pdfplumber pypdf
```
System tools (for rendering):
```
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian
sudo apt-get install -y poppler-utils
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## Rendering command

macOS/Linux:
```
pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX
```

Windows PowerShell:
```powershell
pdftoppm -png "$env:INPUT_PDF" "$env:OUTPUT_PREFIX"
```

If Poppler is unavailable but Python packages are installed, use `pypdf`/`pdfplumber` for structural checks and clearly state that visual rendering was not performed.

## Quality expectations
- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.
- Avoid rendering issues: clipped text, overlapping elements, broken tables, black squares, or unreadable glyphs.
- Charts, tables, and images must be sharp, aligned, and clearly labeled.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

## Final checks
- Do not deliver until the latest PNG inspection shows zero visual or formatting defects.
- Confirm headers/footers, page numbering, and section transitions look polished.
- Confirm selectable text, links, forms, or bookmarks when those features matter to the request.
- Keep intermediate files organized or remove them after final approval.
