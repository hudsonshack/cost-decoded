"""Cost Decoded video engine v2 (high-stimulation edition).

JSON script -> finished vertical Short (1080x1920) or long-form (1920x1080).
Local AI voice (Kokoro), animated data visuals, pop-up stickers and emoji,
kinetic word-by-word captions, punch zooms, shake, flashes, and synthesized
sound effects (pops, clicks, whooshes, ka-chings, impacts). No music.

Usage: python3 engine.py path/to/script.json out.mp4
"""
import json, math, os, random, re, subprocess, sys, tempfile
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")
FONT_DIR = "/usr/share/fonts/opentype/inter/"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
FPS = 30
SR = 24000

PALETTE = {
    "bg": (9, 13, 28), "bg2": (18, 26, 52), "grid": (28, 40, 78), "text": (245, 247, 250),
    "muted": (160, 170, 195), "accent": (255, 200, 61), "good": (46, 230, 140),
    "bad": (255, 77, 90), "blue": (80, 160, 255), "money": (40, 170, 90),
}


def font(size, weight="ExtraBold"):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", max(8, int(size)))


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = max(0.0, min(1.0, x))
    c1, c3 = 1.9, 2.9
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def col(name):
    return PALETTE.get(name, PALETTE["accent"]) if isinstance(name, str) else tuple(name)


def fade(c, a):
    return tuple(int(cc * a + PALETTE["bg"][k] * (1 - a)) for k, cc in enumerate(c))


# ================================================================ voice
_kokoro = None


def tts(text, voice, speed):
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(f"{MODELS}/kokoro-v1.0.onnx", f"{MODELS}/voices-v1.0.bin")
    if isinstance(voice, str) and voice.endswith(".npy"):
        voice = np.load(os.path.join(MODELS, voice))
    elif isinstance(voice, dict):  # {"am_michael":0.6,"am_fenrir":0.4}
        voice = sum(w * _kokoro.get_voice_style(v) for v, w in voice.items())
    samples, sr = _kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    return samples.astype(np.float32)


# ================================================================ sound effects (synthesized)
def _t(sec):
    return np.arange(int(sec * SR)) / SR


def sfx_pop():
    t = _t(0.09)
    f = 900 * np.exp(-t * 35) + 250
    return 0.9 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)


def sfx_click():
    t = _t(0.03)
    rng = np.random.default_rng(1)
    return 0.6 * (rng.standard_normal(len(t)) * np.exp(-t * 400) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 250))


def sfx_tick():
    t = _t(0.015)
    return 0.35 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 500)


def sfx_whoosh():
    t = _t(0.38)
    rng = np.random.default_rng(2)
    n = rng.standard_normal(len(t))
    # crude band sweep: moving average with shrinking window
    out = np.zeros_like(n)
    acc = 0.0
    for i in range(len(n)):
        k = 0.02 + 0.5 * (i / len(n))
        acc = acc + k * (n[i] - acc)
        out[i] = acc
    env = np.sin(np.pi * t / t[-1]) ** 2
    return 0.9 * out / (np.abs(out).max() + 1e-9) * env


def sfx_impact():
    t = _t(0.45)
    rng = np.random.default_rng(3)
    sub = np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 25)) * t) * np.exp(-t * 7)
    crack = rng.standard_normal(len(t)) * np.exp(-t * 60) * 0.5
    return 0.95 * (sub + crack) / 1.3


def sfx_kaching():
    t = _t(0.7)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((2093, 0.5), (2637, 0.35), (3136, 0.25), (4186, 0.15)))
    bell *= np.exp(-t * 5)
    d = int(0.06 * SR)
    bell2 = np.concatenate([np.zeros(d), bell[:-d]])
    clk = np.zeros_like(t)
    clk[:len(sfx_click())] += sfx_click()
    return 0.55 * (bell + 0.8 * bell2) + clk


def sfx_mouse():
    """Crisp mouse click: press + release transients, the classic 'image pops in' click."""
    rng = np.random.default_rng(6)
    def transient(dur, f, amp):
        t = _t(dur)
        n = rng.standard_normal(len(t))
        n = np.diff(np.concatenate([[0], n]))  # crude high-pass
        return amp * (0.6 * n * np.exp(-t * 900) + np.sin(2 * np.pi * f * t) * np.exp(-t * 320))
    press, release = transient(0.03, 3400, 1.0), transient(0.03, 4200, 0.55)
    out = np.zeros(int(0.12 * SR))
    out[:len(press)] += press
    j = int(0.065 * SR)
    out[j:j + len(release)] += release
    return out / (np.abs(out).max() + 1e-9)


def sfx_ding():
    t = _t(0.5)
    return 0.5 * (np.sin(2 * np.pi * 1760 * t) + 0.4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 7)


def sfx_type():
    t = _t(0.04)
    rng = np.random.default_rng(4)
    return 0.45 * rng.standard_normal(len(t)) * np.exp(-t * 180)


SFX = {k: f().astype(np.float32) for k, f in {
    "pop": sfx_pop, "click": sfx_click, "tick": sfx_tick, "whoosh": sfx_whoosh, "impact": sfx_impact,
    "kaching": sfx_kaching, "ding": sfx_ding, "type": sfx_type, "mouse": sfx_mouse}.items()}
SFX_GAIN = {"pop": 0.55, "click": 0.45, "tick": 0.35, "whoosh": 0.35, "impact": 0.6, "kaching": 0.45,
            "ding": 0.4, "type": 0.3, "mouse": 0.85}


# ================================================================ drawing helpers
def text_center(d, xy, s, f, fill, anchor="mm", stroke=0, stroke_fill=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill or PALETTE["bg"])


def fit_font(d, s, max_w, start, weight="ExtraBold", min_size=36):
    size = int(start)
    while size > min_size:
        f = font(size, weight)
        if d.textlength(s, font=f) <= max_w:
            return f
        size -= 4
    return font(min_size, weight)


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fmt_num(v, decimals=0):
    return f"{v:,.{decimals}f}" if decimals else f"{int(round(v)):,}"


def short_money(v):
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(v) >= div:
            return f"{v / div:.1f}".rstrip("0").rstrip(".") + suf
    return fmt_num(v)


_emoji_cache = {}


def emoji_img(ch, size):
    key = (ch, size)
    if key not in _emoji_cache:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
        im = im.crop(im.getbbox() or (0, 0, 160, 160))
        r = size / max(im.size)
        _emoji_cache[key] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _emoji_cache[key]


def sticker(text, color, size):
    """Tilted badge with bold text (and optional leading emoji)."""
    f = font(size, "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold")
    em = None
    m = re.match(r"^(\W+?)\s+(.*)$", text)
    if m and any(ord(c) > 0x2000 for c in m.group(1)):
        em, text = m.group(1), m.group(2)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    tw = int(tmp.textlength(text, font=f))
    ew = int(size * 1.15) if em else 0
    pad = int(size * 0.45)
    W, H = tw + ew + pad * 2, int(size * 1.7)
    im = Image.new("RGBA", (W + 16, H + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 12, W + 8, H + 12], radius=int(H * 0.28), fill=(0, 0, 0, 120))  # shadow
    d.rounded_rectangle([8, 4, W + 8, H + 4], radius=int(H * 0.28), fill=col(color) + (255,))
    dark = sum(col(color)) > 450
    d.text((8 + pad + ew, 4 + H / 2), text, font=f, fill=PALETTE["bg"] if dark else PALETTE["text"], anchor="lm")
    if em:
        e = emoji_img(em, int(size * 1.05))
        im.alpha_composite(e, (8 + pad, int(4 + H / 2 - e.height / 2)))
    return im


def paste_scaled(dst, src, cx, cy, scale, rot=0):
    if scale <= 0.02:
        return
    im = src.resize((max(1, int(src.width * scale)), max(1, int(src.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    dst.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


_photo_cache = {}


def load_photo(path):
    full = path if os.path.isabs(path) else os.path.join(HERE, path)
    if full not in _photo_cache:
        _photo_cache[full] = Image.open(full).convert("RGB")
    return _photo_cache[full]


_card_cache = {}


def photo_card(path, width):
    key = (path, width)
    if key not in _card_cache:
        im = load_photo(path).copy()
        r = width / im.width
        im = im.resize((int(width), int(im.height * r)), Image.LANCZOS)
        b = max(6, int(width * 0.025))
        card = Image.new("RGBA", (im.width + 2 * b + 30, im.height + 2 * b + 30), (0, 0, 0, 0))
        sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([18, 22, im.width + 2 * b + 18, im.height + 2 * b + 22], radius=b * 2, fill=(0, 0, 0, 150))
        from PIL import ImageFilter
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        card.alpha_composite(sh)
        ImageDraw.Draw(card).rounded_rectangle([10, 10, im.width + 2 * b + 10, im.height + 2 * b + 10], radius=b * 2, fill=(255, 255, 255, 255))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width, im.height], radius=b, fill=255)
        card.paste(im, (10 + b, 10 + b), mask)
        _card_cache[key] = card
    return _card_cache[key]


# ================================================================ scene visuals
# Each visual draws onto `d`/`img` at local time t and returns nothing.
# cues(spec) returns [(time, sfx_name)] relative to scene start.

def v_big_number(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    count = s.get("count", True)
    p = ease_out(t / 1.1) if count else 1
    val = s["value"] * p
    final = s.get("prefix", "") + fmt_num(s["value"], s.get("decimals", 0)) + s.get("suffix", "")
    label = s.get("prefix", "") + fmt_num(val, s.get("decimals", 0)) + s.get("suffix", "")
    pop = ease_back(t / 0.35)
    base = fit_font(d, final, W * 0.88, s.get("size", 270) * S / 1080)
    f = font(base.size * (0.5 + 0.5 * pop))
    cy = H * 0.40
    c = col(s.get("color", "accent"))
    # glow ring burst on landing
    if count and 1.0 < t < 1.6 or (not count and t < 0.6):
        k = ease_out((t - (1.0 if count else 0)) / 0.6)
        r = S * (0.25 + 0.35 * k)
        d.ellipse([W / 2 - r, cy - r, W / 2 + r, cy + r], outline=fade(c, 0.6 * (1 - k)), width=int(S * 0.012))
    text_center(d, (W / 2, cy), label, f, c, stroke=int(f.size * 0.04), stroke_fill=(0, 0, 0))
    if s.get("caption"):
        a = ease_out((t - 0.35) / 0.4)
        fc = font(S * 0.056, "Bold")
        for i, line in enumerate(wrap(d, s["caption"], fc, W * 0.82)):
            text_center(d, (W / 2, cy + base.size * 0.72 + fc.size * 0.5 + i * fc.size * 1.25 + (1 - a) * 40), line, fc, fade(PALETTE["muted"], a))


def c_big_number(s):
    out = [(0.0, "impact")]
    if s.get("count", True):
        out += [(0.04 * i, "tick") for i in range(1, 26)]
        out.append((1.1, "kaching" if s.get("prefix", "").startswith("$") else "ding"))
    elif s.get("prefix", "").startswith("$"):
        out.append((0.15, "kaching"))
    return out


def v_compare_bars(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    items = s["items"]
    vmax = max(i["value"] for i in items)
    n = len(items)
    area_top, area_bot = (H * 0.30, H * 0.66) if land else (H * 0.22, H * 0.62)
    gap = S * 0.06
    bw = min((W * 0.84 - gap * (n - 1)) / n, S * 0.32)
    x0 = W / 2 - (bw * n + gap * (n - 1)) / 2
    fl = font(S * 0.048, "Bold")
    fv = font(S * 0.08)
    if s.get("title"):
        a = ease_back(t / 0.3)
        tf = fit_font(d, s["title"], W * 0.88, S * 0.066)
        text_center(d, (W / 2, H * (0.12 if land else 0.15)), s["title"], font(tf.size * (0.6 + 0.4 * a)), PALETTE["text"])
    for k, it in enumerate(items):
        st = 0.3 + 0.45 * k
        p = ease_back((t - st) / 0.7) if t > st else 0
        p = min(p, 1.08)
        h = (area_bot - area_top - H * 0.06) * (it["value"] / vmax) * p
        x = x0 + k * (bw + gap)
        c = col(it.get("color", "accent"))
        d.rounded_rectangle([x, area_bot - max(h, 2), x + bw, area_bot], radius=int(bw * 0.08), fill=c)
        if p > 0:
            shown = it["value"] * min(p, 1)
            val = s.get("prefix", "") + (short_money(shown) if s.get("short") else fmt_num(shown, s.get("decimals", 0))) + s.get("suffix", "")
            text_center(d, (x + bw / 2, area_bot - h - fv.size * 0.7), val, fv, c, stroke=3, stroke_fill=(0, 0, 0))
        for i, line in enumerate(wrap(d, it["label"], fl, bw * 1.1)):
            text_center(d, (x + bw / 2, area_bot + fl.size * (1.0 + 1.2 * i)), line, fl, PALETTE["text"])


def c_compare_bars(s):
    out = [(0.0, "whoosh")]
    for k in range(len(s["items"])):
        out.append((0.3 + 0.45 * k, "pop"))
    out.append((0.3 + 0.45 * len(s["items"]) + 0.3, "ding"))
    return out


def v_donut(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    p = ease_out(t / 1.2)
    cx, cy = W / 2, H * (0.40 if land else 0.38)
    r, th = S * (0.22 if land else 0.30), int(S * (0.07 if land else 0.09))
    pulse = 1 + 0.04 * ease_back((t - 1.2) / 0.3) * (1 - ease_out((t - 1.5) / 0.4)) if t > 1.2 else 1
    r *= pulse
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PALETTE["bg2"], width=th)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=-90, end=-90 + 360 * s["value"] / 100 * p,
          fill=col(s.get("color", "good")), width=th)
    text_center(d, (cx, cy), f"{fmt_num(s['value'] * p)}%", font(S * (0.12 if land else 0.16)), PALETTE["text"])
    if s.get("caption"):
        fc = font(S * 0.056, "Bold")
        a = ease_out((t - 0.5) / 0.5)
        for i, line in enumerate(wrap(d, s["caption"], fc, W * 0.82)):
            text_center(d, (cx, cy + r + H * (0.08 if land else 0.06) + i * fc.size * 1.25), line, fc, fade(PALETTE["muted"], a))


def c_donut(s):
    return [(0.0, "whoosh")] + [(0.05 * i, "tick") for i in range(1, 24)] + [(1.2, "pop"), (1.25, "ding")]


def v_statement(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    lines = s["lines"]
    hl = set(w.lower() for w in s.get("highlight", []))
    f0 = font(S * s.get("scale", 0.1))
    lh = f0.size * 1.22
    y0 = H * 0.38 - lh * (len(lines) - 1) / 2
    for i, line in enumerate(lines):
        st = 0.3 * i
        if t < st:
            continue
        pop = ease_back((t - st) / 0.3)
        f = font(f0.size * (0.4 + 0.6 * pop))
        words = line.split()
        total = d.textlength(line, font=f)
        x = W / 2 - total / 2
        y = y0 + i * lh
        for w in words:
            key = re.sub(r"\W", "", w.lower())
            c = PALETTE["accent"] if key in hl else PALETTE["text"]
            d.text((x, y), w, font=f, fill=c, anchor="lm", stroke_width=int(f.size * 0.03), stroke_fill=(0, 0, 0))
            x += d.textlength(w + " ", font=f)


def c_statement(s):
    return [(0.3 * i, "pop") for i in range(len(s["lines"]))] + [(0.3 * (len(s["lines"]) - 1) + 0.05, "impact")]


def v_people_grid(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    rows, cols = s.get("rows", 10), s.get("cols", 10)
    size = S * (0.55 if land else 0.72) / cols
    x0, y0 = W / 2 - size * cols / 2, H * (0.10 if land else 0.16)
    lit = s.get("lit", rows * cols)
    for k in range(rows * cols):
        r, c = divmod(k, cols)
        p = ease_back((t - k * 0.01) / 0.3)
        if p <= 0:
            continue
        cx, cy = x0 + c * size + size / 2, y0 + r * size + size / 2
        rr = size * 0.32 * p
        clr = col(s.get("color", "blue")) if k < lit else PALETTE["grid"]
        d.ellipse([cx - rr * 0.55, cy - rr * 1.1, cx + rr * 0.55, cy], fill=clr)
        d.rounded_rectangle([cx - rr * 0.9, cy + rr * 0.05, cx + rr * 0.9, cy + rr * 1.1], radius=int(max(1, rr * 0.5)), fill=clr)
    if s.get("caption"):
        a = ease_back((t - rows * cols * 0.01) / 0.3)
        fc = fit_font(d, s["caption"], W * 0.88, S * (0.06 if land else 0.07))
        if a > 0:
            text_center(d, (W / 2, y0 + rows * size + H * 0.05), s["caption"], font(fc.size * min(a, 1.1)), PALETTE["text"])


def c_people_grid(s):
    n = s.get("rows", 10) * s.get("cols", 10)
    return [(0.0, "whoosh")] + [(k * 0.01, "tick") for k in range(0, n, 5)] + [(n * 0.01, "pop")]


def v_outro(d, img, W, H, t, dur, s):
    S, land = min(W, H), W > H
    p = ease_back(t / 0.4)
    f = font(S * 0.15 * (0.5 + 0.5 * p), "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold")
    text_center(d, (W / 2, H * 0.36), "FOLLOW", f, PALETTE["accent"], stroke=int(f.size * 0.05), stroke_fill=(0, 0, 0))
    if s.get("caption"):
        a = ease_out((t - 0.3) / 0.4)
        text_center(d, (W / 2, H * 0.36 + f.size * 1.0), s["caption"], font(S * 0.055, "Bold"), fade(PALETTE["text"], a))


def c_outro(s):
    return []


def v_photo_hook(d, img, W, H, t, dur, s):
    """Full-bleed photo on top with slow zoom, big punchy headline underneath."""
    S, land = min(W, H), W > H
    ph = load_photo(s["file"])
    area_h = int(H * (0.5 if not land else 0.6))
    z = 1.12 + 0.06 * (t / max(dur, 0.1))
    r = max(W / ph.width, area_h / ph.height) * z
    im = ph.resize((int(ph.width * r), int(ph.height * r)), Image.BILINEAR)
    fx, fy = s.get("focus", (0.5, 0.5))
    x0 = int((im.width - W) * fx)
    y0 = int((im.height - area_h) * fy)
    im = im.crop((x0, y0, x0 + W, y0 + area_h))
    img.paste(im, (0, 0))
    # gradient fade into background
    grad = Image.new("L", (1, 256))
    for i in range(256):
        grad.putpixel((0, i), int(255 * max(0, (i - 120) / 136) ** 1.4))
    grad = grad.resize((W, int(area_h * 0.45)))
    over = Image.new("RGB", grad.size, PALETTE["bg"])
    img.paste(over, (0, area_h - grad.height), grad)
    hl = set(w.lower() for w in s.get("highlight", []))
    f0 = font(S * s.get("scale", 0.11), "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold")
    lh = f0.size * 1.12
    y = area_h - f0.size * 0.2
    for i, line in enumerate(s.get("lines", [])):
        st = 0.15 + 0.25 * i
        if t < st:
            continue
        pop = ease_back((t - st) / 0.3)
        f = font(f0.size * (0.5 + 0.5 * pop), f0.path.split("Inter-")[1].split(".")[0])
        lf = fit_font(d, line, W * 0.9, f.size, f0.path.split("Inter-")[1].split(".")[0])
        words = line.split()
        total = d.textlength(line, font=lf)
        x = W / 2 - total / 2
        for w in words:
            key = re.sub(r"[^\w$%]", "", w.lower())
            c = PALETTE["accent"] if key in hl or w.lower() in hl else PALETTE["text"]
            d.text((x, y + i * lh), w, font=lf, fill=c, anchor="lm", stroke_width=int(lf.size * 0.06), stroke_fill=(0, 0, 0))
            x += d.textlength(w + " ", font=lf)


def c_none(s):
    return []


VISUALS = {"big_number": (v_big_number, c_big_number), "compare_bars": (v_compare_bars, c_compare_bars),
           "donut": (v_donut, c_donut), "statement": (v_statement, c_statement),
           "people_grid": (v_people_grid, c_people_grid), "outro": (v_outro, c_outro),
           "photo_hook": (v_photo_hook, c_none)}

DEFAULT_POPS = {  # auto stickers if a scene has none, cycled for variety
    "big_number": [{"t": 1.15, "text": "🤯 WAIT WHAT", "color": "bad", "x": 0.72, "y": 0.22, "rot": 8}],
    "donut": [{"t": 1.25, "text": "💰", "x": 0.8, "y": 0.2, "emoji": True}],
    "statement": [],
    "compare_bars": [],
    "people_grid": [],
    "outro": [{"t": 0.3, "text": "👆", "x": 0.5, "y": 0.66, "emoji": True}],
}


# ================================================================ captions
NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
               "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand "
               "million billion trillion percent dollar dollars cents".split())


def word_times(text, dur):
    words = text.split()
    weights = [len(w) + 2 + (4 if w.endswith((".", ",", "?", "!")) else 0) for w in words]
    tot = sum(weights)
    out, acc = [], 0.0
    for w, wt in zip(words, weights):
        s0 = acc / tot * dur
        acc += wt
        out.append((s0, acc / tot * dur, w))
    return out


def draw_caption(d, W, H, words, idx, t_in, hl_words):
    S, land = min(W, H), W > H
    # group into chunks of 3 words, show the chunk containing idx
    ci = idx // 3
    chunk = words[ci * 3: ci * 3 + 3]
    if not chunk:
        return
    texts = [w[2].upper() for w in chunk]
    line = " ".join(texts)
    f = fit_font(d, line, W * 0.88, S * (0.07 if land else 0.088), "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold")
    total = d.textlength(line, font=f)
    x = W / 2 - total / 2
    y = H * (0.86 if land else 0.79)
    for j, w in enumerate(texts):
        active = (ci * 3 + j) == idx
        key = re.sub(r"[^\w$%]", "", w.lower())
        is_num = bool(re.search(r"\d|\$", w)) or key in NUMWORDS
        c = PALETTE["accent"] if active else (PALETTE["good"] if is_num or key in hl_words else PALETTE["text"])
        ff = f
        if active:
            ff = font(f.size * (1.0 + 0.12 * (1 - ease_out(t_in / 0.18))), f.path.split("Inter-")[1].split(".")[0])
        d.text((x, y), w, font=ff, fill=c, anchor="lm", stroke_width=int(f.size * 0.11), stroke_fill=(0, 0, 0))
        x += d.textlength(w, font=ff) + d.textlength(" ", font=f)


# ================================================================ background
def make_background(W, H, theme):
    big = Image.new("RGB", (W + 200, H + 200), PALETTE["bg"])
    g = ImageDraw.Draw(big)
    for y in range(big.height):
        k = y / big.height
        g.line([(0, y), (big.width, y)], fill=tuple(int(PALETTE["bg"][i] * (1 - k) + PALETTE["bg2"][i] * k) for i in range(3)))
    step = 100
    gc = (24, 50, 40) if theme == "wallstreet" else PALETTE["grid"]
    for x in range(0, big.width, step):
        g.line([(x, 0), (x, big.height)], fill=gc, width=2)
    for y in range(0, big.height, step):
        g.line([(0, y), (big.width, y)], fill=gc, width=2)
    return big


class Particles:
    def __init__(self, W, H, theme, n=14, seed=5):
        rng = random.Random(seed)
        self.W, self.H, self.theme = W, H, theme
        self.p = [(rng.random() * W, rng.random() * H, 40 + rng.random() * 70, rng.random() * 360, rng.uniform(-30, 30))
                  for _ in range(n)]
        S = min(W, H)
        self.f = font(S * 0.06, "ExtraBold")

    def draw(self, d, img, t):
        for x, y, v, r0, spin in self.p:
            yy = (y + v * t * (2.2 if self.theme == "wallstreet" else 1)) % (self.H + 100) - 50
            if self.theme == "wallstreet":  # falling cash bills
                w, h = self.W * 0.07, self.W * 0.035
                bill = Image.new("RGBA", (int(w), int(h)), PALETTE["money"] + (110,))
                bd = ImageDraw.Draw(bill)
                bd.rectangle([2, 2, w - 3, h - 3], outline=(170, 240, 190, 140), width=2)
                bd.text((w / 2, h / 2), "$", font=font(h * 0.7), fill=(200, 255, 215, 160), anchor="mm")
                bill = bill.rotate(r0 + spin * t, expand=True, resample=Image.BILINEAR)
                img.paste(bill, (int(x), int(yy)), bill)
            else:
                d.text((x, self.H - yy), "$", font=self.f, fill=(30, 44, 86), anchor="mm")


def draw_ticker(d, W, H, t, items):
    S = min(W, H)
    f = font(S * 0.032, "Bold")
    bar_h = S * 0.055
    y = H * 0.012
    d.rectangle([0, y, W, y + bar_h], fill=(5, 8, 18))
    text = "   •   ".join(items) + "   •   "
    tw = d.textlength(text, font=f)
    x = -(t * S * 0.18) % tw
    for k in range(-1, int(W / tw) + 2):
        xx = k * tw - x
        for part in text.split("   •   "):
            if not part:
                continue
            c = PALETTE["good"] if "▲" in part else PALETTE["bad"] if "▼" in part else PALETTE["accent"]
            d.text((xx, y + bar_h / 2), part, font=f, fill=c, anchor="lm")
            xx += d.textlength(part + "   •   ", font=f)


# ================================================================ render
def render(script_path, out_path):
    spec = json.load(open(script_path))
    vertical = spec.get("format", "short") == "short"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    S = min(W, H)
    theme = spec.get("theme", "default")
    voice, speed = spec.get("voice", "voice_smooth.npy"), spec.get("speed", 1.08)
    pad = 0.18

    scenes, audio = [], []
    for sc in spec["scenes"]:
        a = tts(sc["say"], voice, speed)
        dur = len(a) / SR + pad
        audio.append(np.concatenate([a, np.zeros(int(pad * SR), np.float32)]))
        scenes.append((sc, dur, word_times(sc["say"], len(a) / SR)))
    voice_track = np.concatenate(audio)
    tail = 0.7
    voice_track = np.concatenate([voice_track, np.zeros(int(tail * SR), np.float32)])
    total = len(voice_track) / SR
    starts = np.cumsum([0] + [s[1] for s in scenes])

    # ---- sound effects track
    fx = np.zeros_like(voice_track)

    def place(at, name, gain=1.0):
        i = int(max(0, at) * SR)
        clip = SFX[name] * SFX_GAIN[name] * gain
        j = min(len(fx), i + len(clip))
        if i < len(fx):
            fx[i:j] += clip[: j - i]

    pops_by_scene, photos_by_scene = [], []
    for k, (sc, dur, words) in enumerate(scenes):
        vtype = sc["visual"]["type"]
        pops = sc.get("pops", DEFAULT_POPS.get(vtype, []) if spec.get("auto_pops", False) else [])
        pops_by_scene.append(pops)
        for pp in pops:
            place(starts[k] + pp["t"], "pop", 0.7)
        photos = sc.get("photos", [])
        photos_by_scene.append(photos)
        for ph in photos:
            place(starts[k] + ph.get("t", 0.1), "mouse")
        if vtype == "photo_hook" and k == 0:
            place(0.0, "mouse")

    mix = np.clip(voice_track * 0.95 + fx, -1, 1)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "mix.wav")
    sf.write(wav, mix, SR)

    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac",
         "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)

    bg_big = make_background(W, H, theme)
    parts = Particles(W, H, theme)
    brand_f = font(S * 0.034, "ExtraBold")
    src_f = font(S * 0.026, "Medium")
    ticker = spec.get("ticker")
    hl_words = set(w.lower() for w in spec.get("highlight_words", []))
    sticker_cache = {}
    rng = random.Random(9)

    n_frames = int(total * FPS)
    for fi in range(n_frames):
        t = fi / FPS
        idx = min(int(np.searchsorted(starts, t, side="right") - 1), len(scenes) - 1)
        sc, dur, words = scenes[idx]
        lt = t - starts[idx]
        vtype = sc["visual"]["type"]

        # moving grid background
        off = int((t * 40) % 100)
        img = bg_big.crop((off, off, off + W, off + H))
        d = ImageDraw.Draw(img)
        parts.draw(d, img, t)
        dy = sc["visual"].get("dy", 0)
        if dy and vtype != "photo_hook":
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            VISUALS[vtype][0](ImageDraw.Draw(layer), layer, W, H, lt, dur, sc["visual"])
            img.paste(layer, (0, int(dy * H)), layer)
        else:
            VISUALS[vtype][0](d, img, W, H, lt, dur, sc["visual"])

        # photo cards pop in with a click
        for ph in photos_by_scene[idx]:
            st = ph.get("t", 0.1)
            if lt < st:
                continue
            a = ease_back((lt - st) / 0.22)
            card = photo_card(ph["file"], int(W * ph.get("w", 0.7)))
            paste_scaled(img, card, W * ph.get("x", 0.5), H * ph.get("y", 0.25), a, ph.get("rot", 0))

        # pop-up stickers / emoji
        for pp in pops_by_scene[idx]:
            if lt < pp["t"]:
                continue
            a = ease_back((lt - pp["t"]) / 0.28)
            wob = math.sin((lt - pp["t"]) * 7) * 3
            key = (pp["text"], pp.get("color", "accent"), pp.get("emoji", False))
            if key not in sticker_cache:
                sticker_cache[key] = emoji_img(pp["text"], int(S * 0.2)) if pp.get("emoji") else sticker(pp["text"], pp.get("color", "accent"), int(S * 0.055))
            paste_scaled(img, sticker_cache[key], W * pp.get("x", 0.5), H * pp.get("y", 0.25), a, pp.get("rot", 0) + wob)

        # punch-in zoom at scene start + slow drift, shake on impact
        punch = 1 + 0.07 * (1 - ease_out(lt / 0.28))
        drift = 1 + 0.025 * (lt / max(dur, 0.1))
        z = punch * drift
        if z > 1.001:
            zw, zh = int(W * z), int(H * z)
            img = img.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        if lt < 0.18:
            sx, sy = rng.randint(-9, 9), rng.randint(-9, 9)
            img = img.transform(img.size, Image.AFFINE, (1, 0, sx, 0, 1, sy), fillcolor=PALETTE["bg"])
        d = ImageDraw.Draw(img)

        # chrome
        if ticker:
            draw_ticker(d, W, H, t, ticker)
        d.rectangle([0, H - 12, W * t / total, H], fill=PALETTE["accent"])
        if sc.get("source"):
            d.text((W / 2, H * 0.94), "Source: " + sc["source"], font=src_f, fill=PALETTE["muted"], anchor="mm")
        if vtype != "outro":
            wi = next((i for i, (a0, b0, _) in enumerate(words) if a0 <= lt < b0), None)
            if wi is not None:
                draw_caption(d, W, H, words, wi, lt - words[wi][0], hl_words)

        # white flash on cut
        if idx > 0 and lt < 0.07:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.35 * (1 - lt / 0.07))
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()
    return total


if __name__ == "__main__":
    secs = render(sys.argv[1], sys.argv[2])
    print(f"rendered {sys.argv[2]} ({secs:.1f}s)")
