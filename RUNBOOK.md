# Cost Decoded: weekly production runbook

This file is the standing instruction set for the weekly scheduled run. Follow it top to bottom.

## Channel
- **Name:** Cost Decoded. **Promise:** the real cost of everything, decoded with data.
- **Niche:** everyday economics and business explainers (how companies really make money, what things really cost, hidden fees, price history, "why is X so expensive"). YouTube category: EDUCATION.
- **Audience:** US, 18-45, curious about money and business. Plain English, no jargon, no hype.
- **Not allowed:** personalized financial or investment advice ("you should buy..."), stock picks, crypto pumping, politics, tragedies, health claims, anything about real private individuals, reused clips or footage from other creators.

## Output
- 1-2 Shorts every day at 12:30 (a second at 18:30 once the Metricool cap allows). Length depends on the format (see the Replication playbook below): Story and Paradox Shorts run 50-90 s, Trick Shorts 25-40 s. Adjust volume and mix to whatever analytics and current trends show gets the most views.
- 1 long-form video (6-10 min) a week once Shorts are performing, scheduled Thursday.
- Formats: rotate the three playbook formats (Story, Paradox, Trick). Never post the same format three days in a row. Rankings (#5 to #1) and timely news angles are fine as long as they follow one of the three structures.
- Post times: use Metricool `getBestTimeToPostByNetwork` for YouTube once the channel has data; until then 12:30 and 18:30 America/New_York.

## Step 1: Review last week (skip in week 1)
1. Pull YouTube analytics (see Analytics below): views, average view duration, average percentage viewed and subscribers gained per video.
2. Note the top and bottom performer and why (hook, topic, length).
3. Append 3-5 bullet learnings to `LEARNINGS.md` and apply them this week.

## Step 2: Pick topics
1. Research what is getting views in the niche right now: search the web for trending business and money news from the last 14 days, and check comparable channels' recent uploads.
2. Pick topics that pass all five tests: (a) a brand or thing nearly everyone has used (Costco, Apple, Starbucks, movie theaters, gas stations), (b) a story (a person, a turning point, a twist) or one clean trick, (c) a surprising number at the center, (d) at least two reputable sources (company filings, major news outlets, government data), (e) not already covered in `TOPICS.md`.
3. Mix: lean on evergreen brand stories, add a timely hook whenever this week's news connects (a viral product, a price change, a lawsuit), and make every second or third video a "they're doing this to you" topic (fees, shrinkflation, tipping screens, dynamic pricing), because those pull 5-10x more comments.
4. Log chosen topics in `TOPICS.md` with date and sources.

## Style rules (locked formula, engine v4 "premium dark")
Matched frame-by-frame to Hudson's reference Shorts. Keep every video in this style.
- **Full-bleed first:** most scenes fill the whole frame. Use `broll` (full-screen graded photo with slow push/pan) for anything that has a photo; use the black grid-floor stage only for data graphics. Never leave big empty space.
- **Pacing:** Story/Paradox scenes are one sentence (3-6 s) with motion inside (push-in, 1-2 cues, a chart that builds); Trick scenes are 2-3 s. Something on screen changes every 1-2 s either way.
- **Hook:** scene 1 is a `photo_hook` (full-screen photo + huge headline, red highlight on the key number). Custom per topic: a number or claim plus an open loop. Never reuse a hook word-for-word.
- **Big words:** `bigword` cues for the key number or word (green for money, red for emphasis). On broll scenes they sit on top of the photo.
- **Graphics:** `compare_bars`, `donut`, `people_grid`, `statement` on the grid stage; `nodes` for breakdowns (white icon circles joined by lines with letter-spaced labels; `hot: true` turns a label green).
- **No repeats:** every photo and cutout appears only once per video. Gather 6-8 different images per Short (more angles, more varieties) before writing cues.
- **Cutouts:** objects cut out with `photos.py cutout <slug>` rise in from the bottom edge (y ~0.68-0.72) with a shadow and no outline. Avoid branded items from the wrong company.
- **Captions:** 1-2 words, synced, clean white heavy caps with a soft shadow, numbers/money in green. Write numbers as `{$4.65|four sixty five}` so the caption shows digits.
- **Look:** palette is black / white / red `#FF3030` / green `#39FF6A`; bloom glow, green corner flare and light-leak flashes are automatic.
- **Sound:** click on every photo/cutout/node/bar, pop on stickers, low hit on big words, soft ticks on counters, quiet whoosh on cuts. No music, except the approved A/B test below (all three studied winners use a very quiet beat).
- **Ending:** no end card. The last line is a half-sentence that runs straight into the hook's first words (e.g. "Which is exactly why" -> "Theaters are selling a $90 popcorn bucket"), so the Short loops. A `follow` cue (SUBSCRIBE pill that gets tapped) may pop in during the last 2 s.
- **Replication playbook (Nov 7, from a vidIQ study of the niche's top Shorts; details in LEARNINGS.md):**
  Every winner tells a story about a brand everyone knows; none of them is a list of stats. Pick one format per video:
  1. **Story** (45-55 s for now, see Traction fixes; 120-140 words, 9-12 scenes). Model: Silas Business "Why Costco's Hotdog is Only $1.50" (469K views on a 4K-sub channel, same topic as our 452-view Costco Short).
     Beats: the familiar thing and its "impossible" number -> the problem (costs rise, a law, a rival) -> a person or turning point, ideally with a quote ("he said he'd kill him") -> how they solved it -> "But here's the interesting part:" the real business engine -> back to the opening number (loop).
  2. **Paradox** (45-55 s for now, see Traction fixes). Model: Business Explains The World "How North Korea actually makes money" (389K, 4.3% likes, 575 comments).
     Hook = two facts that can't both be true ("most sanctioned country on Earth... yet it has money for a water park"). Then "So how does X actually make money?", split the answer into 2-3 buckets (legal / weird / hidden), end with a three-item summary that loops ("crypto, arms and fake ponytails: that's what the wallet is made of").
  3. **Trick** (25-40 s, 70-100 words). Model: Sisenco Digital "Why does Apple let you play with their phones for hours?" (162K views, 1,823x its channel average, 4.5% likes) and TruthBro shrinkflation (828K, 2.2K comments).
     Hook = a question about something everyone has noticed. Name the trick (Endowment Effect), prove it with one big number ("Apple made billions"), give the viewer one takeaway.
  Rules for all three:
  - Hook in the first 2 s: brand + an impossible number, a question, or a paradox. Timely beats evergreen: tie it to this week's news when you can ("Theaters are selling a $90 Godzilla popcorn bucket").
  - One explanatory visual per idea, not decoration: `split_bars` (where each $1 goes), `ticker` (a year or count rolling up), `compare_bars`, `nodes`, a cutout of the exact object, `archival` b-roll for history beats.
  - One "wait, what?" turn in the middle (a ban, a threat, a reversal, a villain).
  - Conversational narration: "Funny thing is...", "But here's the interesting part:", "Now they're doing it again." No stacked statistics.
  - First comment: a two-option question people want to answer ("Be honest: sneak snacks in, or pay for the popcorn?").
  - Variety protects monetization: YouTube's inauthentic-content policy targets templated, mass-produced channels, so no two videos in a row share a format or visual order, and every script must contain real research and a point of view.
- **Voice:** free smooth voice, speed 1.05 for Story/Paradox (about 160 words a minute, like the winners), 1.10 for Trick.

## Nov 13 review: why views dropped, and the fixes (these override older rules where they conflict)
Studio data (first 8 Shorts, ~4K views, 2 subscribers): 55% of viewers swiped away. Best: airlines, 60% stayed, 48% average viewed (male voice + beat, 45 s, shock number + brand in line 1). Worst: Black Friday, 80% swiped, and shopping cart, 60% swiped, which YouTube then barely showed (40 and 9 views); both were the female narrator. The 62 s Story (popcorn) kept only 35% on average. Every Short lost viewers in the first second because the headline faded in after the opening frame.
Rules from now on:
1. **The first frame sells the video.** The photo_hook headline is now on screen from frame 1 (engine change). The opening photo must show the exact subject (the product, the brand's store or logo-free signage, the object), never a vague mood shot. Headline is 2 short lines (12 characters max each) that state the shocking claim.
2. **Line 1 is a claim the viewer feels, in 10 words or fewer:** a "you" angle or a famous brand plus a number that sounds wrong ("McDonald's isn't really a burger company." / "It takes 300 streams to make one dollar."). No dates, setup or names before the claim.
3. **Length 30-45 s for every format** (Story included). Cut scenes until it fits; the best performer was 45 s.
4. **Voice and music: Setup B (current male voice + quiet beat) is the default.** The A/B decision rule fired early on a large gap: Setup A averaged 30% stayed-to-watch vs 60% for B. Don't use the female narrator unless a future test says otherwise.
5. **Swipe-away target: 35% or less (65%+ stayed).** Any video over 55% swiped gets a written cause in the review log, and the next script must fix that cause.
6. **Post time test:** the 17:00 ET airlines post beat every 12:30 post. Alternate 12:30 and 17:00 for the next 6 videos and log which wins.
7. **Opening photo passes the US-viewer test (Nov 14, from 003 + 008):** the frame-0 photo shows the exact product or brand a US viewer knows, with English signage only (no foreign-language text), and the headline says what it does to YOU or names the brand + number. Look at frame 0 before scheduling and reject any photo that fails.

## Daily review loop (every run, before making anything new)
1. Read the Google Sheet "Cost Decoded stats" (spreadsheet id 1FF4QKssRrnTG4NhKu8Oa0pSUmsVrycpd_UjeOcRJwPc, Sheet1). A local check on Hudson's Mac copies YouTube Studio numbers into it each afternoon (views, stayed to watch %, swiped away %, watch time, likes, subscribers). If a published video has no row yet, add its row (ID, title, file, published time, length, setup, format) and leave the Studio columns blank.
2. For every video at least 24 h old whose "Review notes" are blank or say "Studio check to fill in": compare it with the channel's best and median. Name the most likely cause of a weak result from this checklist, in order: (a) opening frame and headline, (b) first spoken line, (c) topic relevance for US viewers, (d) length vs avg view, (e) voice/music setup, (f) visual pacing in the first 5 s, (g) post time. Write a one-line cause + fix in "Review notes" and in LEARNINGS.md "Video reviews".
3. Apply the fix to the next script you make today, and say in the script JSON `"review_fix"` what you changed and why.
4. If the same cause shows up in 2 or more videos, make it a rule in this section and commit it.
5. If the newest Short is still in the 24-48 h window with fewer than 100 views and 60%+ swiped, don't repeat its topic type, hook pattern or opening image style in the next video.
6. Never change already-published videos. Fixing already-scheduled ones (hook headline, first line, setup) is allowed when the review shows a clear problem.

## A/B tests (approved by Hudson, Nov 7; split rule set the same evening)
Hudson liked both previews. Already-scheduled videos stay as they are. Every NEW video alternates between the two setups:
- **Setup A, female narrator:** `"voice": "af_heart", "speed": 1.0`, no music.
- **Setup B, quiet beat:** current voice (default), plus `"music": {"file": "assets/music/empty-street-static.mp3", "db": -22, "duck_db": 4}` (use `high-rise-haze.mp3` for videos over 95 s).
Start with A on the next new video (expected Nov 12), then B, then A, and so on. Check LEARNINGS.md "A/B tests" for which setup the last video used, and log each one (file, date, setup, format).
**Decision rule (you decide, then tell Hudson):** once each setup has at least 3 videos with 3+ days of data, compare interaction per view: (likes + comments) / views, plus average percentage viewed if Metricool shows it. If one setup is at least 30% higher and its views aren't clearly lower, make it the default for every video, note it in LEARNINGS.md, and report it in the next Monday report. Otherwise keep alternating and re-check weekly.
Spread formats across both setups (don't put every Story on A and every Trick on B), so the format doesn't skew the comparison.
Preview any script's audio in seconds without rendering frames: `AUDIO_ONLY=1 python3 engine.py <script.json> out/<name>.mp4` writes `out/<name>.wav`.

## Proof moments (approved by Hudson, Nov 7)
- In about half the videos, add one `proof` scene (3-4 s): a paper card with a VERBATIM line from a company filing, court record or major outlet, with a highlighter sweep over the key phrase. Modeled on the highlighted article screenshots in Business Explains The World's breakouts.
- Spec: `{"type": "proof", "kicker": "AMC Entertainment, 2025 annual report", "quote": "<exact words, 12-30 words>", "highlight": "<exact sub-phrase>", "hl_at": 0.5}`.
- Rules: copy the words exactly from the source (re-open it to check); quotes from news outlets stay under 15 words; the card is plain paper, never a recreation of an outlet's or company's page design or logo. This is the only on-screen sourcing allowed (no footer source lines).
- Narrate it naturally ("In its own annual report, AMC says...") so it reads as a story beat, not a citation.

## Cross-posting (Hudson, Nov 9: YouTube ONLY for now)
- Post to YouTube only, even though TikTok is connected in Metricool. Hudson will reinvest YouTube earnings into a paid Metricool plan once the channel shows real traction; then every Short goes to YouTube, Instagram, TikTok and Snapchat at 2-3 videos a day. Don't cross-post or raise volume until he says so.
- Old rule, kept for when he switches it on: one Metricool post with providers youtube + tiktok + instagram, `instagramData: {"type": "REEL", "showReelOnFeed": true}`, `tiktokData: {"privacyOption": "PUBLIC_TO_EVERYONE", "title": "<title>"}`, same text and first comment.

## Traction fixes (approved by Hudson, Nov 9; apply to EVERY video)
1. **Thumbnail / cover frame:** every Metricool post sets `videoCoverMilliseconds` to the hook frame with the big headline fully drawn (about 1500 ms; extract that frame and check it). Store it as `cover_ms` in the script. YouTube may only show custom Shorts covers once the channel is verified; set it anyway. (YouTube had auto-picked meaningless mid-video frames like "SAVED / REFUSED".)
2. **Hook lands in the first second:** the first spoken words ARE the surprising number or claim. No setup line first. The headline with that number is on screen from the first frames.
3. **Length:** Story and Paradox Shorts run 45-55 s until a longer one proves it holds viewers (Trick stays 25-40 s). This overrides the older 50-90 s range in the playbook above.
- Judge videos by "Viewed vs. swiped away" in YouTube Studio (Hudson can send screenshots), not early view counts; vidIQ view counts can be hours stale.

## Metadata rules (every upload)
- **Title:** under 60 characters, written as the plain question people search ("Why Movie Theater Popcorn Is So Expensive", "How North Korea Actually Makes Money"), brand or subject first, no hashtags. Check demand with vidiq_keyword_research when credits allow.
- **Description line 1:** one keyword-rich sentence that adds something the title doesn't (not a restatement).
- **Description line 2:** 3-4 hashtags: 1-2 niche (#costco, #wolfofwallstreet), 1 broad (#money or #business), plus #shorts. The first three show above the title.
- **Then:** a blank line, the Sources line and the Photos credit line.
- **Tags:** 5-8 (main keyword, variants, broad topic).
- **First comment:** a short question that invites an opinion, stored as `first_comment` in the script and sent as Metricool `firstCommentText`.
- **Media URL:** use the commit-pinned raw URL (`https://raw.githubusercontent.com/hudsonshack/cost-decoded/<commit sha>/media/<file>.mp4`); the `main` URL can serve a cached 404 for a few minutes after a push.

## Step 3: Script (JSON in `shorts/` or `long/`)
- One idea per scene, 1-2 sentences of narration. Story/Paradox: 10-14 scenes. Trick: 7-9 scenes. Set `"playbook"` in the JSON to story, paradox or trick.
- Every number gets a `source` field in the script JSON for fact-checking only. Nothing source-related is drawn on screen (Hudson's call, Nov 7); sources live in the description.
- Write numbers in narration the way they are spoken ("four sixty five", "two hundred forty five million").
- Vary the visual types (`split_bars`, `ticker`, `proof`, `compare_bars`, `nodes`, `big_number`, `donut`, `statement`, `people_grid`, b-roll with `archival: true` for history, cutouts, emoji, `follow`) so no two videos have the same sequence. Visuals can reveal on spoken words with `"reveal_at": ["word1", "word2"]` (split_bars, compare_bars, ticker). This matters for YouTube's inauthentic-content rules. Use `dy` to push a visual down when a photo card sits above it.
- End with a one-line takeaway, then the outro.
- Fill `title` (under 60 characters, curiosity + number), `description` (2-3 sentence summary, a Sources list, 3-4 hashtags) and `tags`.

## Step 4: Fact-check (do not skip)
Re-open every source and confirm each on-screen figure, date and quote. If a figure can't be confirmed from two sources, cut the scene or the topic. Never publish a guess.

## Step 5: Render and QA
1. `python3 engine.py <script.json> out/<slug>.mp4`
2. Extract frames from every scene and look at them: no clipped text, no overlapping elements, captions readable.
3. Check loudness is between -17 and -13 LUFS and the length fits the format: Story/Paradox 50-90 s, Trick 25-40 s.

## Step 6: Publish (free routing, no paid tools)
Hudson can't create a Google API key, so the direct-API route (`youtube_api.py`) is shelved. Use these two routes:
1. **Metricool free plan** (20 posts a month): commit the MP4s to `media/` and push. Public URL: `https://raw.githubusercontent.com/<owner>/<repo>/main/media/<file>.mp4`. Schedule with `createScheduledPost`: provider `youtube`, `youtubeData.type` = `short` or `video`, `madeForKids` false, category `EDUCATION`, privacy public, title and tags from the script, description as the post text. Track the month's count in `LEARNINGS.md` and stop at 20.
2. **Mac upload** (for anything over the Metricool cap): write the MP4s and a `schedule.txt` (title, description, tags, publish time per file) into the connected Mac folder `Cost Decoded/upload-queue`, then use computer control to open YouTube Studio in Chrome, upload the batch, fill each title and description, and set "Schedule" with the publish time. Needs the MacBook awake and the Claude desktop app open; if it isn't reachable, leave the files in the queue and tell Hudson in the report.

After scheduling, by any route:
- Add or update a 15-minute event in Hudson's Notion Calendar (Google account thehudsonshack@gmail.com, primary calendar) for every scheduled post: title "🎬 Cost Decoded Short: <title>" (or "Video" for long-form), description with status, file name and which route posted it. If a planned event's topic changed, update that event instead of adding a duplicate.
- Delete media files older than 30 days that are already published.

## Analytics
Pull last week's numbers from Metricool analytics, and from YouTube Studio's Analytics tab in Chrome for anything Metricool doesn't show (swipe-away rate, retention curve).

## Step 7: Report
Once the formula is locked, only contact Hudson about analytics and recommended changes: what was scheduled, how last week performed, and what you think should change (and why). Ask him before any major change to the formula. Also flag anything that needs him (a connection that broke, a policy notice).
