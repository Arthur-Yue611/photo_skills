#!/usr/bin/env python3
"""Add editorial type and optional source facial cores to a finished 3:4 art base.

Requires Pillow>=10 and fonttools>=4. No generation, face detection or API calls.
Coordinates in face JSON refer to EXIF-oriented source and final-size canvas.
"""
import argparse
from collections import Counter
import json
import math
import os
from pathlib import Path
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps
from fontTools.ttLib import TTFont


def read_rgb(path):
    with Image.open(path) as im:
        return ImageOps.exif_transpose(im).convert('RGB')


def font_at(path, index, size, text):
    with TTFont(path, fontNumber=index, lazy=True) as font:
        cmap = font.getBestCmap() or {}
        missing = sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
    if missing:
        raise ValueError('Font is missing characters: ' + ' '.join(missing))
    return ImageFont.truetype(str(path), size, index=index)


def source_accent(source, point):
    if point:
        x, y = point
        if not (0 <= x < source.width and 0 <= y < source.height):
            raise ValueError('Accent point is outside the oriented source.')
        return source.getpixel((x, y))
    # NEAREST samples are actual source colors, not averaged or invented RGBs.
    pixels = list(source.resize((64, 64), Image.Resampling.NEAREST).getdata())
    buckets = Counter(tuple(v // 32 for v in p) for p in pixels)
    eligible = [b for b in buckets if 45 < sum(b) * 32 / 3 < 235 and max(b)-min(b) >= 1]
    best = max(eligible or list(buckets), key=lambda b: buckets[b])
    return Counter(p for p in pixels if tuple(v // 32 for v in p) == best).most_common(1)[0][0]


def polygon(points, size, name):
    if not isinstance(points, list) or len(points) < 3:
        raise ValueError(name + ' needs at least three points.')
    for p in points:
        if len(p) != 2 or not all(math.isfinite(v) for v in p):
            raise ValueError(name + ' has an invalid point.')
        if not (0 <= p[0] < size[0] and 0 <= p[1] < size[1]):
            raise ValueError(name + ' extends outside the oriented source.')
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).polygon([tuple(p) for p in points], fill=255)
    return mask


def restore_faces(art, source, manifest):
    result = art.copy()
    union = Image.new('L', art.size)
    expected = []
    for index, face in enumerate(manifest.get('faces', []), 1):
        scale = float(face['scale'])
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError('Face scale must be positive and finite.')
        a, b = face['source_anchor'], face['target_anchor']
        if len(a) != 2 or len(b) != 2 or not all(math.isfinite(v) for v in a+b):
            raise ValueError('Face anchors need two finite coordinates.')
        tx, ty = b[0]-scale*a[0], b[1]-scale*a[1]
        outer = polygon(face['outer'], source.size, 'outer')
        core = polygon(face['core'], source.size, 'core')
        if ImageChops.subtract(core, outer).getbbox():
            raise ValueError('Every core pixel must be inside outer.')
        for x, y in face['core']:
            if not (0 <= scale*x+tx < art.width and 0 <= scale*y+ty < art.height):
                raise ValueError('Face core would be cut off by the canvas.')
        feather = float(face.get('feather', 5))
        if not math.isfinite(feather) or feather < 0:
            raise ValueError('Feather must be finite and nonnegative.')
        alpha = ImageChops.lighter(outer.filter(ImageFilter.GaussianBlur(feather)), core)
        matrix = (1/scale, 0, -tx/scale, 0, 1/scale, -ty/scale)
        warped = source.transform(art.size, Image.Transform.AFFINE, matrix, Image.Resampling.BICUBIC)
        cm = core.transform(art.size, Image.Transform.AFFINE, matrix, Image.Resampling.NEAREST)
        if not cm.getbbox():
            raise ValueError('Face core has no pixels at this output size.')
        if ImageChops.multiply(cm, union).getbbox():
            raise ValueError('Facial cores overlap. Recheck the placement.')
        am = alpha.transform(art.size, Image.Transform.AFFINE, matrix, Image.Resampling.BILINEAR)
        am = ImageChops.lighter(am, cm)  # keep every final core pixel opaque
        result = Image.composite(warped, result, am)
        union = ImageChops.lighter(union, cm)
        expected.append((cm, warped, {'face': index, 'scale': scale, 'source_core_preserved': True}))
    return result, expected


def tracked_width(text, font, tracking):
    return sum(font.getlength(c) for c in text) + max(0, len(text)-1)*tracking


def draw_tracked(draw, xy, text, font, tracking, fill):
    x, y = xy
    for c in text:
        draw.text((round(x), round(y)), c, font=font, fill=fill, anchor='lt')
        x += font.getlength(c)+tracking


def wrap_words(text, font, tracking, width):
    lines, current = [], ''
    for word in text.split():
        trial = (current+' '+word).strip()
        if tracked_width(trial, font, tracking) > width:
            if not current:
                raise ValueError('Subtitle contains a word too long for the type area.')
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    if len(lines) > 2 or any(tracked_width(t, font, tracking) > width for t in lines):
        raise ValueError('Subtitle needs to be shorter (up to two short lines).')
    return lines


def add_type(im, source, args):
    w, h = im.size
    raw = args.title.replace('|', '\n').strip()
    lines = raw.splitlines()
    # Short CJK titles naturally split into balanced two-line groups.
    if len(lines) == 1 and 4 <= len(raw) <= 8 and all(ord(c) > 127 for c in raw):
        cut = (len(raw)+1)//2
        lines = [raw[:cut], raw[cut:]]
    if not raw or len(lines) > 2 or any(not line.strip() for line in lines):
        raise ValueError('Use one or two nonempty title lines; separate with |.')
    title_font = font_at(args.font, args.font_index, round(w*.045), raw)
    latin_path = args.latin_font or args.font
    latin_index = 0 if args.latin_font else args.font_index
    english = font_at(latin_path, latin_index, max(12, round(w*.013)), args.subtitle)
    micro = font_at(latin_path, latin_index, max(10, round(w*.009)), args.number+' / PAPER NOTES '+args.footer)
    tw, et, mt = w*.003, w*.002, w*.0018
    if any(tracked_width(t, title_font, tw) > w*.32 for t in lines):
        raise ValueError('Title is too long for the left type area.')
    subtitle_lines = wrap_words(args.subtitle, english, et, w*.32)
    if not subtitle_lines:
        raise ValueError('Supply an English subtitle.')
    if tracked_width(args.footer, micro, mt) > w*.32:
        raise ValueError('Footer is too long.')
    layer = Image.new('RGBA', im.size)
    d = ImageDraw.Draw(layer)
    ink, secondary = (52, 49, 43, 255), (102, 97, 88, 255)
    x, y = w*.09, h*.13
    number = args.number+' / PAPER NOTES'
    if tracked_width(number, micro, mt) > w*.32:
        raise ValueError('Editorial number is too long.')
    draw_tracked(d, (x, h*.082), number, micro, mt, secondary)
    for line in lines:
        draw_tracked(d, (x, y), line, title_font, tw, ink)
        y += title_font.size*1.35
    y += h*.021
    accent = source_accent(source, args.accent_point)
    d.line((round(x), round(y), round(x+w*.03), round(y)), fill=accent+(255,), width=max(1, round(w*.0015)))
    y += h*.022
    for line in subtitle_lines:
        draw_tracked(d, (x, y), line, english, et, secondary)
        y += english.size*1.65
    if args.footer:
        draw_tracked(d, (x, h*.935), args.footer, micro, mt, secondary)
    return Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'), layer.getchannel('A'), accent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--art', type=Path, required=True, help='Reviewed text-free 3:4 base')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True, help='Lossless .png result')
    p.add_argument('--title', required=True, help='Use | to split into two lines')
    p.add_argument('--subtitle', required=True)
    p.add_argument('--number', default='01')
    p.add_argument('--footer', default='PAPER MEMORY')
    p.add_argument('--font', type=Path, required=True, help='Installed CJK serif font')
    p.add_argument('--font-index', type=int, default=0, help='Collection face index for TTC')
    p.add_argument('--latin-font', type=Path)
    p.add_argument('--accent-point', type=int, nargs=2, metavar=('X', 'Y'))
    p.add_argument('--faces', type=Path, help='Reviewed JSON source-face masks and placement')
    p.add_argument('--width', type=int, default=1536, help='Positive multiple of 3')
    p.add_argument('--overwrite', action='store_true')
    args = p.parse_args()
    temp = None
    try:
        if args.width <= 0 or args.width % 3:
            raise ValueError('Width must be a positive multiple of 3.')
        if args.output.suffix.lower() != '.png':
            raise ValueError('Output must be PNG for exact facial-core verification.')
        if args.output.resolve() in {args.art.resolve(), args.source.resolve()}:
            raise ValueError('Output cannot replace an input.')
        if args.output.exists() and not args.overwrite:
            raise ValueError('Output already exists; choose a new path or use --overwrite.')
        art, source = read_rgb(args.art), read_rgb(args.source)
        if art.width*4 != art.height*3:
            raise ValueError('Art base must already be exactly 3:4. Crop or outpaint first; do not stretch.')
        art = art.resize((args.width, args.width*4//3), Image.Resampling.LANCZOS)
        expected = []
        if args.faces:
            manifest = json.loads(args.faces.read_text(encoding='utf-8'))
            if not isinstance(manifest.get('faces'), list) or not manifest['faces']:
                raise ValueError('A faces file must contain a nonempty faces array.')
            art, expected = restore_faces(art, source, manifest)
        result, type_mask, accent = add_type(art, source, args)
        for core, warped, _ in expected:
            if ImageChops.multiply(core, type_mask).getbbox():
                raise ValueError('Typography overlaps a protected facial core. Reposition the art/type.')
            if Image.composite(ImageChops.difference(result, warped), Image.new('RGB', result.size), core).getbbox():
                raise ValueError('Original facial-core verification failed.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=args.output.stem+'-', suffix='.png', dir=args.output.parent)
        temp = Path(name)
        with os.fdopen(fd, 'wb') as f:
            result.save(f, format='PNG'); f.flush(); os.fsync(f.fileno())
        saved = read_rgb(temp)
        if ImageChops.difference(saved, result).getbbox():
            raise ValueError('Saved PNG does not match the composed result.')
        os.replace(temp, args.output); temp = None
        print(json.dumps({'output': str(args.output), 'size': list(saved.size), 'accent_rgb_from_source': accent,
                          'face_checks': [record for _, _, record in expected], 'saved_png_verified': True}, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as e:
        p.error(str(e))
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
