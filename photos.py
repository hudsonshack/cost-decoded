"""Find and download openly licensed photos (CC0 / public domain / CC BY) via Openverse.
search:   python3 photos.py search "query"            -> prints candidates
download: python3 photos.py get <slug> <url> "<credit>" -> assets/photos/<slug>.jpg, logs credit
"""
import json, os, sys, urllib.parse, urllib.request, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "assets", "photos")
CREDITS = os.path.join(DIR, "credits.json")

def search(q, n=8):
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "license": "cc0,pdm,by", "page_size": n, "mature": "false"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "cost-decoded/1.0"}), timeout=20))
    for r in d["results"]:
        if (r.get("width") or 0) >= 700:
            print(f'{r["license"]:4} {r["width"]}x{r["height"]} | {(r["title"] or "")[:45]} | {r["creator"]} | {r["url"]}')

def get(slug, url, credit):
    os.makedirs(DIR, exist_ok=True)
    out = os.path.join(DIR, slug + ".jpg")
    subprocess.run(["curl", "-sL", "-m", "60", "-A", "cost-decoded/1.0", "-o", out + ".raw", url], check=True)
    from PIL import Image
    im = Image.open(out + ".raw").convert("RGB")
    im.thumbnail((1600, 1600))
    im.save(out, quality=90)
    os.remove(out + ".raw")
    c = json.load(open(CREDITS)) if os.path.exists(CREDITS) else {}
    c[slug] = credit
    json.dump(c, open(CREDITS, "w"), indent=1)
    print(out, im.size)

if __name__ == "__main__":
    if sys.argv[1] != "cutout": {"search": lambda: search(sys.argv[2]), "get": lambda: get(*sys.argv[2:5])}[sys.argv[1]]()


def cutout(slug):
    """Remove the background of assets/photos/<slug>.jpg -> assets/cutouts/<slug>.png (trimmed)."""
    from rembg import remove, new_session
    from PIL import Image
    out_dir = os.path.join(HERE, "assets", "cutouts")
    os.makedirs(out_dir, exist_ok=True)
    im = Image.open(os.path.join(DIR, slug + ".jpg"))
    im.thumbnail((1000, 1000))
    cut = remove(im, session=new_session("u2netp"))
    a = cut.split()[3].point(lambda v: 255 if v > 40 else 0)
    cut.putalpha(Image.eval(cut.split()[3], lambda v: v) if True else a)
    cut = cut.crop(a.getbbox() or (0, 0, cut.width, cut.height))
    cut.save(os.path.join(out_dir, slug + ".png"))
    print(os.path.join(out_dir, slug + ".png"), cut.size)


if __name__ == "__main__" and sys.argv[1] == "cutout":
    for s in sys.argv[2:]:
        cutout(s)
