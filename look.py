"""v4 'premium dark' look for the Cost Decoded engine, matched to the reference Shorts:
black stage with a scrolling perspective grid floor, green corner flare, vignette, bloom on
bright elements, full-bleed graded b-roll photos, monochrome icon infographics, light leaks."""
import math, os, re
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

from engine_v2 import (HERE, FONT_DIR, PALETTE, VISUALS, font, ease_out, fade, fit_font, emoji_img, paste_scaled)

BLACK_W = "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold"


def _norm(s):
    return re.sub(r"[^a-z0-9$%]", "", s.lower())


def _spring(x):
    x = max(0.0, min(1.0, x))
    return 1.1 * ease_out(x / 0.6) if x < 0.6 else 1.1 - 0.1 * ease_out((x - 0.6) / 0.4)


class GridBG:
    def __init__(self, W, H, n_frames=24):
        self.frames = []
        horizon = int(H * 0.60)
        S = min(W, H)
        vign = Image.new("L", (W, H), 0)
        vd = ImageDraw.Draw(vign)
        for i in range(40):
            k = i / 40
            vd.ellipse([-W * 0.35 + k * W * 0.3, -H * 0.2 + k * H * 0.25, W * 1.35 - k * W * 0.3, H * 1.2 - k * H * 0.25],
                       fill=int(255 * (1 - k) ** 2.2))
        vign = vign.filter(ImageFilter.GaussianBlur(60))
        flare = Image.new("RGB", (W, H), (0, 0, 0))
        fd = ImageDraw.Draw(flare)
        for i in range(30):
            r = S * (0.55 - i * 0.017)
            c = int(4 + i * 2.0)
            fd.ellipse([W * 1.02 - r, -H * 0.06 - r, W * 1.02 + r, -H * 0.06 + r], fill=(0, c, int(c * 0.35)))
        flare = flare.filter(ImageFilter.GaussianBlur(40))
        black = Image.new("RGB", (W, H), (0, 0, 0))
        for f in range(n_frames):
            ph = f / n_frames
            im = Image.new("RGB", (W, H), PALETTE["bg"])
            d = ImageDraw.Draw(im)
            step = W / 7
            for x in range(8):
                d.line([(x * step, 0), (x * step, horizon)], fill=(26, 26, 32), width=2)
            y = 0.0
            while y < horizon:
                d.line([(0, y), (W, y)], fill=(26, 26, 32), width=2)
                y += step
            vp = (W / 2, horizon - H * 0.08)
            for k in range(-9, 10):
                d.line([vp, (W / 2 + k * W * 0.16, H)], fill=(78, 78, 88), width=3)
            for k in range(14):
                tt = ((k + ph) / 14) ** 2.3
                yy = horizon + (H - horizon) * tt
                d.line([(0, yy), (W, yy)], fill=(int(45 + 70 * tt),) * 3, width=max(1, int(1 + 4 * tt)))
            fadeband = Image.linear_gradient("L").resize((W, int(H * 0.12)))
            im.paste(Image.new("RGB", fadeband.size, PALETTE["bg"]), (0, int(horizon - H * 0.08)), fadeband.rotate(180))
            im = ImageChops.add(im, flare)
            im = Image.composite(black, im, vign)
            self.frames.append(im)

    def frame(self, t):
        return self.frames[int(t * 14) % len(self.frames)].copy()


_BLOOM_LUT = [min(255, int(max(0, v - 165) * 1.5)) for v in range(256)] * 3


def bloom(img, W, H):
    small = img.resize((W // 4, H // 4), Image.BILINEAR).point(_BLOOM_LUT)
    glow = small.filter(ImageFilter.GaussianBlur(7)).resize((W, H), Image.BILINEAR)
    return ImageChops.add(img, glow)


_broll_cache = {}
OVERSCAN = 1.22


def broll_base(path, W, H):
    key = (path, W, H)
    if key not in _broll_cache:
        full = path if os.path.isabs(path) else os.path.join(HERE, path)
        im = Image.open(full).convert("RGB")
        r = max(W * OVERSCAN / im.width, H * OVERSCAN / im.height)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.18)
        im = ImageEnhance.Color(im).enhance(1.12)
        im = ImageEnhance.Brightness(im).enhance(0.8)
        _broll_cache[key] = im
    return _broll_cache[key]


def spaced_text(d, xy, text, f, fill, spacing):
    total = sum(d.textlength(ch, font=f) for ch in text) + spacing * (len(text) - 1)
    x = xy[0] - total / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=f, fill=fill, anchor="lm")
        x += d.textlength(ch, font=f) + spacing


def v_broll(d, img, W, H, t, dur, s):
    """Full-bleed photo with slow push and pan, darkened grade, fades top/bottom, optional glowing headline."""
    S = min(W, H)
    base = broll_base(s["file"], W, H)
    k = t / max(dur, 0.1)
    z = 1.0 + 0.10 * k
    # window = the frame size scaled into base pixels, shrinking as we zoom in
    scale = min(base.width / W, base.height / H) / z
    cw, ch = int(W * scale), int(H * scale)
    fx, fy = s.get("focus", (0.5, 0.45))
    pan = s.get("pan", 0.06)
    cx = (base.width - cw) * min(1, max(0, fx + pan * (k - 0.5)))
    cy = (base.height - ch) * fy
    frame = base.crop((int(cx), int(cy), int(cx) + cw, int(cy) + ch)).resize((W, H), Image.BILINEAR)
    img.paste(frame, (0, 0))
    grad = Image.linear_gradient("L").resize((W, int(H * 0.5)))
    img.paste(Image.new("RGB", grad.size, PALETTE["bg"]), (0, H - grad.height), grad.point(lambda v: int(v * 0.92)))
    top = Image.linear_gradient("L").rotate(180).resize((W, int(H * 0.18)))
    img.paste(Image.new("RGB", top.size, PALETTE["bg"]), (0, 0), top.point(lambda v: int(v * 0.6)))
    if s.get("lines"):
        hl = set(_norm(w) for w in s.get("highlight", []))
        f0 = font(S * s.get("scale", 0.12), BLACK_W)
        y0 = H * s.get("y", 0.52)
        hc = PALETTE[s.get("hl_color", "bad")]
        for i, line in enumerate(s["lines"]):
            st = s.get("lines_at", 0.1) + 0.22 * i
            if t < st:
                continue
            lf = fit_font(d, line, W * 0.92, f0.size, BLACK_W)
            lf = font(lf.size * _spring((t - st) / 0.28), BLACK_W)
            total = d.textlength(line, font=lf)
            x = W / 2 - total / 2
            for w in line.split():
                c = hc if _norm(w) in hl else PALETTE["text"]
                d.text((x, y0 + i * f0.size * 1.08), w, font=lf, fill=c, anchor="lm",
                       stroke_width=max(2, int(lf.size * 0.03)), stroke_fill=(0, 0, 0))
                x += d.textlength(w + " ", font=lf)
    if s.get("label"):
        a = ease_out((t - 0.3) / 0.4)
        spaced_text(d, (W / 2, H * s.get("label_y", 0.66)), s["label"].upper(), font(S * 0.05, "Bold"),
                    fade(PALETTE["text"], a), S * 0.012)


_icon_cache = {}


def icon_disc(emoji, r):
    key = (emoji, r)
    if key not in _icon_cache:
        e = emoji_img(emoji, int(r * 1.15))
        sil = Image.new("RGBA", e.size, (10, 10, 12, 255))
        sil.putalpha(e.split()[3])
        disc = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
        ImageDraw.Draw(disc).ellipse([4, 4, r * 2 + 4, r * 2 + 4], fill=(248, 248, 250, 255))
        disc.alpha_composite(sil, (r + 4 - sil.width // 2, r + 4 - sil.height // 2))
        _icon_cache[key] = disc
    return _icon_cache[key]


def nodes_layout(W, H, n):
    cx, cy = W / 2, H * 0.40
    S = min(W, H)
    angles = [-90, 180, 0] if n <= 3 else [-90 + (360 / n) * k for k in range(n)]
    return (cx, cy), [(cx + math.cos(math.radians(a)) * S * 0.29, cy + math.sin(math.radians(a)) * S * 0.30) for a in angles[:n]]


def v_nodes(d, img, W, H, t, dur, s):
    """Monochrome infographic: centre icon branching out to labelled icon nodes."""
    S = min(W, H)
    (cx, cy), pts = nodes_layout(W, H, len(s["nodes"]))
    lab = font(S * 0.042, "Bold")
    for k, (x, y) in enumerate(pts):
        st = 0.45 + 0.4 * k
        if t < st - 0.2:
            continue
        p = ease_out((t - st + 0.2) / 0.3)
        d.line([(cx, cy), (cx + (x - cx) * p, cy + (y - cy) * p)], fill=(230, 230, 235), width=max(3, int(S * 0.004)))
    paste_scaled(img, icon_disc(s["center"]["emoji"], int(S * 0.11)), cx, cy, _spring((t - 0.05) / 0.3))
    if s["center"].get("label") and t > 0.25:
        spaced_text(d, (cx, cy + S * 0.17), s["center"]["label"].upper(), font(S * 0.055, "Bold"),
                    fade(PALETTE["text"], ease_out((t - 0.25) / 0.3)), S * 0.014)
    for k, ((x, y), nd) in enumerate(zip(pts, s["nodes"])):
        st = 0.45 + 0.4 * k
        if t < st:
            continue
        paste_scaled(img, icon_disc(nd["emoji"], int(S * 0.08)), x, y, _spring((t - st) / 0.3))
        c = PALETTE["good"] if nd.get("hot") else PALETTE["text"]
        txt = nd["label"].upper()
        side = abs(x - cx) > 1
        lf = lab
        while lf.size > 18 and sum(d.textlength(ch, font=lf) for ch in txt) + S * 0.008 * len(txt) > W * 0.40:
            lf = font(lf.size - 2, "Bold")
        ly = y - S * 0.12
        lx = min(max(x, W * 0.21), W * 0.79)
        spaced_text(d, (lx, ly), txt, lf, fade(c, ease_out((t - st - 0.1) / 0.3)), S * 0.008)


def nodes_cue_times(s):
    return [0.05] + [0.45 + 0.4 * k for k in range(len(s["nodes"]))]


VISUALS["broll"] = (v_broll, lambda s: [])
VISUALS["photo_hook"] = (v_broll, lambda s: [])
VISUALS["nodes"] = (v_nodes, lambda s: [])

_leak = None


def light_leak(img, W, H, k):
    """Warm light-leak sweep across a cut (k: 0..1)."""
    global _leak
    if _leak is None:
        L = Image.new("RGB", (W * 2, H), (0, 0, 0))
        ld = ImageDraw.Draw(L)
        for i in range(30):
            r = H * (0.55 - i * 0.017)
            ld.ellipse([W - r * 0.8, H * 0.45 - r, W + r * 0.8, H * 0.45 + r], fill=(int(30 + i * 7), int(12 + i * 3.5), int(i * 0.8)))
        _leak = L.filter(ImageFilter.GaussianBlur(50))
    x = int(-W * 1.2 + k * W * 1.6)
    a = math.sin(math.pi * max(0, min(1, k)))
    lut = [int(v * a) for v in range(256)] * 3
    left = max(0, min(W, -x))
    crop = _leak.crop((left, 0, left + W, H)).point(lut)
    return ImageChops.screen(img, crop)
