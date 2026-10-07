#!/usr/bin/env python3
"""Place an actual source crop above gradient art; optionally restore source faces.

Requires Python 3 and Pillow>=10. Does not generate art or detect faces.
Face targets use coordinates within the final-sized LOWER panel.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps


def opaque_rgb(path):
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened)
        icc = image.info.get("icc_profile")
        if image.mode == "RGBA":
            if image.getextrema()[3] != (255, 255):
                raise ValueError("Transparent inputs are unsupported; provide opaque RGB.")
            image = image.convert("RGB")
        elif image.mode != "RGB":
            raise ValueError(f"Expected RGB input, got {image.mode}; no color conversion is applied.")
        return image.copy(), icc


def crop_rect(size, box, fx, fy):
    width, height = size
    if box:
        left, top, right, bottom = box
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise ValueError("Photo crop must lie inside the oriented source.")
        if (right-left)*9 != (bottom-top)*16:
            raise ValueError("Explicit photo crop must have exact 16:9 proportions.")
        return tuple(box)
    unit = min(width//16, height//9)
    if unit < 1:
        raise ValueError("Photo is too small for an integer-pixel 16:9 crop.")
    cw, ch = 16*unit, 9*unit
    left = max(0, min(width-cw, round(fx*width-cw/2)))
    top = max(0, min(height-ch, round(fy*height-ch/2)))
    return left, top, left+cw, top+ch


def frame_art(image, size, fx, fy, allow_crop):
    ratio = size[0]/size[1]
    if image.width/image.height > ratio:
        cw, ch = max(1, round(image.height*ratio)), image.height
    else:
        cw, ch = image.width, max(1, round(image.width/ratio))
    removed = 1-(cw*ch)/(image.width*image.height)
    if removed > .15 and not allow_crop:
        raise ValueError(f"Lower-art framing would remove {removed:.1%}; review and regenerate near 144:175.")
    left = max(0, min(image.width-cw, round(fx*image.width-cw/2)))
    top = max(0, min(image.height-ch, round(fy*image.height-ch/2)))
    box = (left, top, left+cw, top+ch)
    return image.crop(box).resize(size, Image.Resampling.LANCZOS), box, removed


def point(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(name+" needs two coordinates.")
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in value):
        raise ValueError(name+" needs finite numeric coordinates.")
    return value


def polygon(points, size, name):
    if not isinstance(points, list) or len(points) < 3:
        raise ValueError(name+" needs at least three points.")
    for item in points:
        x, y = point(item, name)
        if not (0 <= x < size[0] and 0 <= y < size[1]):
            raise ValueError(name+" is outside the oriented source.")
    mask = Image.new("L", size)
    ImageDraw.Draw(mask).polygon([tuple(p) for p in points], fill=255)
    if not mask.getbbox():
        raise ValueError(name+" has no pixels.")
    return mask


def restore_faces(lower, source, manifest):
    faces = manifest.get("faces")
    if not isinstance(faces, list) or not faces:
        raise ValueError("Face JSON must contain a nonempty faces array.")
    result = lower.copy()
    union = Image.new("L", lower.size)
    expected = []
    for index, face in enumerate(faces, 1):
        scale = float(face["scale"])
        feather = float(face.get("feather", 5))
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError("Face scale must be positive and finite.")
        if not math.isfinite(feather) or feather < 0:
            raise ValueError("Face feather must be finite and nonnegative.")
        source_anchor = point(face["source_anchor"], "source_anchor")
        target_anchor = point(face["target_anchor"], "target_anchor")
        tx = target_anchor[0]-scale*source_anchor[0]
        ty = target_anchor[1]-scale*source_anchor[1]
        outer = polygon(face["outer"], source.size, "outer")
        core = polygon(face["core"], source.size, "core")
        if ImageChops.subtract(core, outer).getbbox():
            raise ValueError("Face core must lie inside outer.")
        for x, y in face["core"]:
            if not (0 <= scale*x+tx < lower.width and 0 <= scale*y+ty < lower.height):
                raise ValueError("Face core would be clipped by the lower panel.")
        matrix = (1/scale, 0, -tx/scale, 0, 1/scale, -ty/scale)
        warped = source.transform(lower.size, Image.Transform.AFFINE, matrix, Image.Resampling.BICUBIC)
        transformed_core = core.transform(lower.size, Image.Transform.AFFINE, matrix, Image.Resampling.NEAREST)
        if not transformed_core.getbbox():
            raise ValueError("Face core has no pixels at the output size.")
        if ImageChops.multiply(transformed_core, union).getbbox():
            raise ValueError("Face cores overlap; review placement.")
        alpha = ImageChops.lighter(outer.filter(ImageFilter.GaussianBlur(feather)), core)
        alpha = alpha.transform(lower.size, Image.Transform.AFFINE, matrix, Image.Resampling.BILINEAR)
        alpha = ImageChops.lighter(alpha, transformed_core)
        result = Image.composite(warped, result, alpha)
        union = ImageChops.lighter(union, transformed_core)
        expected.append((transformed_core, warped, {"face": index, "scale": scale, "source_core_preserved": True}))
    for core, warped, _ in expected:
        if Image.composite(ImageChops.difference(result, warped), Image.new("RGB", result.size), core).getbbox():
            raise ValueError("Protected face was changed by another face mask.")
    return result, expected


def save_verified(final, top, face_expected, photo_height, output, icc):
    temporary = None
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd, name = tempfile.mkstemp(prefix=output.stem+"-", suffix=".png", dir=output.parent)
        temporary = Path(name)
        with os.fdopen(fd, "wb") as file:
            final.save(file, format="PNG", **({"icc_profile": icc} if icc else {}))
            file.flush()
            os.fsync(file.fileno())
        with Image.open(temporary) as saved:
            saved.load()
            if saved.mode != "RGB" or saved.size != final.size or saved.tobytes() != final.tobytes():
                raise ValueError("Saved PNG does not match the composed image.")
            actual_top = saved.crop((0, 0, top.width, photo_height))
            if actual_top.tobytes() != top.tobytes():
                raise ValueError("Saved top pixels do not match the resized source crop.")
            if face_expected:
                actual_lower = saved.crop((0, photo_height, saved.width, saved.height))
                for core, warped, _ in face_expected:
                    if Image.composite(ImageChops.difference(actual_lower, warped), Image.new("RGB", actual_lower.size), core).getbbox():
                        raise ValueError("Saved lower face core does not match the transformed source.")
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--art", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--width", type=int, default=1152, help="Positive multiple of 144.")
    parser.add_argument("--crop-box", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--focus-x", type=float, default=.5)
    parser.add_argument("--focus-y", type=float, default=.5)
    parser.add_argument("--art-focus-x", type=float, default=.5)
    parser.add_argument("--art-focus-y", type=float, default=.5)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--faces", type=Path, help="Reviewed source masks and final lower-panel positions.")
    parser.add_argument("--allow-art-crop", action="store_true", help="Only after inspecting the lower crop.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        if args.width <= 0 or args.width % 144:
            raise ValueError("Width must be a positive multiple of 144.")
        if any(not math.isfinite(v) or not 0 <= v <= 1 for v in (args.focus_x, args.focus_y, args.art_focus_x, args.art_focus_y)):
            raise ValueError("Focus coordinates must be finite values from 0 to 1.")
        if args.output.suffix.lower() != ".png":
            raise ValueError("Use .png output for lossless verification.")
        inputs = [p.resolve() for p in (args.source, args.art, args.faces) if p is not None]
        if args.output.resolve() in inputs:
            raise ValueError("Output must not replace any input.")
        if args.output.exists() and not args.overwrite:
            raise ValueError("Output exists; choose another name or use --overwrite.")
        if args.prepare_only and (args.art or args.faces):
            raise ValueError("Do not combine --prepare-only with art or faces.")
        if not args.prepare_only and not args.art:
            raise ValueError("Supply --art or use --prepare-only.")
        source, icc = opaque_rgb(args.source)
        width, height = args.width, args.width*16//9
        photo_height = args.width*9//16
        box = crop_rect(source.size, args.crop_box, args.focus_x, args.focus_y)
        top = source.crop(box).resize((width, photo_height), Image.Resampling.LANCZOS)
        expected = []
        report = {
            "mode": "preview" if args.prepare_only else "final",
            "canvas_size": [width, height],
            "photo_size": [width, photo_height],
            "art_size": [width, height-photo_height],
            "photo_crop_box": list(box),
            "photo_operations": ["EXIF display orientation", "crop", "uniform resize"],
            "top_rgb_sha256": hashlib.sha256(top.tobytes()).hexdigest()
        }
        if args.prepare_only:
            final = top
        else:
            art, art_icc = opaque_rgb(args.art)
            if icc and art_icc and art_icc != icc:
                raise ValueError("Source and art have different ICC profiles; review the art color space.")
            lower, art_box, removed = frame_art(art, (width, height-photo_height), args.art_focus_x, args.art_focus_y, args.allow_art_crop)
            if args.faces:
                manifest = json.loads(args.faces.read_text(encoding="utf-8"))
                if not isinstance(manifest, dict):
                    raise ValueError("Face JSON must be an object.")
                lower, expected = restore_faces(lower, source, manifest)
            final = Image.new("RGB", (width, height))
            final.paste(lower, (0, photo_height))
            final.paste(top, (0, 0))
            report.update(art_crop_box=list(art_box), art_crop_fraction=removed)
        save_verified(final, top, expected, photo_height, args.output, icc)
        report.update(output=str(args.output), top_pixels_verified=True,
                      face_checks=[item[2] for item in expected], saved_png_verified=True)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()

