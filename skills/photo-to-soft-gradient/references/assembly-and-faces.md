# Assembly and face protection

Use Python 3 and Pillow 10 or newer. The included script performs assembly only; it does not generate art, detect faces or install an image model.

## Layout

| Part | Default pixels | Ratio |
| --- | --- | --- |
| Final image | 1152×2048 | 9:16 |
| Top source crop | 1152×648 | 16:9 |
| Lower art | 1152×1400 | 144:175 |

Choose another width divisible by 144 for exact pixel sizes. Orient sources using EXIF display orientation, then crop and resize uniformly. Keep RGB values and the source ICC profile; do not run a color conversion, filter, sharpening or retouch on the top.

The script accepts opaque RGB or opaque RGBA inputs. It rejects other image modes and transparency instead of silently changing source colors. An unusual source format needs a reviewed export outside the untouched-photo workflow.

## Crop preview

```bash
python scripts/compose_image.py --source original.jpg --prepare-only \
  --output work/top_preview.png --focus-x 0.5 --focus-y 0.5
```

Set focus values from 0 to 1 or supply an integer-pixel exact 16:9 crop:

```bash
python scripts/compose_image.py --source original.jpg --prepare-only \
  --crop-box 0 100 1600 1000 --output work/top_preview.png
```

All coordinates refer to the displayed EXIF-oriented source, not raw sensor orientation.

## Final assembly

```bash
python scripts/compose_image.py --source original.jpg --art lower_art.png \
  --output final.png --focus-x 0.5 --focus-y 0.5
```

Reuse the reviewed top crop. The script frames the art with uniform resize plus crop, without stretching. It rejects loss of more than 15% of lower-art area unless `--allow-art-crop` is explicitly given after visual review. Prefer regeneration or outpainting near 144:175 when important subjects would be cut off.

The source ICC profile is applied to the final PNG. Supply lower art in the same RGB color space as the source before assembly; do not change source pixels to match generated art. Review mismatched color profiles rather than assuming both images share the same space.

The report includes sizes, top crop, art crop, removed area and pixel verification. The saved PNG is verified before replacing an existing output. Use `--overwrite` only for a reviewed replacement; the script always refuses to overwrite an input.

## Source-face masks

When the lower art contains identifiable faces, plan the body and head orientation to match the source. Prepare a reviewed JSON file:

```json
{
  "faces": [
    {
      "outer": [[110, 80], [230, 80], [230, 220], [110, 220]],
      "core": [[130, 100], [210, 100], [210, 200], [130, 200]],
      "scale": 1.2,
      "source_anchor": [170, 150],
      "target_anchor": [650, 700],
      "feather": 5
    }
  ]
}
```

Coordinates above are illustrative and must be replaced after inspecting the actual source and lower art.

- `outer` and `core`: reviewed polygons in EXIF-oriented full-source pixels. Include all original facial features, contour and glasses in the core; place outer edges beyond it. Keep the core inside the outer.
- `scale`: positive uniform scale for the face and its matching whole person; no independent horizontal/vertical stretch.
- `source_anchor`: a source point matching `target_anchor`.
- `target_anchor`: a point in the final-sized lower panel, measured from its own top-left, not from the full canvas. For the default output, lower coordinates span 1152×1400.
- `feather`: source-pixel blur applied to the outer mask only. Keep every core pixel fully opaque.

```bash
python scripts/compose_image.py --source original.jpg --art lower_art.png \
  --faces reviewed_faces.json --output final.png
```

The script restores faces after framing the lower art, then pastes the top photo last. It checks source-mask coverage, lower-panel fit, face-core overlap and exact saved core equality with the uniformly resampled source. It does not know whether a mask contains a real face or whether the body matches; inspect both.

Remove a conflicting generated face with the image editor before this step. Do not use a larger pasted mask to conceal misaligned anatomy. Do not apply gradient tint, opacity, rotation, beautification or sharpening over a protected core.

## When tools are unavailable

An image generator alone cannot prove that the top is the actual untouched photo. A prompt-only host should return the lower-art prompt and these assembly steps. If it can generate the lower art but cannot assemble it, clearly label that art as incomplete rather than a finished two-part image.

