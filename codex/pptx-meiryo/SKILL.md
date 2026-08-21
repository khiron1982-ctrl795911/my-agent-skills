---
name: pptx-meiryo
description: Use when creating or substantially revising PPTX files with python-pptx, especially Simul International decks. Enforces Meiryo, 16:9 layout, Simul Blue, safe margins, custom text boxes, and post-generation validation.
---

# pptx-meiryo

Use this skill whenever creating or substantially revising PowerPoint files with Python.

## Role

- Apply implementation rules for PPTX generation and substantial revision with `python-pptx`.
- Use the `ppt` skill for slide-message design, deck structure, and layout-pattern selection.
- Preserve the user's source deck and write a versioned output file when revising an existing PPTX.

## Hard Rules

- Use `python-pptx` only. Do not use `pptxgenjs`.
- Set size immediately after `Presentation()`:
  - `prs.slide_width = Inches(13.33)`
  - `prs.slide_height = Inches(7.5)`
- Use custom `add_textbox` text boxes. Do not rely on placeholders for generated decks.
- Set every run font to `Meiryo`.
- Use 16:9, white background, Simul Blue `RGBColor(0x00, 0x5C, 0xFF)`.
- Keep each slide to at most 3 main colors.
- Safe margins: left/right `0.5"`, top/bottom `0.4"`.
- Title top: `0.4"`. Main left: `0.5"`.
- Round coordinates to `0.05"`.
- Text boxes must set:
  - `tf.word_wrap = True`
  - `tf.vertical_anchor = MSO_ANCHOR.MIDDLE`
  - `tf.auto_size = None`
  - `tf.margin_left = tf.margin_right = Inches(0.1)`
  - `tf.margin_top = tf.margin_bottom = Inches(0.05)`
- Font sizes:
  - title `28pt`
  - heading `20pt`
  - body `14pt`
  - note `11pt`
  - never below `10pt`
- Set paragraph line spacing explicitly, usually `Pt(20)` for body.
- Add images before text boxes so text remains above images.
- Preserve image aspect ratio by specifying only width or height unless intentionally cropping.
- Minimum text/image gap: `0.25"`.
- Bullets:
  - max 2 levels
  - max 7 items per box
  - roughly 40 Japanese chars per item at 14pt
  - first level `■`, second level `・`
  - use bold or color for emphasis; avoid underline/italic.
- Tables:
  - cell margin left/right `0.1"`, top/bottom `0.05"`
  - numeric values right-aligned
  - comma separators for large numbers
  - no 3D charts
  - legend right or bottom.

## Required Validation

Run validation after generation or substantial revision. Fix and regenerate until there are no issues:

```bash
python -X utf8 scripts/validate_pptx.py path/to/deck.pptx
```

When running outside the skill directory, resolve the script path explicitly:

```powershell
python -X utf8 "C:\Users\khiro\.codex\skills\pptx-meiryo\scripts\validate_pptx.py" "path\to\deck.pptx"
```

The validator checks slide size, out-of-bounds shapes, text overflow risk, minimum font size, and non-Meiryo text runs. It is a structural check, not a substitute for visual PNG review.

## Existing PPTX Revisions

When revising an existing deck instead of rebuilding from scratch:

- Preserve the user's source file; write a new versioned file.
- Set all text runs to `Meiryo`.
- Normalize text frame settings where safe.
- Validate bounds and fonts.
- Call out any remaining limitation if the deck still uses existing placeholders or inherited shapes.

## Simul HR Deck Conventions

For Simul HR decks, keep terms consistent:

- Use `ポジション番号`, not `ランク`, for grade-internal salary steps.
- Use `評価区分` for S/A/B/C/D labels.
- Use one bonus profit basis consistently across decks; default to `営業利益` unless the user specifies otherwise.
- Use `C以下` consistently for low-rating triggers unless the approved policy says otherwise.
- Avoid direct employee-facing wording such as `給料DOWN`; use `処遇見直し` or `給与見直し`.
- Avoid promising automatic salary increases. Explain that changes depend on evaluation, role, company performance, and transition protections.

## Debug Checklist

- Compile or run the deck-generation script before validating the output PPTX.
- Run `validate_pptx.py` and fix every structural issue that is not an intentional exception.
- Export or render slides to images when possible and visually inspect text overflow, image cropping, table density, and slide-to-slide consistency.
- Keep the original deck untouched when revising an existing file; deliver a versioned output path.
