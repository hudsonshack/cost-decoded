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
  1. **Story** (50-90 s, 150-170 words, 10-14 scenes). Model: Silas Business "Why Costco's Hotdog is Only $1.50" (469K views on a 4K-sub channel, same topic as our 452-view Costco Short).
     Beats: the familiar thing and its "impossible" number -> the problem (costs rise, a law, a rival) -> a person or turning point, ideally with a quote ("he said he'd kill him") -> how they solved it -> "But here's the interesting part:" the real business engine -> back to the opening number (loop).
  2. **Paradox** (60-100 s). Model: Business Explains The World "How North Korea actually makes money" (389K, 4.3% likes, 575 comments).
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

## A/B tests (approved by Hudson, Nov 7)
Run each test on one new video, change nothing else, and log it in LEARNINGS.md under "A/B tests" (file, date, what changed).
Compare against the other videos in the Monday report (views, likes per view, comments, and average percentage viewed if Metricool shows it).
Report the result to Hudson and let him decide whether it becomes the default.
1. **Female narrator** (next new video, expected Nov 12): set `"voice": "af_heart", "speed": 1.0` in the script. No music. Use the Story format so it compares cleanly with 005 (popcorn).
2. **Quiet beat** (the new video after that, expected Nov 13): current voice, plus `"music": {"file": "assets/music/empty-street-static.mp3", "db": -22, "duck_db": 4}`. For videos over 95 s use `high-rise-haze.mp3`. Story format.
Preview any script's audio in seconds without rendering frames: `AUDIO_ONLY=1 python3 engine.py <script.json> out/<name>.mp4` writes `out/<name>.wav`.
Until a test is adopted, every other video stays on the current voice with no music.

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
- Vary the visual types (`split_bars`, `ticker`, `compare_bars`, `nodes`, `big_number`, `donut`, `statement`, `people_grid`, b-roll with `archival: true` for history, cutouts, emoji, `follow`) so no two videos have the same sequence. Visuals can reveal on spoken words with `"reveal_at": ["word1", "word2"]` (split_bars, compare_bars, ticker). This matters for YouTube's inauthentic-content rules. Use `dy` to push a visual down when a photo card sits above it.
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
