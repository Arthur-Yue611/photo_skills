---
name: photo-to-pixel-scan
description: >-
  Blend architecture or scenery photos with coarse 2D pixel art and a complete glowing pixel scan boundary. Use for photo-to-pixel fusion, pixel scanning, buildings, streets, villages, forests, flowers, mountains, lakes, prompt writing, batches and revisions. Keep the complete subject and whole frame near half photo, half pixels; use a nearly straight curve with only tiny smooth waves, local scan colors and visibly pixel-painted buildings. 将建筑与风景照片制作成原片与二维像素融合的扫描作品；大方块、轻微起伏分界、局部景物配色、主体和整图尽量对半。适合建筑、街景、乡村、树林、山湖与气球形景观，不用于人像、合照、宠物、动物主题、MC三维方块、普通马赛克、对比拼图、地图或视频。
---

# Photo to Pixel Scan

Create one continuous photo/pixel artwork per original. Keep the original aspect ratio, framing and scene geometry. Use the latest approved treatment as the default: coarse square pixel art, clearly pixel-painted architecture and a glowing scanner with tiny smooth undulations.

## Inspect and identify the complete subject

View each actual original before planning. Use screenshots and approved outputs only as style references. If the original is unavailable, ask for it again; do not substitute an earlier generated image or invent a source scene.

Read [references/scene-guide.md](references/scene-guide.md). Treat an entire facade or building complex as one subject, including roofs, towers, pavilions, walls and stairs. Do not select only its tallest section. For scenery without a separate subject, divide the whole view. For an isolated attraction or small building, divide the object itself and extend that same boundary through the surroundings.

Exclude portrait, group-photo, pet and animal-theme requests. Preserve incidental figures and their locations in supported scenery. Keep any recognizable face wholly in the original-photo region. If that is incompatible with the division, request another source rather than repaint the face or leave a photographic island in the pixel region.

## Plan one balanced division

Keep one connected photograph region and one connected pixel region. Aim for approximately 45–55 percent per side for BOTH the complete subject and the entire frame. Estimate the actual visible subject silhouette, not a rectangle containing empty sky.

Adjust the boundary's position and angle without moving, stretching or cropping the subject. Use top-to-bottom or left-to-right crossings as appropriate; neither orientation is fixed. For an off-center subject, consider a shallow diagonal across the frame instead of extending its centerline vertically. A left-to-right crossing still divides one continuous scene; never make separate stacked panels.

Use a nearly straight CURVE with only slight, smooth, low-amplitude waviness. Keep the overall direction simple. Reject a ruler-straight divider, angular polyline, abrupt kink at a roof, large S-curve, loop or object outline. Fit scene features only when this does not distort that simple route. Do not confuse stair-step pixel edges with a bent overall boundary.

Record the source, complete subject, region orientation, proposed route and both area estimates. Read [references/composition.md](references/composition.md) and run the helper's plan check before generating. If a natural route cannot balance both, prioritize the subject split and state the remaining frame imbalance; do not introduce sharp turns to force exact equality.

## Make every pixel-side object visibly pixel art

Use large, crisp, flat square cells, grouped source colors and stair-step outlines. Default to about 20 percent larger cell side lengths than the earlier baseline; when revising the previous 30 percent version, target 1.20/1.30 (about 92.3 percent) of its artwork cell side lengths. Apply this only to artwork pixels, not scanner grains. Accept some loss of fine detail. Read [references/pixel-size.md](references/pixel-size.md) for scale guides.

Make broad walls, roofs and towers as visibly pixel-painted as the surrounding grass and sky. Replace plaster grain, tiny painterly facets, smooth arches and thin realistic window bars with coarse square shading clusters and stepped forms. Keep recognizable structure, proportions, window and door positions, core colors and perspective. Use somewhat smaller, still visible cells for identity-bearing details; never exempt buildings or small furniture from pixel treatment.

Group neighboring cells into deliberate shapes and light/shadow masses. Use a consistent square unit and integer-multiple clusters. Keep foreground forms clearer and distant masses simpler; allow quiet sky and wall areas without drawing an artificial grid. Avoid random checkerboards, camouflage-like fragments and tiny polygon facets.

Use the original lighting direction and palette. Do not copy style-reference clouds, objects or buildings. Clear source skies must remain clear. Do not leave smooth painterly architecture or photographic patches inside the pixel region. Do not produce blurred mosaic, voxel models, plastic surfaces or Minecraft cubes.

## Preserve the approved scan treatment

Build one complete visible front from neighboring luminous square cells, short square-cell trails and a few nearby glints. Keep its breadth and brightness consistent with an approved reference when provided. Without a reference, start around 3–4 percent of image width and inspect at full-frame size; numeric guides are not exact generation guarantees.

Match colors locally as the route passes through the scene: red at red walls, yellow at yellow walls, blue at sky or water, ivory at clouds, green at grass and turquoise at turquoise surfaces. Combine these along the scan rather than applying one global neon or rainbow color. Use a thin bright core, medium translucent colored squares and a few smaller outer glints. Keep color visible through the transparency. Start near 0.4–0.5 percent image width for the bright core and 3–4 percent for the entire scan, then judge the image at normal viewing size. These are guides, not exact generation guarantees. Allow a few pale highlights, never a continuous blown-out white ribbon. Keep highlights concentrated near the front, without broad haze, a neon tube, smoke or stars.

On a targeted revision, change only the requested treatment. If the user approved the scanner and requests stronger building pixels, keep scanner route, waves, colors, width and brightness fixed. For a grain-only revision, restore the complete approved scan band and photographic region from the previous output after generation; verify that their pixels are unchanged. Preserve approved versions under separate filenames; do not overwrite them.

## Generate, restore the source and check

Use [references/prompt-template.md](references/prompt-template.md) to write a filled scene-specific prompt. Use the available image-generation/editing tool. Generate one image per original, never a grid.

Read [references/staged-workflow.md](references/staged-workflow.md) when the generated route misses the plan, changes the subject balance, or repeated full-image edits alter the scene. After one targeted route correction fails, switch to that staged workflow instead of repeatedly requesting the same full-image edit.

Inspect the actual generated route, source geometry, buildings and small objects. Recheck both area balances using the actual route. Correct added clouds, extra structures, unchanged buildings or missing objects before assembly; an accurate proposal does not prove the model followed it.

Restore the actual original photographic region using the reviewed route and the helper, or an equivalent source-preserving compositor. A prompt alone cannot guarantee unchanged photography. Do not shift a mask across incorrectly generated art to hide a wrong division. Inspect the complete scan after assembly; restore clipped colored cells with a reviewed scan mask if needed. The helper's automatic brightness gate is not a semantic scanner detector.

Never enhance, recolor or regenerate the complete assembled image afterward. If source restoration is unavailable, label the output a generated preview and disclose that the photographic side has not been verified as unchanged.

Read [references/quality-checks.md](references/quality-checks.md) before delivery. Report the actual result and remaining limitations without claiming universal robustness from a few examples. A skill supplies instructions, not an image model. If no image tool is available, supply a prompt and state that no image was generated.

Keep private photos, generated personal examples and third-party screenshots out of public skill files unless the user specifically authorizes publication.
