---
name: photo-to-soft-gradient
description: Pair an untouched photo crop above soft gradient art in a vertical 9:16 image. Use for photo to gradient art, soft color fields, floating photo shapes, surreal photo edits, flowers, leaves, birds, animals, water, trees, night scenes, buildings and environmental portraits; also prompt writing, batches and revisions. 照片转柔和渐变双联：上方真实原图，下方以3—5片交叠渐变重组主体；用于弥散渐变、色光消融、悬浮轮廓、风景花叶动物与环境人像，保留原脸。不要用于七彩水墨纸张、旅行手账色卡、纸浆浮雕海报、普通模糊滤镜、精确地图或视频。
---

# Photo to Soft Gradient

Generate only the lower gradient art, then place an actual crop of the source photograph above it. Keep the top untouched except for display orientation, cropping and uniform resizing. Deliver one separate 9:16 image per source.

## 1. Inspect the source

- View the actual photograph before planning. Separate it from style references and previous generated results.
- Treat social-media screenshots as style examples. Ignore their captions, names, controls, logos, watermarks and status bars. Do not use an example's upper photograph as the user's original without an explicit request.
- For creation with only style examples, prepare the skill or prompts. For photo processing without an actual source, request that source.
- Record the subject count, pose, facing direction, key shape, original colors, light direction, reflections and support/contact relationships. Note visible faces, including side profiles.
- Identify one main detail and a few supporting details that will keep the lower art recognizable.

## 2. Plan the crop and lower art

Use **1152×2048 PNG** by default. Place a **1152×648** photo crop above **1152×1400** art. The final ratio is 9:16 and the top is 16:9; the top occupies about 31.6% of the height. Do not divide the canvas into equal halves. Use widths divisible by 144 for other exact sizes.

Preview the top crop before generation:

```bash
python scripts/compose_image.py --source original.jpg --prepare-only \
  --output work/top_preview.png --focus-x 0.5 --focus-y 0.5
```

Inspect the preview. Move the crop focus or pass an exact 16:9 `--crop-box LEFT TOP RIGHT BOTTOM` using EXIF-oriented source coordinates. For tall photos, preserve important faces and actions where possible. Do not stretch, move people or invent missing surroundings to fit a crop. Explain important context loss when it cannot be avoided.

Read [references/scene-guide.md](references/scene-guide.md) to choose the detail, colors and changes of scale or position. Change the lower layout meaningfully: enlarge, lift, extend or rearrange existing shapes. Retain the subject's own structure and pose; preserve meaningful interactions between people, animals and objects.

## 3. Generate the lower panel only

Read [references/prompt-template.md](references/prompt-template.md) before generation.

- Supply the original photograph as the content reference. Request a single lower art panel near **144:175** (roughly 4:5); leave margin for the small framing crop.
- Build **3–5 free-form color fields** of different sizes. Let them overlap and mix naturally, with colors slowly fading away from their centers. Avoid equally sized blobs, equal rainbow bands, outlined ribbons or separate colored tiles.
- Make at least one field pass through the subject so part of its outer shape dissolves into light. Preserve a few sharp, recognizable details; never blur the entire image.
- Derive the main colors from the source. Use deep blue, dark violet, deep green or a dark source color as the base. Keep shadows colored and transparent-looking, highlights soft and broad, and a wide quiet area.
- Turn selected outer shapes into translucent color light, floating shapes or extended forms. Tie these changes to source shape and light. Do not treat the glow as physical smoke or add a starry sky.
- Keep the result clean, airy and slightly weightless. Do not add rough paper, tears, folds, grain, neon outlines, captions, swatches, frames or unrelated decorations.
- Keep subject count, animal species, flower/leaf shape and meaningful contact relationships faithful. Do not add extra people, duplicate a head or change clothing.
- Preserve visible faces exactly through the source-face workflow below. Apply transparency and dissolution outside facial features. Never enlarge a blurry face by inventing sharper eyes or skin.

Use the host's image generation/editing tool. If unavailable, provide the lower-panel prompt and assembly instructions, and state that no image was generated. Do not describe a generated imitation of the original as an untouched top photo.

## 4. Protect faces and assemble

Read [references/assembly-and-faces.md](references/assembly-and-faces.md) for commands, dimensions and face masks.

Use ordinary image processing for this assembly. When a recognizable face appears below, preserve its source facial core with uniform scale and translation only; keep eyes, eyebrows, nose, mouth, face shape, expression, glasses and skin color. Feather only outside the protected core. Keep source face light consistent by designing the nearby gradient around it.

Review face placement against the actual art. Remove a conflicting generated face before compositing; do not place one face over a mismatched head, body or side profile. If faces cannot be preserved with available tools, keep them unrendered/too small to resolve only when the source already has that appearance, or explain the limitation and request direction. Do not silently turn an identifiable person into a silhouette or promise exact preservation from a prompt.

After finishing the lower art, paste the original photo last:

```bash
python scripts/compose_image.py --source original.jpg --art lower_art.png \
  --output final.png --focus-x 0.5 --focus-y 0.5
```

Reuse the reviewed crop. Add `--faces reviewed_faces.json` when needed. Never feather or overlay the top photo, add a gap, or send the complete assembled image back through a generator. Save the lossless PNG. The helper verifies the saved top against the cropped/resized source, and any protected lower face against the uniformly transformed source.

## 5. Check and deliver

Read [references/quality-checks.md](references/quality-checks.md). Inspect all outputs at useful magnification, including side profiles, animal limbs, leaf edges and face transitions.

For a revision, edit the lower art only and repeat assembly using the same original and crop. For batches, track each source separately and return each finished image independently. Do not count style screenshots as requested original photos or show unfinished bases as complete results.

State material crop loss or unresolved fidelity limits briefly. Keep private photos and third-party style examples out of public skill folders unless the user explicitly chooses to publish them.

