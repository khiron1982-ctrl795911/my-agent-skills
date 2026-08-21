---
name: ppt
description: General PowerPoint planning, creation, editing, and review for Japanese business decks in Codex. Use for a non-SIMUL deck when Codex needs to turn an outline into slides, choose a layout, improve a .pptx file, or audit readability. For SIMUL internal files and COM rendering QA, follow the local pptx-simul skill instead.
---

# PPT

Use this skill for PowerPoint work where the output must be a practical business deck, not a decorative page. Favor clear structure, one message per slide, and layout choices based on the information relationship.

## Routing

- Start with a text-only slide outline → local `powerpoint-corrections`.
- Need only a layout or diagram recommendation → local `ppt-design-patterns`.
- Edit or QA a SIMUL internal PPTX → local `pptx-simul` (its file rules and COM QA take precedence).
- Create or review any other practical business deck in Codex → this skill.

## Workflow

1. Clarify the deck purpose, audience, delivery context, and desired action.
2. For each slide, write the lead message first. Keep it within 1-2 lines and make it the slide's main claim.
3. Classify the slide's object area:
   - Related elements: comparison, sequence, hierarchy, formula, inclusion, overlap, before/after, etc.
   - Fixed-format content: graph, screenshot, pricing, table, schedule, ranking, case study, Q&A, quote, etc.
   - Page-type content: cover, agenda, company overview, member profile, MVV, history, traction, org chart, etc.
4. Select a layout pattern from `references/design-patterns.md`.
5. Build or revise the slide with enough whitespace, aligned object edges, and clear visual hierarchy.
6. Review the deck for message consistency, overly dense text, inconsistent labels, unreadable numbers, weak contrast, and unsupported claims.

## Design Rules

- Treat the title as the topic and the lead sentence as the conclusion.
- Put the reason, evidence, or explanation in the object area.
- Use horizontal layouts when each item has little text; use vertical layouts when item text is longer.
- Use tables when comparison axes or text volume are high.
- Make the most important number, label, or conclusion visibly dominant.
- Avoid copying source examples blindly. Select the pattern by purpose and information structure.
- When using screenshots, crop aggressively and use callouts or enlargement only for the area being explained.
- When using photos as backgrounds, protect text legibility with overlays or controlled contrast.

## Delivery Gate

Before handing off a deck, render or inspect every changed slide where the environment permits.
Confirm that titles carry the intended conclusion, all text is legible at presentation size, and
data labels, sources, dates, and units are internally consistent. Treat unverified numerical or
external claims as placeholders rather than presenting them as facts.

## Reference

Read `references/design-patterns.md` when selecting layouts, auditing slide patterns, or turning raw content into a deck.

Source inputs:
- Cone article: https://cone-c-slide.com/see-sla/blog/design-pattern/
- Speaker Deck: https://speakerdeck.com/coneinc/pawapointonodezainpatanda-quan-zi-liao-zuo-cheng-shi-nishi-eru39noaidea
- Speaker Deck embed ID: `d461c7030be549c7aa16dbb648ef82ab`
