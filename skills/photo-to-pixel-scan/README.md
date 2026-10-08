# Photo to Pixel Scan

Turn a building or landscape photo into one continuous image: part real photo, part clear 2D pixel art, joined by a glowing pixel scan.

[中文说明](README.zh-CN.md) · [Instructions](SKILL.md) · [License](LICENSE)

**Skill name:** `photo-to-pixel-scan`

**Short description:** Blend architecture and scenery photos with large 2D pixel blocks, a gently wavy scan and colors taken from the local scenery.

## Updated treatment

Use the current roughly 20 percent enlargement target, without enlarging it again on each run. Keep colored translucent scanner grains and a thin bright core. Build purposeful square color groups instead of random small fragments. For an unstable division, generate full pixel art first, assemble it with the real photo, and add the scan only along that established join. See [the staged workflow](references/staged-workflow.md).

[Complete Chinese and English prompts](references/prompt-template.md)

## Suitable photos

Use architecture, streets, village rows, forests, flowers, fields, mountains, lakes and landscape attractions such as balloon-shaped structures. Do not use portrait, group-photo, pet or animal-theme photos.

A whole building complex is the subject, including towers, roofs, walls and stairs. For an isolated object, divide the object itself. For a forest or other scene without a separate object, divide the whole view.

## What this version keeps

- Preserve the original ratio, framing and subject geometry.
- Keep the complete subject and whole frame each near half photo and half pixels.
- Use a nearly straight curve with only slight smooth waves. Adjust its angle and position without sharp corners or large bends.
- Keep a complete glowing scan made of square cells; use colors from the material it crosses.
- Use clearly visible large pixels. Give buildings coarse wall shading, stepped roofs and pixel-built windows, rather than smooth painterly surfaces.
- Use somewhat smaller visible cells for small details; pixel-paint every object in the edited region.
- Preserve the actual original photographic region through source restoration.

## Use

Upload an original and ask:

```text
Use $photo-to-pixel-scan for this building or landscape photo.
Keep the complete subject and whole frame close to half photo and half pixels.
Use large visible pixel blocks, including on buildings,
and a slightly wavy scan with local source colors.
Preserve the original photo region and output each image separately.
```

The AI needs to view images and provide image generation or editing. This skill supplies instructions, not an image model. Different models may produce different results.

The optional restoration helper needs Python 3, Pillow and ImageMagick:

```bash
python -m pip install -r requirements.txt
python scripts/compose_pixel_scan.py --source original.jpg --plan reviewed-plan.json --check-plan
python scripts/compose_pixel_scan.py --source original.jpg --art generated.png --plan reviewed-plan.json --output final.png
```

Read [composition.md](references/composition.md) before writing a plan. The helper supports top-to-bottom and left-to-right routes. It checks areas and unchanged photo pixels, but cannot judge the artistic scan join; inspect it visually. If source restoration is unavailable, call the result a generated preview rather than an untouched-photo composite.

## Download and upload

From a GitHub collection, download its ZIP, extract it and select the complete `skills/photo-to-pixel-scan/` folder. Import it using your AI tool's supported method.

For the `photo_skills` collection, place this complete folder under `skills/`, beside the other skills. The final path must be `skills/photo-to-pixel-scan/SKILL.md`. Keep supporting folders together. Use the two collection README files in `assets/project-readmes/` at the repository root; they include all six styles. Keep `.gitignore` as a file with that exact name.

## Files

| File or folder | Purpose |
| --- | --- |
| `SKILL.md` | Instructions for the AI |
| `agents/openai.yaml` | Display name and example request |
| `references/` | Prompts, scene choices, pixel sizes, restoration and checks |
| `scripts/compose_pixel_scan.py` | Area checks and original-photo restoration |
| `requirements.txt` | Python dependency for the helper |
| `README.md`, `README.zh-CN.md` | Plain-language usage and upload notes |
| `assets/project-readmes/` | English and Chinese collection descriptions |
| `.gitignore` | Keep caches and local input/output folders out of uploads |
| `LICENSE` | MIT license for instructions and code |

Tests on houses, a village, a castle, a forest and a balloon-shaped attraction helped refine this style. These examples do not guarantee identical results for every photo. Private photos and third-party screenshots are not included or licensed by this project.
