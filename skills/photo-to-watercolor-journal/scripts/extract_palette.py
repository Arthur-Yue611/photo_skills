#!/usr/bin/env python3
"""Pick four representative colors that are actual source RGB pixels.

Requires Pillow. Quantization groups sampled pixels; returned colors are source
medoids rather than generated centroid colors. Supply an original opaque photo,
not a UI/style screenshot. Source files are never modified.
"""
import argparse
import json
import math
from collections import Counter

from PIL import Image, ImageOps


def extract(path):
    with Image.open(path) as opened:
        rgb = ImageOps.exif_transpose(opened).convert("RGBA")
        width, height = rgb.size
        step = max(1, math.ceil(math.sqrt(width * height / 50000)))
        pixels = [rgb.getpixel((x, y))[:3]
                  for y in range(0, height, step)
                  for x in range(0, width, step)
                  if rgb.getpixel((x, y))[3] == 255]
    if not pixels:
        raise ValueError("No fully opaque source pixels; supply an opaque photo.")
    counts = Counter(pixels)
    if len(counts) < 4:
        raise ValueError("Source has fewer than four distinct sampled RGB colors.")
    sample = Image.new("RGB", (len(pixels), 1))
    sample.putdata(pixels)
    grouped = sample.quantize(colors=12, method=Image.Quantize.MEDIANCUT)
    groups = {}
    for label, color in zip(grouped.getdata(), pixels):
        groups.setdefault(label, []).append(color)
    candidates = []
    for members in groups.values():
        mean = tuple(sum(p[c] for p in members) / len(members) for c in range(3))
        actual = min(set(members), key=lambda p: (
            sum((p[c] - mean[c]) ** 2 for c in range(3)), p))
        candidates.append((actual, len(members)))
    candidates.sort(key=lambda item: (-item[1], item[0]))
    picked = [candidates.pop(0)]
    while len(picked) < 4 and candidates:
        # Combine source coverage and distance from already chosen colors.
        index = max(range(len(candidates)), key=lambda i: (
            math.sqrt(candidates[i][1]) * min(
                math.dist(candidates[i][0], p[0]) for p in picked),
            candidates[i][0]))
        candidate = candidates.pop(index)
        if candidate[0] not in [p[0] for p in picked]:
            picked.append(candidate)
    if len(picked) < 4:
        for color, frequency in counts.most_common():
            if color not in [p[0] for p in picked]:
                picked.append((color, frequency))
                if len(picked) == 4:
                    break
    return {
        "aspect_ratio": {"width": width, "height": height},
        "method": "source pixels grouped by median cut; source medoids",
        "colors": [{"hex": "#%02X%02X%02X" % color,
                    "rgb": list(color)} for color, _ in picked],
        "note": "Representative candidates; generation may not match exact RGB."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", help="Original opaque photo, not a UI screenshot")
    args = parser.parse_args()
    try:
        print(json.dumps(extract(args.photo), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    main()
