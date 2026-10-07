# Photo Skills

Reusable skills that turn photos into different styles of art.

[中文说明](README.zh-CN.md) · [License](LICENSE)

Each skill has its own folder under `skills/`. Download and install only the skills you want.

## Available skills

| Skill | Result | Folder |
| --- | --- | --- |
| Photo-to-Sketch Storytelling | A real photo continues into a drawing on warm white paper, with a small character taking part in the scene. | [photo-to-sketch-storytelling](skills/photo-to-sketch-storytelling/SKILL.md) |
| Photo-to-Watercolor Journal | A pen-and-watercolor travel page with four color swatches and handwritten English captions. | [photo-to-watercolor-journal](skills/photo-to-watercolor-journal/SKILL.md) |
| Photo-to-Rainbow Ink Diptych | A real photo above colorful ink and watercolor art with rough paper texture. | [photo-to-rainbow-ink-diptych](skills/photo-to-rainbow-ink-diptych/SKILL.md) |
| Photo-to-Paper Relief Poster | A separate 3:4 poster with thin paper relief, warm white space and small Chinese-English titles. | [photo-to-paper-relief-poster](skills/photo-to-paper-relief-poster/SKILL.md) |
| Photo to Soft Gradient | A real photo above soft gradient art, with overlapping color fields and a few recognizable details. | [photo-to-soft-gradient](skills/photo-to-soft-gradient/SKILL.md) |

## Choose a style

| Style | Suitable photos |
| --- | --- |
| Photo and drawing | Scenes with an object or shape that can continue into a small drawn story |
| Watercolor journal | Streets, buildings, nature, travel scenes and people with their surroundings |
| Rainbow ink | Night lights, water, plants, buildings, animals and travel scenes |
| Paper relief poster | Buildings, flowers, trees, still life, landscapes and people with their surroundings |
| Soft gradient | Flowers, leaves, birds, animals, water, trees, night scenes, buildings and people with their surroundings |

Faces need extra care in all generated styles. Some skills include scripts that place actual source-face pixels into the result. A prompt alone cannot guarantee unchanged faces.

## Photo to Soft Gradient

Create one vertical **9:16** image for each photo. Put an actual **16:9** crop of the original at the top. Use only crop and uniform resize there: no recoloring, retouching or generated replacement.

Generate the lower art first. Keep a few details that make the photo recognizable, while changing scale, position or space. Build **3–5 large, soft, overlapping color fields** on a dark blue, violet, green or source-colored base. Let one field cross an outer subject edge and dissolve it into light. Keep some details clear and a wide area quiet.

Add no text, frames, watermarks, neon outlines, stars, smoke, coarse grain or paper texture. Finish by placing the real photo above the generated art.

### Suitable photos

| Photo type | What to keep |
| --- | --- |
| Flowers and leaves | Flower centers, petal edges, leaf veins and original colors |
| Birds and other animals | Species, number, pose and body shape |
| Lakes, ponds, reeds and reflections | Shoreline, plant shapes, ripples and real reflection direction |
| Trees and woods | Main trunks, branch curves and leaf shapes |
| Night scenes, streets and buildings | Light direction, a clear building edge or a recognizable object |
| People with their surroundings | Original faces, clothing, pose and important contacts |
| Face close-ups, ID photos and exact maps | Not a main use; this style changes space and reduces detail |

Default output: **1152×2048 PNG**. The upper photo is **1152×648**; the lower art is **1152×1400**. The top is about 31.6% of the height.

For visible faces below, keep the actual source facial features, expression, glasses and skin color. Use reviewed masks, uniform scale and translation; do not tint or dissolve the protected face area. The script checks the saved top against the resized source crop, and protected faces against the transformed source. It does not choose a good crop or detect faces for you.

### Use

```text
Use $photo-to-soft-gradient to turn this photo into a 9:16 photo-and-gradient image.
Keep a real 16:9 crop above. Generate the lower art with 3–5 soft color fields,
a few clear source details and a quiet dark area. Preserve original faces.
Add no text or frames. Generate the lower art first, then assemble the real photo above it.
```

### Included files

| File | Purpose |
| --- | --- |
| `SKILL.md` | Main workflow and matching description |
| `agents/openai.yaml` | Name, short description and example request |
| `references/prompt-template.md` | Lower-art prompt and revision examples |
| `references/scene-guide.md` | Guidance for different photo types |
| `references/assembly-and-faces.md` | Crop, assembly and original-face instructions |
| `references/quality-checks.md` | Checks before delivery |
| `scripts/compose_image.py` | Crop preview, assembly and saved-pixel checks |

## Download and install

1. On the repository page, select **Code → Download ZIP**.
2. Extract the ZIP and open `skills/`.
3. Copy the complete skill folder you want, including its references and scripts, into your AI tool's supported skill location, or use that tool's supported import flow.
4. Upload your own photo and ask the AI to use the skill.

For the new style, choose `skills/photo-to-soft-gradient/`. Do not install only `SKILL.md`; keep the entire folder.

## Requirements

Your AI tool must be able to read skills and view photos. Generating art also requires an image generation/editing tool. **Installing a skill does not install an image model or grant tool access.** Different image models can produce different results.

The soft-gradient assembly script needs Python 3 and Pillow:

```bash
python -m pip install "Pillow>=10"
```

Without an image tool, ask for a prompt only. Without ordinary image assembly, a generated upper photo cannot be claimed as the untouched original.

## Add a skill

Create a separate folder under `skills/`, add its `SKILL.md` and needed files, then add a row to both README tables. Keep all table rows together with no blank line between them.

Keep private photos, account details and generated private images outside this repository. Publish third-party example images only when you have permission.

## License

Skill instructions and included code use the [MIT License](LICENSE). User photos and third-party images are not covered by that license.
