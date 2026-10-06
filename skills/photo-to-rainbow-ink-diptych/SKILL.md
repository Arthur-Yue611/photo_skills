---
name: photo-to-rainbow-ink-diptych
description: Create a vertical 9:16 photo and rainbow-ink diptych by generating a textured ink-and-watercolor reconstruction below, then deterministically compositing an untouched 16:9 crop of the original photo above. Use for rainbow ink art, torn-paper photo diptychs, folded-paper watercolor, abstract photo archives, neon night streets, landscapes, flowers, foliage, water, animals and environmental portraits. 将照片制作成水墨七彩双联：上方真实原图、下方七彩晕染与粗粝纸张；适用于水墨七彩、撕纸折叠照片艺术、原图与水墨上下对照、提示词设计、批量制作与局部修订。不要用于钢笔淡彩手账、摄影向下延伸加微型人物、纯黑白水墨、精确地图或视频。
---

# Photo-to-Rainbow Ink Diptych

Generate only the lower art panel, then paste the actual source photo above using deterministic image processing. Never ask a generator to reproduce the real-photo panel.

## 1. Inspect the inputs

- Separate the actual source photograph from style references. Treat social-media screenshots as style references; never copy their interface, captions, logos or artwork as source content. Request an actual photograph if only a style screenshot is available for execution. Continue preparing documentation or prompts without it.
- Inspect dimensions, displayed EXIF orientation, subject count/positions/actions/facing directions, depth, light direction, dominant colors, real reflections and any real fog.
- Preserve the source file. Do not adjust exposure, color, sharpness, skin or facial shape in the photo panel.
- For batches, use one output per distinct original scene; do not silently count duplicates or previously generated images as new originals.

## 2. Plan the panels

Default final PNG: **1152 × 2048**. Upper photo: **1152 × 648**, exact 16:9. Lower art: **1152 × 1400**. The top occupies about 31.6% of the height, not half. Use a width divisible by 144 for other exact integer-pixel sizes.

Inspect a 16:9 crop that preserves important people, gestures and relationships before generation:

```bash
python scripts/compose_diptych.py --source original.jpg --prepare-only \
  --output work/top_preview.png --focus-x 0.5 --focus-y 0.5
```

Move the crop focus or supply `--crop-box LEFT TOP RIGHT BOTTOM` in displayed, EXIF-oriented source pixels. A tall photo may not fit full bodies into this shallow crop. Never stretch, move people or reconstruct missing scenery to solve that. Choose a meaningful crop, explain material context loss, or request a wider original if essential subjects cannot coexist in any crop.

Read [references/prompt-template.md](references/prompt-template.md) before generation and [references/scene-adaptation.md](references/scene-adaptation.md) for color and fold decisions.

## 3. Generate only the lower art

- Supply the actual source photograph as the content reference; use style references separately if supported.
- Target **144:175**, approximately 4:5, with margin for a small crop. Do not generate a complete 9:16 diptych and extract its lower half.
- Retain subject count, relative positions, action, facing direction, depth and light direction. Reconstruct the same scene using large wet pigment blooms, ink pools, mineral granulation and rough paper fibers. Avoid a literal cartoon filter.
- Use red, orange, yellow, green, cyan, blue and violet with strengths governed by source light/color. Let source-dominant colors lead; add missing hues as quiet scene-related undertones or accents. Never impose seven equal bands or an unrelated rainbow. For an explicitly requested source-palette-only variant, omit unsupported hues and identify the variant.
- Keep quiet exposed paper between pigment masses and ink anchors. Match paper atmosphere to the scene; do not saturate every area.
- Use a few believable tears, curls or folds motivated by branches, roads, cloth, ripples, architecture or light direction. Keep them subordinate to one main subject reading. Put all paper effects inside the lower panel; never overlay or erase top-photo pixels.
- Preserve people as original poses and silhouettes with matching clothing and facing direction; do not invent facial features. The upper photo preserves the actual face. An abstract lower silhouette does not guarantee a photographic face. If original facial content is explicitly required below too, use protected source-face compositing or a masking editor and inspect it; do not claim prompt-only exact preservation.
- Prohibit text, numbers, logos, watermarks, UI, decorative frames, star fields, synthetic smoke, invented fog, swatches, handwritten captions and unrelated ornaments. Preserve water sparkles, reflections or mist only when present in the original.

Use the host's image generation/editing capability for this stage. Without one, deliver the lower-panel prompt and assembly instructions, not a claimed finished image. Installing this skill does not supply an image model.

## 4. Assemble the real photo last

The requested two-stage workflow authorizes ordinary image processing for assembly. Use Pillow or an equivalent deterministic editor, with no generative changes in the top panel.

```bash
python scripts/compose_diptych.py --source original.jpg --art lower_art.png \
  --output final_diptych.png --focus-x 0.5 --focus-y 0.5
```

Reuse the exact reviewed focus or crop box. Install Pillow in the execution environment if needed. The helper applies only orientation/crop/uniform resize above and crops the lower art to fill without stretching. It refuses input overwrites and flags excessive art cropping. Inspect framing before using `--allow-art-crop`, or regenerate near 4:5; never bypass this check without reviewing subjects.

Paste the original photo after the art is final. Keep its horizontal rectangle intact. Simulate any irregular tear or tonal transition entirely within the art panel; do not feather, fold or retouch the top. Save a lossless verified PNG master.

## 5. Verify and revise

Read [references/quality-checks.md](references/quality-checks.md). Check ratios, source crop, exact saved-top pixel equality with the prepared source crop, lower subject relationships, seven-color balance, paper breathing room and absence of forbidden additions.

Revise only the lower art, then reassemble with the same original and crop. Never send the final diptych through a full-image generator. Without a deterministic editor, report that the untouched-photo requirement remains incomplete.

Return the finished artwork and briefly explain material cropping or a requested variant. Keep private originals and third-party reference screenshots out of public distributions unless publication is explicitly authorized.
