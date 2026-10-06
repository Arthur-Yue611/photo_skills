# Photo Skills

Reusable AI skills for photo editing, creative transformations, and visual storytelling.

[中文说明](README.zh-CN.md) · [Available skills](#available-skills) · [Install](#install) · [License](LICENSE)

This repository is a growing collection. Each skill lives in its own folder under `skills/` and can be installed independently. Start with one skill; add more as the collection grows.

## Available skills

| Skill | What it does | Folder |
| --- | --- | --- |
| **Photo-to-Sketch Storytelling** | Extends a real photo into delicate hand-drawn imagery on warm ivory paper, with a miniature character participating in the scene. | [photo-to-sketch-storytelling](skills/photo-to-sketch-storytelling/SKILL.md) |
| **Photo-to-Watercolor Journal** | Converts travel photos into fine-pen watercolor journal pages with original proportions, atmosphere-matched paper, four solid source-color swatches and handwritten English captions. | [photo-to-watercolor-journal](skills/photo-to-watercolor-journal/SKILL.md) |

## Photo-to-Sketch Storytelling

Keep the upper part photographic. Continue an actual element from the photo into fine pencil or ink linework below. Add restrained color from the original image and a small character with a clear physical action.

The workflow designs a story from three connected parts:

| Photo element | Transformation | Character action |
| --- | --- | --- |
| A hanging scarf | A knitted path | Walks up a fold or lays out its edge |
| A woven twig ring | A winding bridge or small boat | Weaves loose strands or pushes with a pole |
| Moving leaves and tree shadows | A curling ribbon of forest breeze | Winds it onto a reel |

The default is a **2:3 portrait**, warm ivory paper, fine linework and light watercolor or colored pencil. The story, palette and transition are chosen from the uploaded photo. You can override the aspect ratio, style, character count or story.

### Included resources

| File | Purpose |
| --- | --- |
| [`SKILL.md`](skills/photo-to-sketch-storytelling/SKILL.md) | The complete agent workflow and trigger metadata |
| [`agents/openai.yaml`](skills/photo-to-sketch-storytelling/agents/openai.yaml) | English display name and invocation metadata |
| [`references/prompt-template.md`](skills/photo-to-sketch-storytelling/references/prompt-template.md) | Editable prompt structure and revision template |
| [`references/story-patterns.md`](skills/photo-to-sketch-storytelling/references/story-patterns.md) | Source-element, transformation and action patterns |
| [`references/quality-checks.md`](skills/photo-to-sketch-storytelling/references/quality-checks.md) | Checks for identities, continuity, character contact and visual style |

The trigger metadata is bilingual; the detailed workflow and references are currently written in Chinese. A multilingual agent can follow them and respond in your language.

## Photo-to-Watercolor Journal

Turn the entire photo scene into a fine-pen and soft-watercolor travel journal illustration. Keep the original aspect ratio. Let irregular painted edges fade into paper whose tone follows the scene: warm for sunlit scenes, cool for cool landscapes, and deeper blue-grey for night scenes.

Add exactly four rounded square **solid-color** swatches drawn from the original photo at the lower right, plus one handwritten English title and one short sentence beneath it. No borders, split panels, stickers or miniature characters.

**Best suited to:** streets, buildings, city skylines, waterfronts, trains and stations, blue-hour and night scenes, mountains, countryside and other travel landscapes. Environmental travel portraits and group photos can also be illustrated, with care for faces and clothing. ID photos, product catalogs and technical maps are outside the intended use.

Use:

```text
Use $photo-to-watercolor-journal to illustrate this photo as a travel journal.
Keep its aspect ratio, use four solid source-color swatches,
and add a handwritten English title and short sentence.
```

Install the complete `skills/photo-to-watercolor-journal` folder in the same way as the first skill. It includes prompt and quality-check references, and an optional `scripts/extract_palette.py` helper. The helper needs Pillow and returns four representative colors present in the original source pixels; without it, the agent can choose colors visually. Generated swatches may still differ from exact RGB values, and handwritten text needs visual verification. Installing the skill does not provide an image model.

## Requirements

Use an agent host that supports Agent Skills and can view your uploaded photo. To produce an image, the host also needs an image generation or editing tool. **Installing this skill does not install an image model or grant image-tool access.**

Without an image editor, the skill can prepare a complete prompt for a tool you use elsewhere. It contains no external API runner, credentials or model-specific dependency.

## Install

### Use a skill installer

In a Codex environment with `$skill-installer`, ask:

```text
$skill-installer Install the photo-to-sketch-storytelling skill from
https://github.com/Arthur-Yue611/photo_skills
at skills/photo-to-sketch-storytelling.
```

### Download or clone

Download this repository with **Code → Download ZIP**, or clone it:

```bash
git clone https://github.com/Arthur-Yue611/photo_skills.git
```

Copy the **complete** `skills/photo-to-sketch-storytelling` folder to a supported skill directory in your host. For local Codex, the documented user skill directory is `~/.agents/skills/`; repository-scoped skills live under `.agents/skills/` in the target project. Copy the folder, including its references and icon, rather than only `SKILL.md`.

For hosts with a skill import or upload flow, follow that host's supported installation method. This GitHub repository is a source distribution; it is not automatically a listing in a public plugin directory.

Official guidance: [Build skills](https://learn.chatgpt.com/docs/build-skills).

## Use

Upload your own photo and invoke the installed skill:

```text
Use $photo-to-sketch-storytelling to turn this photo into a portrait artwork
that blends real photography with delicate hand-drawn storytelling.
Choose a natural extension element and add one miniature character
performing a clear action.
```

In ChatGPT, select the installed skill using `@`. In Codex CLI or an IDE extension, mention it with `$`.

You can also ask for:

- **Prompt only:** “Use this skill to prepare a final prompt; do not generate an image.”
- **Multiple photos:** “Create one independent artwork for each of these photos.”
- **A revision:** “Keep this composition and fix only the little character's hand contact.”

Generative editing may redraw faces or details. The workflow checks for these changes and asks for targeted fixes where possible; it does not promise pixel-perfect preservation.

## Add another skill

1. Create `skills/your-skill-name/` with its own `SKILL.md`.
2. Include a lowercase, hyphenated `name` and a clear `description` in YAML front matter.
3. Add only the references, assets or scripts needed for that skill.
4. Add its name, purpose and relative folder link to the tables in both README files.
5. Validate and try it on a realistic task before publishing.

Keep personal photos, credentials and generated private outputs outside the repository. Only include sample images that you have chosen to share and have permission to distribute.

## License

The instructions, documentation and bundled icon are distributed under the [MIT License](LICENSE). The license does not cover user-uploaded photos or grant rights to third-party image inputs.
