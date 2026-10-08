# Photo Skills

Six AI skills for turning your photos into drawings, watercolor pages, colorful ink art, paper art posters, soft gradient images and photo/pixel scans.

[中文说明](README.zh-CN.md) · [License](LICENSE)

Choose a style below. Each skill has its own folder. Download the collection, then choose the complete folder for the style you need.

## Choose a skill

| Style | What you get | Skill name and files |
| --- | --- | --- |
| Photo and drawing | The top stays photographic. A real object continues into a drawing below, with a small character taking part. | [photo-to-sketch-storytelling](skills/photo-to-sketch-storytelling/SKILL.md) |
| Watercolor travel journal | A soft watercolor drawing with thin pen lines, four color samples and handwritten English captions. | [photo-to-watercolor-journal](skills/photo-to-watercolor-journal/SKILL.md) |
| Rainbow ink | Your real photo above colorful ink and watercolor art, with visible paper texture. | [photo-to-rainbow-ink-diptych](skills/photo-to-rainbow-ink-diptych/SKILL.md) |
| Paper art poster | A 3:4 poster with a detailed subject, paper fibers around its edges, plenty of warm white space and small titles. | [photo-to-paper-relief-poster](skills/photo-to-paper-relief-poster/SKILL.md) |
| Soft gradient | Your real photo above soft, overlapping areas of color, with a few clear details from the original. | [photo-to-soft-gradient](skills/photo-to-soft-gradient/SKILL.md) |
| Pixel scan | Original photography beside 2D pixel art, with large square blocks, visibly pixel-painted buildings and a slightly wavy local-color scan. Keep the subject and frame near half-and-half. | [photo-to-pixel-scan](skills/photo-to-pixel-scan/SKILL.md) |

## Photo and drawing — photo-to-sketch-storytelling

Keep the upper part of the photo realistic. Choose something already in it, such as a scarf, branch, road or reflection, and continue that shape downward as a drawing on warm white paper. Add one small character doing something connected to that shape: walking, pulling, weaving or rowing.

Use fine pencil or ink lines and a little color from the photo. Choose a different story for each scene. The default image is vertical, with a **2:3** ratio.

**Suitable photos:** travel scenes, plants, clothes, objects and people with their surroundings. Photos with a clear shape or action work especially well.

**Example request:**

```text
Use $photo-to-sketch-storytelling to continue this photo into a drawing.
Choose an existing object and add a small character doing something with it.
Keep the original faces.
```

## Watercolor travel journal — photo-to-watercolor-journal

Turn the whole scene into a drawing with thin pen outlines and soft watercolor. Keep the photo's original shape and proportions. Let the painted edges fade gently into a paper background that suits the scene: warmer for sunny photos, cooler or darker for evening photos.

Add **four solid color samples** taken from the original photo at the lower right. Add a handwritten English title and a short English sentence near the bottom.

**Suitable photos:** streets, buildings, mountains, lakes, countryside, stations, night scenes and travel photos with people.

**Example request:**

```text
Use $photo-to-watercolor-journal to make a watercolor travel page.
Keep the original image ratio, add four colors from the photo,
and add a handwritten English title and short sentence.
```

## Rainbow ink — photo-to-rainbow-ink-diptych

Create a **9:16** vertical image with two parts. Put a real **16:9** crop of your original photo at the top. Below it, rebuild the same scene with colorful ink, watercolor and rough paper. Paper edges or folds should follow the shapes and light in the photo.

Keep the original photo's main colors strongest. Use the other rainbow colors more quietly. Add no captions, frames, stars or smoke effects.

Generate the lower art first, then place the actual original crop above it. Only crop and resize the top photo without stretching; do not recolor or redraw it.

**Suitable photos:** night lights, streets, plants, flowers, water, reflections, landscapes, buildings, animals and people with their surroundings.

**Example request:**

```text
Use $photo-to-rainbow-ink-diptych to make a 9:16 image.
Keep a real 16:9 photo crop at the top and create colorful ink art below.
Generate the lower art first, then assemble both parts. Add no text or frames.
```

## Paper art poster — photo-to-paper-relief-poster

Make one separate **3:4** vertical poster for each photo. Place the main subject toward the lower right and leave about **60% warm white space**. Keep details clear inside the subject; let its outer edges become thin paper fibers, torn paper and small areas of paint, with gentle shadows.

Put a small Chinese title at the upper left, followed by a smaller English phrase, a number and a short line in a color from the photo. Keep the text light and spaced out. The default size is **1536×2048 PNG**.

**Suitable photos:** buildings, gardens, flowers, trees, objects, mountains, lakes, forests, animals and people with their surroundings.

**Example request:**

```text
Use $photo-to-paper-relief-poster to make a separate 3:4 paper art poster.
Keep plenty of warm white space, paper fibers around the subject,
a small Chinese title and a short English phrase. Preserve original faces.
```

## Soft gradient — photo-to-soft-gradient

Create a **9:16** vertical image. Keep a real **16:9** crop of the original at the top. Below it, choose a few recognizable details and rearrange their size and position so they appear to float or extend into light.

Use **3–5 large, soft areas of color** that overlap and blend. Keep a dark blue, violet, green or source-colored background and a wide quiet area. Let some subject edges fade into the colors while a few details stay clear. Add no text, frames, neon outlines, stars, smoke or rough paper texture.

Generate the lower art first, then place the actual original crop above it. The default result is **1152×2048 PNG**, with a **1152×648** photo above **1152×1400** art.

**Suitable photos:** flowers, leaves, birds, fish, other animals, water, reflections, trees, night scenes, buildings and people with their surroundings.

**Example request:**

```text
Use $photo-to-soft-gradient to make a 9:16 photo-and-gradient image.
Keep the real photo crop above. Use 3–5 overlapping soft colors below,
keep a few recognizable details and preserve original faces. Add no text or frames.
```

## Pixel scan — photo-to-pixel-scan

**Updated pixel scan:** large square color groups, clearly pixel-painted buildings, translucent local-color scan grains and a narrow bright core. If the division is unstable, build the photo/pixel split first and add the scan afterward. [Full prompt and workflow](skills/photo-to-pixel-scan/README.md).

Keep part of the actual photo and turn the rest into clear, large 2D pixel blocks. Join them with one complete glowing square-cell scan. Preserve the original ratio and framing.

Choose the complete subject: all connected architecture in a wide building complex, or the full isolated object. Keep both the subject and the whole picture near half photo, half pixels. Choose the boundary's angle and position for each source; it can connect top and bottom or left and right edges.

Make the boundary nearly straight with only tiny smooth waves. Avoid sharp turns and large curves. Match scan colors to the local scenery. Use large visible cells, including on building walls, roofs and towers; make curved outlines stepped and windows pixel-built. Keep small details recognizable without leaving smooth photographic patches.

**Suitable photos:** buildings, streets, villages, forests, fields, mountains, lakes and landscape attractions. **Not for portraits, group photos, pets or animal-themed photos.**

**Example request:**

```text
Use $photo-to-pixel-scan for this building or landscape photo.
Keep the subject and whole frame close to half photo and half pixels.
Use large visible pixel blocks, including on buildings,
a slightly wavy scan and local source colors. Preserve the original photo region.
```

## Keep the original faces

Ask the AI to keep the original face shape, features, expression, glasses and skin color. Check side profiles as well as front-facing faces.

Some skills include a script that places the face directly from the original photo into the result. A written prompt alone does not guarantee the same face. This matters when using an AI tool that can generate images but cannot combine them with the original pixels.

## Download and use

1. On this repository's main page, select **Code → Download ZIP**.
2. Extract the ZIP and open `skills/`.
3. Choose the complete folder for the style you want, keeping its instructions, references and scripts.
4. Import it using your AI tool's supported method.
5. Upload your own original photo and use the example request above.

The full names in the table are the skill names. The simpler section titles describe their styles; they do not rename the folders.

## Find this collection on GitHub

Use the full skill name from the table, such as `photo-to-soft-gradient`. You can also use [this README search](https://github.com/search?q=photo-to-soft-gradient%20in%3Areadme&type=repositories).

GitHub's default repository search checks the repository name, description and topics. To search README text specifically, add `in:readme`. Uploading a README does not change the repository's description or topics.

[GitHub search guide](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)

## What your AI tool needs

It must support skills, view your photos and provide an image generation or editing tool. **A skill supplies instructions; it does not install an image model.** Different models can produce different results.

The two styles with a real photo above generated art also need an ordinary image tool to join the images. Their scripts use Python 3 and Pillow. The paper poster's text script also needs fontTools and a Chinese font. See each skill for its exact requirements.

The pixel-scan helper checks the two sides' area and restores the real photo side. It uses Python 3, Pillow and ImageMagick. This skill excludes portrait and animal subjects.

Without an image tool, ask for a prompt only. Face close-ups, ID photos and exact maps are outside the main use of these artistic styles.

## Add another skill

Create its own folder under `skills/`, add the required `SKILL.md` and supporting files, and add one row to both README tables.

Keep private photos and account information outside this public repository. Include third-party example images only when you have permission to publish them.

## License

Instructions and included code use the [MIT License](LICENSE). User photos and third-party images are not covered by this license.
