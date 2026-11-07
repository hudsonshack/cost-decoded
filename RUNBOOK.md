# Cost Decoded: weekly production runbook

This file is the standing instruction set for the weekly scheduled run. Follow it top to bottom.

## Channel
- **Name:** Cost Decoded. **Promise:** the real cost of everything, decoded with data.
- **Niche:** everyday economics and business explainers (how companies really make money, what things really cost, hidden fees, price history, "why is X so expensive"). YouTube category: EDUCATION.
- **Audience:** US, 18-45, curious about money and business. Plain English, no jargon, no hype.
- **Not allowed:** personalized financial or investment advice ("you should buy..."), stock picks, crypto pumping, politics, tragedies, health claims, anything about real private individuals, reused clips or footage from other creators.

## Output
- 1-2 Shorts every day (35-50 s each): one at 12:30, a second at 18:30 on the strongest topics. Adjust volume and mix to whatever analytics and current trends show gets the most views.
- 1 long-form video (6-10 min) a week once Shorts are performing, scheduled Thursday.
- Formats: single-topic breakdowns, countdown rankings (#5 to #1), and timely news angles. Pick the mix from what is trending in money/business Shorts that week and from our own analytics.
- Post times: use Metricool `getBestTimeToPostByNetwork` for YouTube once the channel has data; until then 12:30 and 18:30 America/New_York.

## Step 1: Review last week (skip in week 1)
1. Pull YouTube analytics (see Analytics below): views, average view duration, average percentage viewed and subscribers gained per video.
2. Note the top and bottom performer and why (hook, topic, length).
3. Append 3-5 bullet learnings to `LEARNINGS.md` and apply them this week.

## Step 2: Pick topics
1. Research what is getting views in the niche right now: search the web for trending business and money news from the last 14 days, and check comparable channels' recent uploads.
2. Pick topics that pass all four tests: (a) a surprising number at the center, (b) explainable in under a minute, (c) at least two reputable sources (company filings, major news outlets, government data), (d) not already covered in `TOPICS.md`.
3. Mix: 2 evergreen ("How Costco makes money on a $1.50 hot dog"), 1 timely (this week's news), 1 ranking ("5 most expensive...").
4. Log chosen topics in `TOPICS.md` with date and sources.

## Style rules (locked formula, engine v3)
- **Pacing:** a new visual every ~1 second. Scenes are one short sentence (2-3 s). Each scene gets a base visual or 1-3 `cues` that pop in on specific words.
- **Hook:** scene 1 is a `photo_hook` with a custom hook for that topic (a number or claim plus an open loop). Model hooks on what's performing in the niche that week; never reuse one word-for-word.
- **Captions:** 1-2 words at a time, synced to the voice, heavy white caps with black stroke, numbers/money in lime. Write numbers as `{$4.65|four sixty five}` so the caption shows digits and the voice says words.
- **Images:** real photos (CC0 / public domain / CC BY via `photos.py search/get`), shown as white-bordered `card`s, or cut out with `photos.py cutout <slug>` and popped in as outlined `cutout`s that stack. Look at every photo and cutout before use. Never use photos of real people. No branded items from the wrong company.
- **Extras:** `bigword` (huge word behind everything, with a hit), `sticker` badges, `emoji`, `rain` (falling cash) for money moments.
- **Sound:** click on every photo/cutout, pop on stickers, low hit on big words, quiet whoosh on cuts. No music.
- **Ending:** no end card. The last line ends abruptly and should flow back into the hook for replays.
- **Voice:** free smooth voice, speed 1.10-1.12.

## Step 3: Script (JSON in `shorts/` or `long/`)
- One idea per scene, 1-2 sentences of narration. 6-9 scenes for a Short.
- Every number on screen gets a `source` field. Use the exact figure from the source; round only in narration.
- Write numbers in narration the way they are spoken ("four sixty five", "two hundred forty five million").
- Vary the visual types (`big_number`, `compare_bars`, `donut`, `statement`, `people_grid`, plus `photos` cards and `pops` stickers) so no two videos have the same sequence. This matters for YouTube's inauthentic-content rules. Use `dy` to push a visual down when a photo card sits above it.
- End with a one-line takeaway, then the outro.
- Fill `title` (under 60 characters, curiosity + number), `description` (2-3 sentence summary, a Sources list, 3-4 hashtags) and `tags`.

## Step 4: Fact-check (do not skip)
Re-open every source and confirm each on-screen figure, date and quote. If a figure can't be confirmed from two sources, cut the scene or the topic. Never publish a guess.

## Step 5: Render and QA
1. `python3 engine.py <script.json> out/<slug>.mp4`
2. Extract frames from every scene and look at them: no clipped text, no overlapping elements, captions readable.
3. Check loudness is between -17 and -13 LUFS and the length is 30-58 s for Shorts.

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
