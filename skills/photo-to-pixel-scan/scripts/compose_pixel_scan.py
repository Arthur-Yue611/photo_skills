#!/usr/bin/env python3
"""Check a photo/pixel scan plan and restore original photography.

Use an image-generation tool for artwork first. Raster operations use
ImageMagick. Pillow is used only to read and verify.
"""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image

AREA_LOW, AREA_HIGH = 0.45, 0.55


def imagemagick():
    for name in ("magick", "convert"):
        program = shutil.which(name)
        if program:
            check = subprocess.run([program, "-version"], capture_output=True, text=True)
            if check.returncode == 0 and "ImageMagick" in check.stdout:
                return program
    raise ValueError("ImageMagick is required; install its magick command.")


def coordinates(points, minimum, maximum, route=False):
    if not isinstance(points, list) or not minimum <= len(points) <= maximum:
        raise ValueError(f"Use {minimum}–{maximum} points.")
    for p in points:
        if not isinstance(p, list) or len(p) != 2:
            raise ValueError("Each point must be an [x, y] pair.")
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or
               not math.isfinite(v) for v in p):
            raise ValueError("Point coordinates must be finite numbers.")
        if not (0 <= p[0] <= 1 and 0 <= p[1] <= 1):
            raise ValueError("Coordinates must be between 0 and 1.")
        if route and not 0 < p[0] < 1:
            raise ValueError("The scan route needs 0 < x < 1.")
    if route:
        if points[0][1] != 0 or points[-1][1] != 1:
            raise ValueError("The seam must start at y=0 and end at y=1.")
        if any(a[1] >= b[1] for a, b in zip(points, points[1:])):
            raise ValueError("The seam y-coordinates must strictly increase.")


def read_plan(path):
    plan = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict):
        raise ValueError("The plan must be a JSON object.")
    if plan.get("boundary_mode") not in ("scene", "subject"):
        raise ValueError("boundary_mode must be scene or subject.")
    subject = plan.get("complete_subject")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("Describe the complete_subject before assembly.")
    axis = plan.get("boundary_axis", "y")
    if axis not in ("x", "y"):
        raise ValueError("boundary_axis must be x or y.")
    requested_side = plan.get("pixel_side", "right" if axis == "y" else "bottom")
    allowed = ("left", "right") if axis == "y" else ("top", "bottom")
    if requested_side not in allowed:
        raise ValueError("pixel_side must be left/right for y, or top/bottom for x.")
    side = requested_side if axis == "y" else ("left" if requested_side == "bottom" else "right")
    width = plan.get("scan_width", 0.04)
    if isinstance(width, bool) or not isinstance(width, (int, float)):
        raise ValueError("scan_width must be a number.")
    if not math.isfinite(width) or not 0.015 <= width <= 0.05:
        raise ValueError("scan_width must be between 0.015 and 0.05.")
    points = plan.get("points")
    if axis == "x":
        coordinates(points, 2, 50)
        points = [[1 - y, x] for x, y in points]
    coordinates(points, 2, 50, route=True)
    outlines = plan.get("subject_polygons", [])
    if not isinstance(outlines, list) or len(outlines) > 30:
        raise ValueError("subject_polygons must be a list of up to 30 outlines.")
    for outline in outlines:
        coordinates(outline, 3, 300)
    if plan["boundary_mode"] == "subject" and not outlines:
        raise ValueError("Provide the actual subject silhouette in subject_polygons.")
    if axis == "x":
        outlines = [[[1 - y, x] for x, y in outline] for outline in outlines]
    return plan, side, float(width), points, outlines


def read_rgb(path):
    with Image.open(path) as image:
        image.load()
        return image.size, image.convert("RGB").tobytes()


def read_mask(path):
    with Image.open(path) as image:
        image.load()
        return image.convert("L").tobytes()


def drawing(points, width, height):
    return "polygon " + " ".join(
        f"{round(x * (width - 1))},{round(y * (height - 1))}" for x, y in points
    )


def execute(args):
    source = args.source.resolve()
    plan_file = args.plan.resolve()
    for path in (source, plan_file):
        if not path.is_file():
            raise ValueError(f"Input is not a regular file: {path}")
    if args.check_plan:
        art = output = report_path = None
    else:
        if args.art is None or args.output is None:
            raise ValueError("Assembly requires --art and --output.")
        art = args.art.resolve()
        output = args.output.resolve()
        if not art.is_file():
            raise ValueError("Artwork is not a regular file.")
        if output in (source, art, plan_file):
            raise ValueError("Keep the output separate from all inputs.")
        if output.suffix.lower() != ".png":
            raise ValueError("Use a .png output to retain source pixels.")
        report_path = output.with_suffix(".verification.json")
        if output.exists() or report_path.exists():
            raise ValueError("Use a new output filename; existing versions are preserved.")
        output.parent.mkdir(parents=True, exist_ok=True)
    plan, side, scan_fraction, points, outlines = read_plan(plan_file)
    program = imagemagick()

    def run(*parts):
        result = subprocess.run([program, *map(str, parts)],
                                capture_output=True, text=True)
        if result.returncode:
            raise ValueError("ImageMagick failed: " + result.stderr.strip())

    with tempfile.TemporaryDirectory(prefix="photo-pixel-scan-") as work:
        temp = Path(work)
        original = temp / "source.miff"
        source_ref = temp / "source.png"
        axis = plan.get("boundary_axis", "y")
        orient = ["-rotate", "90"] if axis == "x" else []
        run(source, "-auto-orient", *orient, "-depth", "8", original)
        run(original, "PNG24:" + str(source_ref))
        (w, h), original_bytes = read_rgb(source_ref)

        route = [(round(x * (w - 1)), round(y * (h - 1))) for x, y in points]
        edge = w - 1 if side == "right" else 0
        polygon = route + [(edge, h - 1), (edge, 0)]
        material = temp / "material.miff"
        draw = "polygon " + " ".join(f"{x},{y}" for x, y in polygon)
        run("-size", f"{w}x{h}", "xc:black", "-fill", "white", "-draw", draw,
            "-alpha", "off", "-type", "Grayscale", "-depth", "8", material)
        material_png = temp / "material.png"
        run(material, material_png)
        material_bytes = read_mask(material_png)
        pixel_fraction = sum(material_bytes) / (255 * w * h)
        subject_fraction = None
        if outlines:
            subject_mask = temp / "subject.png"
            draws = " ".join(drawing(outline, w, h) for outline in outlines)
            run("-size", f"{w}x{h}", "xc:black", "-fill", "white",
                "-draw", draws, "-alpha", "off", "-type", "Grayscale",
                "-depth", "8", subject_mask)
            subject_bytes = read_mask(subject_mask)
            subject_area = sum(subject_bytes)
            if subject_area == 0:
                raise ValueError("The supplied subject outlines enclose no area.")
            subject_fraction = sum(a * b for a, b in
                                   zip(material_bytes, subject_bytes)) / (255 * subject_area)
        frame_ok = AREA_LOW <= pixel_fraction <= AREA_HIGH
        subject_ok = (AREA_LOW <= subject_fraction <= AREA_HIGH
                      if subject_fraction is not None else None)
        areas = {
            "source": source.name,
            "size": [h, w] if axis == "x" else [w, h],
            "boundary_mode": plan["boundary_mode"],
            "complete_subject": plan["complete_subject"],
            "pixel_side": plan.get("pixel_side", "right" if axis == "y" else "bottom"),
            "boundary_axis": axis,
            "frame_pixel_fraction": pixel_fraction,
            "frame_photo_fraction": 1 - pixel_fraction,
            "frame_balance_ok": frame_ok,
            "subject_pixel_fraction": subject_fraction,
            "subject_photo_fraction": (1 - subject_fraction
                                       if subject_fraction is not None else None),
            "subject_balance_ok": subject_ok,
            "subject_measurement": "supplied silhouette" if outlines else "visual review required",
            "target_range": [AREA_LOW, AREA_HIGH]
        }
        if args.check_plan:
            print(json.dumps(areas, ensure_ascii=False, indent=2))
            return
        if subject_ok is False or (not frame_ok and not args.allow_imbalance):
            raise ValueError(
                "Area balance needs revision: " + json.dumps(areas, ensure_ascii=False) +
                ". Adjust angle and position through the subject and background while retaining the subject's half-and-half area ratio; "
                "regenerate mismatched artwork before assembly."
            )

        with Image.open(art) as image:
            aw, ah = image.size
            if getattr(image, "n_frames", 1) != 1:
                raise ValueError("Use one artwork image, not an animation.")
            if image.getexif().get(274) in (5, 6, 7, 8):
                aw, ah = ah, aw
        if axis == "x":
            aw, ah = ah, aw
        if abs((aw / ah) / (w / h) - 1) > 0.01:
            raise ValueError("Artwork aspect ratio differs; correct its framing first.")
        scaled = temp / "art.miff"
        run(art, "-auto-orient", *orient, "-filter", "point", "-resize", f"{w}x{h}!",
            "-depth", "8", scaled)

        band = temp / "scan-band.miff"
        sigma = max(0.5, (h if axis == "x" else w) * scan_fraction / 4.652)
        run(material, "-alpha", "off", "-blur", f"0x{sigma:.4f}",
            "(", "-clone", "0", "-threshold", "1%", ")",
            "(", "-clone", "0", "-threshold", "99%", ")",
            "-delete", "0", "-compose", "Difference", "-composite",
            "-alpha", "off", "-type", "Grayscale", "-depth", "8", band)
        lights = temp / "scan-lights.miff"
        run(scaled, "-alpha", "off", "-channel", "RG", "-separate", "+channel",
            "-evaluate-sequence", "Min", "-level", "90%,98%", band,
            "-alpha", "off", "-compose", "Multiply", "-composite",
            "-alpha", "off", "-type", "Grayscale", "-depth", "8", lights)
        alpha = temp / "alpha.png"
        run(material, "-alpha", "off", "-blur", "0x1", lights,
            "-evaluate-sequence", "Max", "-alpha", "off", "-type", "Grayscale",
            "-depth", "8", alpha)
        layer = temp / "layer.miff"
        run(scaled, alpha, "-alpha", "off", "-compose", "CopyOpacity",
            "-composite", layer)
        ready = temp / "ready.png"
        run(original, layer, "-compose", "Over", "-composite",
            "-depth", "8", "PNG24:" + str(ready))
        size, finished_bytes = read_rgb(ready)
        if size != (w, h):
            raise ValueError("The result no longer matches the source size.")
        mask_bytes = read_mask(alpha)
        kept = 0
        for i, opacity in enumerate(mask_bytes):
            if opacity == 0:
                kept += 1
                offset = i * 3
                if original_bytes[offset:offset + 3] != finished_bytes[offset:offset + 3]:
                    raise ValueError("Untouched photography changed; output was not saved.")
        if kept == 0:
            raise ValueError("No original photographic region remained.")
        report = dict(areas, art=art.name, scan_width_fraction=scan_fraction,
                      untouched_photo_pixels=kept, untouched_photo_matches_source=True,
                      imbalance_override_used=bool(args.allow_imbalance and not frame_ok),
                      note="Region areas follow the seam before glow. Subject areas depend on the supplied outlines. Deliberate scan overlays are excluded from the untouched-pixel check.")
        handle, stage_name = tempfile.mkstemp(prefix=".pixel-scan-", suffix=".png",
                                              dir=output.parent)
        os.close(handle)
        staged = Path(stage_name)
        try:
            if axis == "x":
                run(ready, "-rotate", "-90", "PNG24:" + str(staged))
            else:
                shutil.copyfile(ready, staged)
            read_rgb(staged)
            os.replace(staged, output)
        finally:
            staged.unlink(missing_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    print(json.dumps({"output": str(output), "verification": str(report_path),
                      "untouched_photo_matches_source": True,
                      "frame_balance_ok": frame_ok,
                      "subject_balance_ok": subject_ok}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--art", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-plan", action="store_true",
                        help="Measure frame/subject regions without generating or assembling art.")
    parser.add_argument("--allow-imbalance", action="store_true",
                        help="Allow a reviewed frame imbalance; never bypass a failed subject balance.")
    args = parser.parse_args()
    try:
        execute(args)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    main()
