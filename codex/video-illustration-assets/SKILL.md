---
name: video-illustration-assets
description: Use when creating or revising videos, video scripts, video generation code, short-form clips, landscape videos, or HyperFrames/Remotion-style compositions that should incorporate the user's saved original AI/person illustration assets from OneDrive. Trigger on requests like "次に動画作る", "動画を作る", "AI動画", "ショート動画", "動画生成", or when a video needs friendly explanatory male character images, AI assistant visuals, or AI neural network background imagery.
---

# Video Illustration Assets

## Core Rule

When producing a video for the user, actively incorporate the saved original illustrations unless the user asks for a different visual style or the subject clearly conflicts.

Read `references/asset-manifest.md` before selecting visuals. Use the absolute paths listed there directly in scripts, FFmpeg filters, HTML compositions, HyperFrames, Remotion, PowerPoint-to-video workflows, or other video generation pipelines.

## Usage Guidance

- Use the male character images for explanation, thinking, and gentle caution scenes.
- Use the AI assistant avatar for AI tool, chatbot, automation, and helper scenes.
- Use the neural network background for opening, transition, abstract AI, or data-processing scenes.
- Use the contact sheet only for preview, selection, QA, or storyboard review. Do not place the contact sheet in the final video unless the user explicitly asks.
- Prefer these original illustrations over generic stock-like images for AI/business explainer videos.
- Match the asset to the scene intent before rendering: presenter for human explanation, AI avatar for tool/assistant moments, neural background for abstract AI or transition scenes.
- Keep character scale, crop, and placement consistent across scenes unless a zoom or emphasis is intentional.
- When generating multiple video formats, reuse the same chosen asset set so short and landscape versions feel related.

## Verification

Before rendering the final video, confirm that every referenced illustration path exists. If a file is missing, report the missing path and continue with the available assets only when the visual still makes sense.

Also verify:

- The final script/code references absolute paths from `references/asset-manifest.md`.
- The contact sheet was not accidentally placed in the final video.
- Assets are not stretched, clipped awkwardly, hidden by captions, or too small to recognize.
- The rendered preview or contact sheet shows the selected illustrations in the expected scenes.
