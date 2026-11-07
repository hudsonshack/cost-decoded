"""Cost Decoded video engine v3 (inspo-matched editing style).

Style (from the reference Shorts): a visual change roughly every second, 1-2 word
flash captions synced to the voice (money/number words in lime), cutout objects and
photo cards that spring in (0 -> 110% -> 100%) with a click and stack up, huge
background words, slow push-ins, hard cuts, and an abrupt ending that loops.

Script JSON (per scene):
  say      narration text
  visual   optional base visual (big_number, compare_bars, donut, statement, people_grid, photo_hook, none)
  cues     list of timed pop-ins:
           {"at": "<word in the narration>" | "t": seconds,
            "type": "cutout" | "card" | "sticker" | "emoji" | "bigword" | "rain",
            "file", "text", "color", "x", "y", "w", "rot"}
  source   on-screen source line

Usage: python3 engine.py script.json out.mp4
"""
import json, math, os, random, re, subprocess, sys, tempfile
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from scipy.signal import resample_poly

from engine_v2 import (HERE, FONT_DIR, FPS, SR, PALETTE, font, ease_out, ease_back, col, fade, tts, SFX, SFX_GAIN,
                       fit_font, sticker, emoji_img, paste_scaled, photo_card, make_background, Particles,
                       draw_ticker, VISUALS)

LIME = (70, 255, 110)
BLACK_W = "Black" if os.path.exists(f"{FONT_DIR}Inter-Black.otf") else "ExtraBold"
from look import GridBG, bloom, light_leak, nodes_cue_times  # noqa: E402  (registers broll/photo_hook/nodes visuals)

# ---------------------------------------------------------------- word timing (whisper)
_whisper = None


def align(audio):
    """Return [(word, start, end)] for a 24 kHz mono clip."""
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    a16 = resample_poly(audio, 2, 3).astype(np.float32)
    segs, _ = _whisper.transcribe(a16, word_timestamps=True, language="en")
    words = []
    for s in segs:
        for w in s.words:
            txt = w.word.strip()
            if not txt:
                continue
            if words and re.match(r"^[.,%]", txt):  # glue "$1" + ".50"
                p = words[-1]
                words[-1] = (p[0] + txt, p[1], w.end)
            else:
                words.append((txt, w.start, w.end))
    return words


def norm(s):
    return re.sub(r"[^a-z0-9$%]", "", s.lower())


BRACE = re.compile(r"\{([^|}]+)\|([^}]+)\}")


def parse_say(say):
    """'{1,513|fifteen hundred and thirteen} clients' -> spoken text + display tokens [(display, n_spoken_words)]."""
    spoken = BRACE.sub(lambda m: m.group(2), say)
    tokens, pos = [], 0
    for m in BRACE.finditer(say):
        for w in say[pos:m.start()].split():
            tokens.append((w, 1))
        tail = re.match(r"\S*", say[m.end():]).group(0)  # punctuation glued to the brace, e.g. "}."
        tokens.append((m.group(1) + tail, len(m.group(2).split())))
        pos = m.end() + len(tail)
    for w in say[pos:].split():
        tokens.append((w, 1))
    return spoken, tokens


def timed_tokens(spoken, tokens, words, clip_dur):
    """Start/end time for every display token, using whisper words as anchors."""
    import difflib
    sw = spoken.split()
    a = [norm(x) for x in sw]
    b = [norm(w[0]) for w in words]
    times = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = words[blk.b + k][1]
    lead = words[0][1] if words else 0.0
    end = words[-1][2] if words else clip_dur
    chars = np.cumsum([0] + [len(x) + 1 for x in sw])
    frac = chars / chars[-1]
    anchors = [(-1, lead)] + [(i, t) for i, t in enumerate(times) if t is not None] + [(len(sw), end)]
    for i in range(len(sw)):
        if times[i] is None:
            prev = max((x for x in anchors if x[0] < i), key=lambda x: x[0])
            nxt = min((x for x in anchors if x[0] > i), key=lambda x: x[0])
            fp = frac[prev[0]] if prev[0] >= 0 else 0.0
            fn = frac[nxt[0]] if nxt[0] < len(sw) else 1.0
            fi = frac[i]
            times[i] = prev[1] + (nxt[1] - prev[1]) * ((fi - fp) / max(fn - fp, 1e-6))
    out, wi = [], 0
    for disp, n in tokens:
        out.append([disp, times[wi], None, wi])
        wi += n
    for k in range(len(out)):
        out[k][2] = out[k + 1][1] if k + 1 < len(out) else end
    return [tuple(x) for x in out]


def bursts(words):
    """1-2 word caption bursts: short words ride along with the next word."""
    out, i = [], 0
    while i < len(words):
        w = words[i]
        if len(norm(w[0])) <= 3 and i + 1 < len(words) and not re.search(r"[\d$]", words[i + 1][0]) and not re.search(r"[.,?!]$", w[0]):
            out.append((w[0] + " " + words[i + 1][0], w[1], words[i + 1][2]))
            i += 2
        else:
            out.append(w)
            i += 1
    return out


# ---------------------------------------------------------------- assets
_cut_cache = {}


def cutout_sticker(path, width, outline=False):
    """Cutout PNG with a white outline and soft shadow, like the reference edits."""
    key = (path, width, outline)
    if key in _cut_cache:
        return _cut_cache[key]
    full = path if os.path.isabs(path) else os.path.join(HERE, path)
    im = Image.open(full).convert("RGBA")
    if not outline:
        r = width / im.width
        im = im.resize((int(width), max(1, int(im.height * r))), Image.LANCZOS)
        pad = 30
        out = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
        a = Image.new("L", out.size, 0)
        a.paste(im.split()[3], (pad, pad + 14))
        sh = Image.new("RGBA", out.size, (0, 0, 0, 255))
        sh.putalpha(a.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.75)))
        out.alpha_composite(sh)
        out.alpha_composite(im, (pad, pad))
        _cut_cache[key] = out
        return out
    r = width / im.width
    im = im.resize((int(width), max(1, int(im.height * r))), Image.LANCZOS)
    pad = max(12, int(width * 0.05))
    canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    a = Image.new("L", canvas.size, 0)
    a.paste(im.split()[3], (pad, pad))
    stroke = a.filter(ImageFilter.MaxFilter(size=(max(3, int(width * 0.018)) // 2) * 2 + 1))
    shadow = stroke.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
    sh.putalpha(shadow)
    out = Image.new("RGBA", (canvas.width + 12, canvas.height + 16), (0, 0, 0, 0))
    out.alpha_composite(sh, (12, 16))
    white = Image.new("RGBA", canvas.size, (255, 255, 255, 255))
    white.putalpha(stroke)
    out.alpha_composite(white, (0, 0))
    out.alpha_composite(im, (pad, pad))
    _cut_cache[key] = out
    return out


def spring(x):
    """0 -> 110% -> 100% pop."""
    x = max(0.0, min(1.0, x))
    if x < 0.6:
        return 1.1 * ease_out(x / 0.6)
    return 1.1 - 0.1 * ease_out((x - 0.6) / 0.4)


# ---------------------------------------------------------------- drawing pieces
def draw_bigword(img, W, H, text, color, k):
    S = min(W, H)
    d = ImageDraw.Draw(img)
    f = fit_font(d, text, W * 0.96, S * 0.32, BLACK_W)
    f = font(f.size * (1.25 - 0.25 * ease_out(k)), BLACK_W)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((W / 2, H * 0.36), text, font=f, fill=col(color) + (int(235 * min(1, k * 2)),), anchor="mm")
    img.paste(layer, (0, 0), layer)


def draw_caption(d, W, H, text, t_in, hl):
    S, land = min(W, H), W > H
    s = re.sub(r"[.,;:]+$", "", text.upper())
    key = norm(text)
    is_money = bool(re.search(r"[\d$%]", text)) or any(norm(h) and norm(h) in key for h in hl)
    f = fit_font(d, s, W * 0.84, S * (0.07 if land else 0.082), BLACK_W)
    f = font(f.size * spring(t_in / 0.14) if t_in < 0.14 else f.size, BLACK_W)
    y = H * (0.86 if land else 0.74)
    d.text((W / 2 + 4, y + 6), s, font=f, fill=(0, 0, 0), anchor="mm", stroke_width=max(3, int(f.size * 0.06)), stroke_fill=(0, 0, 0))
    d.text((W / 2, y), s, font=f, fill=PALETTE["good"] if is_money else (255, 255, 255), anchor="mm",
           stroke_width=max(2, int(f.size * 0.035)), stroke_fill=(0, 0, 0))


# ---------------------------------------------------------------- render
def render(script_path, out_path):
    spec = json.load(open(script_path))
    vertical = spec.get("format", "short") == "short"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    S = min(W, H)
    theme = spec.get("theme", "default")
    voice, speed = spec.get("voice", "voice_smooth.npy"), spec.get("speed", 1.12)
    hl = spec.get("highlight_words", [])
    gap = 0.06  # tight gaps between scenes keep the pace up

    scenes, audio = [], []
    for sc in spec["scenes"]:
        spoken, disp_tokens = parse_say(sc["say"])
        a = tts(spoken, voice, speed)
        words = align(a)
        toks = timed_tokens(spoken, disp_tokens, words, len(a) / SR)
        dur = len(a) / SR + gap
        audio.append(np.concatenate([a, np.zeros(int(gap * SR), np.float32)]))
        # cue times come from the matching script word's aligned start time
        cues, si = [], 0
        for c in sc.get("cues", []):
            c = dict(c)
            if "at" in c and "t" not in c:
                target = norm(c["at"])
                pos = next((j for j in range(si, len(toks)) if target and target in norm(toks[j][0])), None)
                if pos is None:
                    pos = next((j for j in range(len(toks)) if target in norm(toks[j][0])), 0)
                si = pos + 1
                c["t"] = toks[pos][1]
            cues.append(c)
        scenes.append({"sc": sc, "dur": dur, "words": words, "bursts": bursts([(t[0], t[1], t[2]) for t in toks]), "cues": cues})

    voice_track = np.concatenate(audio + [np.zeros(int(0.12 * SR), np.float32)])
    total = len(voice_track) / SR
    starts = np.cumsum([0] + [s["dur"] for s in scenes])

    # ---- sound: clicks for photos/cutouts, pops for stickers, low hit for big words, quiet whoosh on cuts
    fx = np.zeros_like(voice_track)

    def place(at, name, gain=1.0):
        i = int(max(0, at) * SR)
        clip = SFX[name] * SFX_GAIN[name] * gain
        j = min(len(fx), i + len(clip))
        if i < len(fx):
            fx[i:j] += clip[: j - i]

    place(0.0, "impact", 0.55)
    for k, s in enumerate(scenes):
        if k > 0:
            place(starts[k] - 0.08, "whoosh", 0.35)
        vt = s["sc"].get("visual", {}).get("type")
        if vt == "photo_hook":
            place(starts[k] + 0.02, "mouse")
        if vt == "nodes":
            for tt in nodes_cue_times(s["sc"]["visual"]):
                place(starts[k] + tt, "mouse", 0.9)
        for c in s["cues"]:
            name, g = {"cutout": ("mouse", 1.0), "card": ("mouse", 1.0), "sticker": ("pop", 0.8),
                       "emoji": ("pop", 0.8), "bigword": ("impact", 0.5), "rain": ("whoosh", 0.4)}.get(c["type"], ("pop", 0.6))
            place(starts[k] + c["t"], name, g)
    mix = np.clip(voice_track * 0.95 + fx, -1, 1)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "mix.wav")
    sf.write(wav, mix, SR)

    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac",
         "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)

    stage = GridBG(W, H)
    rain = Particles(W, H, "wallstreet", n=18, seed=11)
    src_f = font(S * 0.026, "Medium")
    ticker = spec.get("ticker")
    rng = random.Random(9)
    asset_cache = {}

    def asset(c):
        key = (c["type"], c.get("file"), c.get("text"), c.get("w"), c.get("color"))
        if key not in asset_cache:
            w = int(W * c.get("w", 0.5))
            if c["type"] == "cutout":
                asset_cache[key] = cutout_sticker(c["file"], w, c.get("outline", False))
            elif c["type"] == "card":
                asset_cache[key] = photo_card(c["file"], w)
            elif c["type"] == "sticker":
                asset_cache[key] = sticker(c["text"], c.get("color", "accent"), int(S * 0.06))
            elif c["type"] == "emoji":
                asset_cache[key] = emoji_img(c["text"], int(S * c.get("w", 0.2)))
        return asset_cache[key]

    for fi in range(int(total * FPS)):
        t = fi / FPS
        idx = min(int(np.searchsorted(starts, t, side="right") - 1), len(scenes) - 1)
        s = scenes[idx]
        sc, lt, dur = s["sc"], t - starts[idx], s["dur"]
        vis = sc.get("visual", {"type": "none"})
        vtype = vis.get("type", "none")

        img = stage.frame(t)
        d = ImageDraw.Draw(img)

        full_bleed = vtype in ("broll", "photo_hook")
        # big words sit behind graphics, but on top of full-screen photos
        if not full_bleed:
            for c in s["cues"]:
                if c["type"] == "bigword" and lt >= c["t"]:
                    draw_bigword(img, W, H, c["text"], c.get("color", "bad"), (lt - c["t"]) / 0.35)

        if vtype != "none":
            dy = vis.get("dy", 0)
            if dy and vtype != "photo_hook":
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                VISUALS[vtype][0](ImageDraw.Draw(layer), layer, W, H, lt, dur, vis)
                img.paste(layer, (0, int(dy * H)), layer)
            else:
                VISUALS[vtype][0](d, img, W, H, lt, dur, vis)

        if full_bleed:
            for c in s["cues"]:
                if c["type"] == "bigword" and lt >= c["t"]:
                    draw_bigword(img, W, H, c["text"], c.get("color", "bad"), (lt - c["t"]) / 0.35)
        if any(c["type"] == "rain" and lt >= c["t"] for c in s["cues"]):
            rain.draw(d, img, t)

        # stacked pop-ins
        for c in s["cues"]:
            if c["type"] in ("bigword", "rain") or lt < c["t"]:
                continue
            k = (lt - c["t"]) / 0.24
            wob = math.sin((lt - c["t"]) * 5) * 1.5
            paste_scaled(img, asset(c), W * c.get("x", 0.5), H * c.get("y", 0.25), spring(k), c.get("rot", 0) + wob)

        # camera: punch-in on every cut + slow push-in through the scene
        z = (1 + 0.06 * (1 - ease_out(lt / 0.22))) * (1 + 0.05 * (lt / max(dur, 0.1)))
        zw, zh = int(W * z), int(H * z)
        img = img.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        shake = any(c["type"] == "bigword" and 0 <= lt - c["t"] < 0.15 for c in s["cues"])
        if shake:
            img = img.transform(img.size, Image.AFFINE, (1, 0, rng.randint(-10, 10), 0, 1, rng.randint(-10, 10)),
                                fillcolor=PALETTE["bg"])
        img = bloom(img, W, H)
        if idx > 0 and idx % 3 == 1 and lt < 0.32:
            img = light_leak(img, W, H, lt / 0.32)
        d = ImageDraw.Draw(img)

        if ticker:
            draw_ticker(d, W, H, t, ticker)
        d.rectangle([0, H - 10, W * t / total, H], fill=PALETTE["accent"])
        if sc.get("source"):
            d.text((W / 2, H * 0.94), "Source: " + sc["source"], font=src_f, fill=PALETTE["muted"], anchor="mm")
        cur = next((b for b in reversed(s["bursts"]) if b[1] <= lt), None)
        if cur and lt < cur[2] + 0.35:
            draw_caption(d, W, H, cur[0], lt - cur[1], hl)
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()
    return total


if __name__ == "__main__":
    secs = render(sys.argv[1], sys.argv[2])
    print(f"rendered {sys.argv[2]} ({secs:.1f}s)")
