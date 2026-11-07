"""Direct YouTube posting + analytics for Cost Decoded (no third-party scheduler).

Works once Hudson's Google Cloud project passes YouTube's free API compliance audit.
Until then uploads from this project are locked private by YouTube, so keep using
Metricool free / Mac uploads and don't call `upload` for public videos.

Secrets: secrets/youtube.json (never commit), with
  {"client_id": "...", "client_secret": "...", "refresh_token": "..."}

Commands:
  python3 youtube_api.py auth                         # one-time: prints a sign-in link, then paste the redirected URL
  python3 youtube_api.py upload <script.json> <video.mp4> <publishAt ISO, e.g. 2026-12-01T12:30:00-05:00>
  python3 youtube_api.py analytics <startYYYY-MM-DD> <endYYYY-MM-DD>
"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS = os.path.join(HERE, "secrets", "youtube.json")
SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/yt-analytics.readonly https://www.googleapis.com/auth/youtube.readonly"
REDIRECT = "http://localhost:8080"


def _secrets():
    return json.load(open(SECRETS))


def _post(url, data, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST")
    return urllib.request.urlopen(req, timeout=120)


def access_token():
    s = _secrets()
    body = urllib.parse.urlencode({"client_id": s["client_id"], "client_secret": s["client_secret"],
                                   "refresh_token": s["refresh_token"], "grant_type": "refresh_token"}).encode()
    return json.load(_post("https://oauth2.googleapis.com/token", body))["access_token"]


def auth():
    s = _secrets()
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": s["client_id"], "redirect_uri": REDIRECT, "response_type": "code", "scope": SCOPES,
        "access_type": "offline", "prompt": "consent"})
    print("Open this link, sign in with the channel's Google account, approve, then copy the full URL you land on "
          "(the page itself won't load, that's expected):\n\n" + url)
    landed = input("\nPaste that URL here: ").strip()
    code = urllib.parse.parse_qs(urllib.parse.urlparse(landed).query)["code"][0]
    body = urllib.parse.urlencode({"code": code, "client_id": s["client_id"], "client_secret": s["client_secret"],
                                   "redirect_uri": REDIRECT, "grant_type": "authorization_code"}).encode()
    tok = json.load(_post("https://oauth2.googleapis.com/token", body))
    s["refresh_token"] = tok["refresh_token"]
    json.dump(s, open(SECRETS, "w"), indent=1)
    print("Saved refresh token.")


def upload(script_path, video_path, publish_at):
    spec = json.load(open(script_path))
    meta = {
        "snippet": {"title": spec["title"][:100], "description": spec["description"],
                    "tags": spec.get("tags", []), "categoryId": "27"},  # 27 = Education
        "status": {"privacyStatus": "private", "publishAt": publish_at,  # private + publishAt = scheduled
                   "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False},
    }
    tok = access_token()
    start = _post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                  json.dumps(meta).encode(),
                  {"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                   "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(os.path.getsize(video_path))})
    session = start.headers["Location"]
    data = open(video_path, "rb").read()
    req = urllib.request.Request(session, data=data, method="PUT",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    res = json.load(urllib.request.urlopen(req, timeout=600))
    print(json.dumps({"id": res["id"], "status": res.get("status")}, indent=1))
    return res["id"]


def analytics(start, end):
    tok = access_token()
    q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": start, "endDate": end,
                                "metrics": "views,averageViewDuration,averageViewPercentage,subscribersGained,likes,shares",
                                "dimensions": "video", "sort": "-views", "maxResults": 50})
    req = urllib.request.Request("https://youtubeanalytics.googleapis.com/v2/reports?" + q,
                                 headers={"Authorization": f"Bearer {tok}"})
    print(json.dumps(json.load(urllib.request.urlopen(req, timeout=60)), indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"auth": auth, "upload": lambda: upload(*sys.argv[2:5]), "analytics": lambda: analytics(*sys.argv[2:4])}[cmd]()
