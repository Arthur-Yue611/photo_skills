# Check areas and restore the actual photo

Use an image tool to generate the artwork. The helper checks proposed areas and combines artwork with the original; it does not generate pixel art.

Use Python 3, Pillow and ImageMagick. Install Pillow from `requirements.txt`. Pillow only reads and verifies images here; ImageMagick performs assembly. Use `magick`, or ImageMagick's `convert` on older systems, not the unrelated Windows system command.

## Plan in original image coordinates

Express all coordinates as fractions of the original width and height. Keep points in route order and use enough to approximate the tiny smooth waves. These are illustrative plans, not required routes.

Top-to-bottom route:

```json
{
  "boundary_mode": "scene",
  "complete_subject": "the whole village row",
  "boundary_axis": "y",
  "pixel_side": "right",
  "scan_width": 0.04,
  "points": [[0.48, 0.0], [0.47, 0.25], [0.46, 0.50], [0.45, 0.75], [0.44, 1.0]]
}
```

For `boundary_axis: "y"`, start at y=0, end at y=1 and strictly increase y. Use `pixel_side: "left"` or `"right"`. Omitting the axis retains this original format.

Left-to-right route:

```json
{
  "boundary_mode": "subject",
  "complete_subject": "the whole balloon-shaped attraction",
  "boundary_axis": "x",
  "pixel_side": "bottom",
  "scan_width": 0.04,
  "points": [[0.0, 0.40], [0.25, 0.445], [0.50, 0.49], [0.75, 0.537], [1.0, 0.58]],
  "subject_polygons": [[[0.28, 0.175], [0.42, 0.28], [0.447, 0.46], [0.32, 0.802], [0.22, 0.805], [0.115, 0.48], [0.15, 0.26]]]
}
```

For `boundary_axis: "x"`, start at x=0, end at x=1 and strictly increase x. Use `pixel_side: "top"` or `"bottom"`. The helper rotates only its internal work coordinates and returns the output to the original orientation. A left-to-right scanner divides the continuous source scene; it does not create two separate panels.

For a separate subject, supply `subject_polygons` outlining its actual silhouette. For a wide building complex, outline the complete architecture when checking its area, not only a tower. Do not count empty sky inside a bounding rectangle as subject area. Subject areas depend on the accuracy of these outlines; otherwise the report leaves that check for visual review.

## Check before generation

```bash
python scripts/compose_pixel_scan.py --source original.jpg --plan reviewed-plan.json --check-plan
```

Read both frame and subject area results. Aim for 45–55 percent per region as a working range. Adjust position and angle while preserving a nearly straight route with tiny smooth waves. Do not use a sharp bend to force the ratio.

After generation, trace the actual boundary and repeat this check. Do not move a mask over an incorrect art division or treat a passing proposal as proof about the generated image.

## Restore and verify

```bash
python scripts/compose_pixel_scan.py --source original.jpg --art generated.png --plan reviewed-plan.json --output final.png
```

The helper preserves source orientation and ratio, uses sharp sampling on the artwork, assembles the reviewed pixel region and scan, checks untouched photographic pixels against the original, and saves a separate verification report. It never overwrites inputs or an existing output.

Its scan extraction uses a brightness gate, which can miss colored cells or mistake bright surfaces for scanner light. Inspect the actual result. If it clips scan cells, creates a second hard cut or exposes an incorrect join, correct the art/route or use an equivalent compositor with a manually reviewed scan mask and repeat the original-pixel check. Do not accept the join solely because a report passed.

Use `--allow-imbalance` only after reviewing a balanced subject for which no simple natural route can also balance the frame. It permits a remaining frame imbalance, not a failed subject check. State that remaining imbalance.

Only original pixels outside the deliberate pixel and scan edit are checked as unchanged. Never claim exact preservation inside the edited scan itself. Never send the assembled final through a whole-image generator or filter. If exact source restoration is unavailable, return a generated preview with that limitation stated.
