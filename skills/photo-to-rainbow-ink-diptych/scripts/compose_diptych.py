#!/usr/bin/env python3
"""Assemble an unchanged photo crop above generated art. Requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps


def opaque_rgb(path):
    with Image.open(path) as opened:
        im = ImageOps.exif_transpose(opened)
        icc = im.info.get('icc_profile')
        if im.mode == 'RGBA':
            if im.getextrema()[3] != (255, 255):
                raise ValueError('Transparent inputs are unsupported; provide an opaque RGB image.')
            im = im.convert('RGB')
        elif im.mode != 'RGB':
            raise ValueError(f'Expected RGB input, got {im.mode}; do not silently recolor the source.')
        return im.copy(), icc


def crop_rect(size, box, fx, fy):
    w, h = size
    if box:
        l, t, r, b = box
        if not (0 <= l < r <= w and 0 <= t < b <= h):
            raise ValueError('Crop box must lie inside the EXIF-oriented source.')
        if (r-l)*9 != (b-t)*16:
            raise ValueError('Explicit photo crop must have exact 16:9 proportions.')
        return tuple(box)
    unit = min(w//16, h//9)
    if unit < 1:
        raise ValueError('Photo is too small for an integer-pixel 16:9 crop.')
    cw, ch = 16*unit, 9*unit
    l = max(0, min(w-cw, round(fx*w-cw/2)))
    t = max(0, min(h-ch, round(fy*h-ch/2)))
    return l, t, l+cw, t+ch


def cover_art(im, size, fx, fy, allow_crop):
    ratio = size[0]/size[1]
    if im.width/im.height > ratio:
        cw, ch = max(1, round(im.height*ratio)), im.height
    else:
        cw, ch = im.width, max(1, round(im.width/ratio))
    removed = 1-(cw*ch)/(im.width*im.height)
    if removed > .25 and not allow_crop:
        raise ValueError(f'Lower-art framing would remove {removed:.1%}; inspect and regenerate nearer 4:5, or explicitly use --allow-art-crop.')
    l = max(0, min(im.width-cw, round(fx*im.width-cw/2)))
    t = max(0, min(im.height-ch, round(fy*im.height-ch/2)))
    box = (l, t, l+cw, t+ch)
    return im.crop(box).resize(size, Image.Resampling.LANCZOS), box, removed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', required=True, type=Path)
    ap.add_argument('--art', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--width', type=int, default=1152, help='Positive multiple of 144.')
    ap.add_argument('--crop-box', type=int, nargs=4, metavar=('LEFT','TOP','RIGHT','BOTTOM'))
    ap.add_argument('--focus-x', type=float, default=.5)
    ap.add_argument('--focus-y', type=float, default=.5)
    ap.add_argument('--art-focus-x', type=float, default=.5)
    ap.add_argument('--art-focus-y', type=float, default=.5)
    ap.add_argument('--prepare-only', action='store_true', help='Save the upper-photo crop preview only.')
    ap.add_argument('--allow-art-crop', action='store_true')
    ap.add_argument('--overwrite', action='store_true', help='Replace an existing output, never an input.')
    args = ap.parse_args()
    try:
        if args.width <= 0 or args.width % 144:
            raise ValueError('Width must be a positive multiple of 144 for both exact aspect ratios.')
        if any(not 0 <= f <= 1 for f in [args.focus_x,args.focus_y,args.art_focus_x,args.art_focus_y]):
            raise ValueError('Focus values must be between 0 and 1.')
        if args.output.suffix.lower() != '.png':
            raise ValueError('Use .png output for lossless verification.')
        output = args.output.resolve()
        if output == args.source.resolve() or (args.art and output == args.art.resolve()):
            raise ValueError('Output must not overwrite either input.')
        if output.exists() and not args.overwrite:
            raise ValueError('Output exists; choose another path or use --overwrite.')
        if not args.prepare_only and not args.art:
            raise ValueError('Provide --art for assembly, or --prepare-only for a crop preview.')
        if args.prepare_only and args.art:
            raise ValueError('Do not combine --art and --prepare-only.')
        source, icc = opaque_rgb(args.source)
        w, h = args.width, args.width*16//9
        ph = args.width*9//16
        box = crop_rect(source.size,args.crop_box,args.focus_x,args.focus_y)
        top = source.crop(box).resize((w,ph),Image.Resampling.LANCZOS)
        report = {'mode':'preview' if args.prepare_only else 'diptych',
                  'canvas_size':[w,h],'photo_size':[w,ph],'art_size':[w,h-ph],
                  'photo_crop_box':list(box),
                  'photo_operations':['EXIF display orientation','crop','uniform resize'],
                  'top_rgb_sha256':hashlib.sha256(top.tobytes()).hexdigest()}
        if args.prepare_only:
            final = top
        else:
            art, _ = opaque_rgb(args.art)
            bottom, abox, removed = cover_art(art,(w,h-ph),args.art_focus_x,args.art_focus_y,args.allow_art_crop)
            final = Image.new('RGB',(w,h))
            final.paste(bottom,(0,ph))
            final.paste(top,(0,0))  # Paste the actual photo last.
            report.update(art_crop_box=list(abox),art_crop_fraction=removed)
        output.parent.mkdir(parents=True,exist_ok=True)
        final.save(output,format='PNG',**({'icc_profile':icc} if icc else {}))
        with Image.open(output) as saved:
            actual = saved.crop((0,0,w,ph))
            if actual.mode != 'RGB' or actual.tobytes() != top.tobytes():
                raise RuntimeError('Saved upper panel failed pixel equality verification.')
        report.update(output=str(output),top_pixels_verified=True)
        print(json.dumps(report,ensure_ascii=False,indent=2))
    except (ValueError,OSError,RuntimeError) as exc:
        ap.exit(2,f'Error: {exc}\n')


if __name__ == '__main__':
    main()
