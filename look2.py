"""v5 storytelling devices for the Cost Decoded engine, modeled on the top niche Shorts
(Silas Business, Business Explains The World, Sisenco Digital):

  split_bars  "where your $1 goes": 100% stacked bars that fill left to right (Silas's cost-block breakdown)
  ticker      a counter that rolls from one number to another (Silas's year/volume counter pattern interrupt)
  follow pill a small SUBSCRIBE pill that pops in and gets clicked in the last second or two (Silas, Sisenco)

Archival photo grading (sepia, grain, flicker) lives in look.py's v_broll (`"archival": true`).
"""
import math, os, re
from PIL import Image, ImageDraw, ImageFilter

from engine_v2 import (HERE, FONT_DIR, PALETTE, VISUALS, font, ease_out, ease_back, fade, fit_font, emoji_img,
                       paste_scaled, col)
from look import spaced_text

BLACK_W = "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold"
DARK = (10, 10, 12)


def _spring(x):
    x = max(0.0, min(1.0, x))
    return 1.1 * ease_out(x / 0.6) if x < 0.6 else 1.1 - 0.1 * ease_out((x - 0.6) / 0.4)


def _reveal_times(s, n, first=0.35, step=1.1):
    t = list(s.get("_t") or [])
    while len(t) < n:
        t.append(first + step * len(t) if not t else t[-1] + step)
    return t[:n]


# ---------------------------------------------------------------- split bars
def v_split_bars(d, img, W, H, t, dur, s):
    S = min(W, H)
    bars = s["bars"]
    times = _reveal_times(s, len(bars))
    unit = s.get("unit", "")
    if s.get("title"):
        a = ease_out(t / 0.35)
        tf = font(S * 0.05, "Bold")
        while tf.size > 24 and sum(d.textlength(ch, font=tf) for ch in s["title"].upper()) + S * 0.012 * len(s["title"]) > W * 0.9:
            tf = font(tf.size - 2, "Bold")
        spaced_text(d, (W / 2, H * 0.165), s["title"].upper(), tf, fade(PALETTE["text"], a), S * 0.012)
    x0, x1 = W * 0.07, W * 0.93
    bh = S * 0.16
    lab_f = font(S * 0.058, BLACK_W)
    for k, bar in enumerate(bars):
        rt = times[k]
        if t < rt - 0.05:
            continue
        yc = H * (s.get("y0", 0.32) + s.get("gap", 0.215) * k)
        a = ease_out((t - rt + 0.05) / 0.25)
        # label above the bar
        d.text((x0, yc - bh / 2 - S * 0.045), bar["label"].upper(), font=lab_f, fill=fade(PALETTE["text"], a), anchor="lm")
        # empty track
        d.rounded_rectangle([x0, yc - bh / 2, x1, yc + bh / 2], radius=int(bh * 0.22), fill=(28, 28, 34))
        p = ease_out((t - rt) / 0.7) if t > rt else 0
        total = sum(pt["value"] for pt in bar["parts"])
        x = x0
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for pt in bar["parts"]:
            w = (x1 - x0) * pt["value"] / total
            fill_w = max(0.0, min(w, (x1 - x0) * p - (x - x0)))
            if fill_w > 1:
                ld.rectangle([x, yc - bh / 2, x + fill_w, yc + bh / 2], fill=col(pt.get("color", "good")) + (255,))
            if p > (x - x0 + w * 0.6) / (x1 - x0):
                ta = ease_out((t - rt - 0.35) / 0.3)
                tc = DARK if pt.get("color", "good") == "good" else (255, 255, 255)
                vf = font(S * 0.078, BLACK_W)
                sf = font(S * 0.033, "Bold")
                val = f'{pt.get("prefix", "")}{pt["value"]}{pt.get("unit", unit)}'
                cx = x + w / 2
                ld.text((cx, yc - S * 0.012), val, font=vf, fill=tc + (int(255 * ta),), anchor="mm")
                if pt.get("label"):
                    ld.text((cx, yc + bh * 0.30), pt["label"].upper(), font=sf, fill=tc + (int(230 * ta),), anchor="mm")
            x += w
        # round the ends by masking with the track shape
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rounded_rectangle([x0, yc - bh / 2, x1, yc + bh / 2], radius=int(bh * 0.22), fill=255)
        img.paste(layer, (0, 0), Image.composite(layer.split()[3], Image.new("L", (W, H), 0), mask))
        # a part marked "hot" gets a glowing outline once the fill lands
        for pt_i, pt in enumerate(bar["parts"]):
            if pt.get("hot") and p >= 0.99:
                xs = x0 + (x1 - x0) * sum(q["value"] for q in bar["parts"][:pt_i]) / total
                xe = xs + (x1 - x0) * pt["value"] / total
                g = 0.5 + 0.5 * math.sin((t - rt) * 6)
                d.rounded_rectangle([xs - 4, yc - bh / 2 - 4, xe + 4, yc + bh / 2 + 4], radius=int(bh * 0.25),
                                    outline=fade(PALETTE["good"], 0.55 + 0.45 * g), width=max(4, int(S * 0.006)))
    if s.get("note"):
        last = times[-1] + 0.9
        if t > last:
            nf = font(S * 0.05, "Bold")
            spaced_text(d, (W / 2, H * s.get("note_y", 0.66)), s["note"].upper(), nf,
                        fade(PALETTE["good"], ease_out((t - last) / 0.35)), S * 0.01)


def c_split_bars(s):
    out = []
    for rt in _reveal_times(s, len(s["bars"])):
        out.append((rt, "mouse"))
    return out


# ---------------------------------------------------------------- ticker
def _ticker_value(s, t):
    t0, dc = s.get("count_at", 0.15), s.get("count_dur", 1.4)
    k = max(0.0, min(1.0, (t - t0) / dc))
    e = 1 - (1 - k) ** 3
    return s["from"] + (s["to"] - s["from"]) * e


def v_ticker(d, img, W, H, t, dur, s):
    S = min(W, H)
    t0, dc = s.get("count_at", 0.15), s.get("count_dur", 1.4)
    v = _ticker_value(s, t)
    txt = s.get("prefix", "") + (f"{int(round(v))}" if s.get("plain", True) else f"{int(round(v)):,}") + s.get("suffix", "")
    final = s.get("prefix", "") + str(s["to"]) + s.get("suffix", "")
    cy = H * s.get("y", 0.38)
    base = fit_font(d, final, W * 0.86, S * s.get("size", 0.30), BLACK_W)
    landed = t >= t0 + dc
    pop = _spring((t - t0 - dc) / 0.3) if landed else 1.0
    f = font(base.size * pop, BLACK_W)
    c = col(s.get("color", "text"))
    if landed and t - t0 - dc < 0.7:
        k = ease_out((t - t0 - dc) / 0.7)
        r = S * (0.22 + 0.32 * k)
        d.ellipse([W / 2 - r, cy - r, W / 2 + r, cy + r], outline=fade(col(s.get("ring", "good")), 0.7 * (1 - k)), width=int(S * 0.012))
    # slight roll while counting
    roll = 0 if landed else math.sin(t * 60) * S * 0.004
    d.text((W / 2, cy + roll), txt, font=f, fill=c, anchor="mm", stroke_width=max(3, int(f.size * 0.03)), stroke_fill=(0, 0, 0))
    if s.get("label_top"):
        a = ease_out(t / 0.3)
        spaced_text(d, (W / 2, cy - base.size * 0.72), s["label_top"].upper(), font(S * 0.05, "Bold"), fade(PALETTE["muted"], a), S * 0.012)
    hl = set(re.sub(r"\W", "", w.lower()) for w in s.get("highlight", []))
    for i, line in enumerate(s.get("lines", [])):
        st = t0 + dc + 0.15 + 0.25 * i
        if t < st:
            continue
        a = ease_out((t - st) / 0.3)
        lf = fit_font(d, line.upper(), W * 0.9, S * 0.062, BLACK_W)
        y = cy + base.size * 0.70 + i * lf.size * 1.25 + (1 - a) * 30
        total = d.textlength(line.upper(), font=lf)
        x = W / 2 - total / 2
        for w in line.upper().split():
            cc = PALETTE["good"] if re.sub(r"\W", "", w.lower()) in hl else PALETTE["text"]
            d.text((x, y), w, font=lf, fill=fade(cc, a), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0))
            x += d.textlength(w + " ", font=lf)


def c_ticker(s):
    """A quiet tick each time the shown number changes, then a hit when it lands."""
    t0, dc = s.get("count_at", 0.15), s.get("count_dur", 1.4)
    out, last, steps = [], None, 400
    for i in range(steps + 1):
        tt = t0 + dc * i / steps
        v = int(round(_ticker_value(s, tt)))
        if v != last:
            if last is not None and (not out or tt - out[-1][0] > 0.045):
                out.append((tt, "tick"))
            last = v
    out.append((t0 + dc, "impact"))
    return out


VISUALS["split_bars"] = (v_split_bars, c_split_bars)
VISUALS["ticker"] = (v_ticker, c_ticker)


# ---------------------------------------------------------------- follow pill
_pill_cache = {}


def _pill(W, H, state):
    key = (W, H, state)
    if key not in _pill_cache:
        S = min(W, H)
        pw, ph = int(W * 0.56), int(S * 0.115)
        im = Image.new("RGBA", (pw + 40, ph + 50), (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([20, 32, 20 + pw, 32 + ph], radius=ph // 2, fill=(0, 0, 0, 170))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        d = ImageDraw.Draw(im)
        fill = PALETTE["accent"] if state == "on" else (48, 48, 56)
        d.rounded_rectangle([20, 20, 20 + pw, 20 + ph], radius=ph // 2, fill=fill + (255,))
        label = "SUBSCRIBE" if state == "on" else "SUBSCRIBED"
        f = fit_font(d, label, pw * 0.62, S * 0.05, BLACK_W)
        bell = emoji_img("🔔", int(ph * 0.55))
        tw = d.textlength(label, font=f)
        gx = 20 + pw / 2 - (bell.width + 14 + tw) / 2
        im.alpha_composite(bell, (int(gx), int(20 + ph / 2 - bell.height / 2)))
        d.text((gx + bell.width + 14, 20 + ph / 2), label, font=f, fill=(255, 255, 255), anchor="lm")
        _pill_cache[key] = im
    return _pill_cache[key]


def draw_follow(img, W, H, lt, c):
    """Pill springs in, a hand taps it at +0.55 s, it flips to SUBSCRIBED."""
    k = lt - c["t"]
    if k < 0:
        return
    click = c.get("click", 0.55)
    state = "on" if k < click else "off"
    sc = _spring(k / 0.25)
    if click <= k < click + 0.12:
        sc *= 0.93
    x, y = W * c.get("x", 0.5), H * c.get("y", 0.60)
    paste_scaled(img, _pill(W, H, state), x, y, sc)
    if k < click + 0.45:
        S = min(W, H)
        hand = emoji_img("👆", int(S * 0.11))
        hy = y + S * 0.16 - S * 0.10 * ease_out(min(1, k / click))
        paste_scaled(img, hand, x + W * 0.16, hy, 1.0 if k < click else 0.92)


# ---------------------------------------------------------------- proof card
def v_proof(d, img, W, H, t, dur, s):
    """A 'receipt' moment: a paper card with a verbatim line from a filing or article and a highlighter sweep.
    s = {"kicker": "AMC 2025 annual report", "quote": "...exact words...", "highlight": "exact sub-phrase", "hl_at": 0.6}
    Generic paper styling on purpose: it must never imitate a real outlet's page design."""
    S = min(W, H)
    a = ease_out(t / 0.35)
    cw, pad = W * 0.84, S * 0.055
    qf = font(S * 0.058, "Bold")
    lines = []
    for para in [s["quote"]]:
        words, cur = para.split(), ""
        for w in words:
            test = (cur + " " + w).strip()
            if d.textlength(test, font=qf) > cw - pad * 2:
                lines.append(cur); cur = w
            else:
                cur = test
        lines.append(cur)
    lh = qf.size * 1.32
    kf = font(S * 0.032, "Bold")
    ch = pad * 2 + kf.size * 2.0 + lh * len(lines)
    x0, y0 = (W - cw) / 2, H * s.get("y", 0.40) - ch / 2 + (1 - a) * 60
    card = Image.new("RGBA", (int(cw) + 60, int(ch) + 60), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 42, 30 + cw, 42 + ch], radius=18, fill=(0, 0, 0, 190))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([30, 30, 30 + cw, 30 + ch], radius=18, fill=(246, 243, 236, 255))
    cd.text((30 + pad, 30 + pad), s.get("kicker", "").upper(), font=kf, fill=(120, 116, 108))
    cd.line([(30 + pad, 30 + pad + kf.size * 1.45), (30 + cw - pad, 30 + pad + kf.size * 1.45)], fill=(205, 200, 190), width=3)
    ty = 30 + pad + kf.size * 2.0
    hl = s.get("highlight", "")
    k = ease_out((t - s.get("hl_at", 0.6)) / 0.6) if t > s.get("hl_at", 0.6) else 0
    # find highlight span across lines (by character offsets)
    full = " ".join(lines)
    hs = full.find(hl) if hl else -1
    he = hs + len(hl) if hs >= 0 else -1
    pos = 0
    total_hl_chars = max(1, he - hs)
    for ln in lines:
        ls, le = pos, pos + len(ln)
        if hs >= 0 and k > 0 and hs < le and he > ls:
            a0, a1 = max(hs, ls), min(he, le)
            done = min(a1, hs + int(total_hl_chars * k))
            if done > a0:
                xa = 30 + pad + cd.textlength(ln[: a0 - ls], font=qf)
                xb = 30 + pad + cd.textlength(ln[: done - ls], font=qf)
                cd.rectangle([xa - 4, ty + qf.size * 0.12, xb + 4, ty + qf.size * 1.12], fill=(255, 226, 60, 255))
        cd.text((30 + pad, ty), ln, font=qf, fill=(24, 24, 28))
        ty += lh
        pos = le + 1
    if a < 1:
        card.putalpha(card.split()[3].point(lambda v: int(v * a)))
    img.paste(card, (int(x0 - 30), int(y0 - 30)), card)


def c_proof(s):
    return [(0.0, "mouse"), (s.get("hl_at", 0.6), "tick")]


VISUALS["proof"] = (v_proof, c_proof)
