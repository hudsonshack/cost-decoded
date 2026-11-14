# Learnings

Append weekly findings from analytics here.

## Metricool post count
- 2026-11: Metricool counter shows 2 of 20 published (001 YouTube Nov 7, 001 TikTok Nov 7). Scheduled: 002 Nov 8 (YouTube + TikTok in one post), 005 Nov 9, 004 Nov 10, 003 Nov 11.
- Cross-post test: a TikTok-only post counted as 1. Nov 8's Wolf post goes to YouTube + TikTok as ONE post: if the counter goes 2 -> 3 it counts once per post; 2 -> 4 means once per network. Check the planner banner after 12:30 Nov 8 and record the answer here.
- Nov 8 run (14:44 ET): the Wolf post published on both networks (YouTube PM87c0MpATA, TikTok 7705854513109880078). The planner counter isn't exposed through the Metricool API, so the once-per-post vs once-per-network answer is still open. Month count is 3 or 4 of 20 either way; until confirmed, count cross-posts per network (worst case). Nov 9-11 already scheduled, so no new Short this run.
- Note for the next run: the Nov 13 planned calendar event "Why Movie Theater Popcorn Costs So Much" repeats 005 (scheduled Nov 9). Swap that day for a fresh topic.
- Nov 9 run: 005 published Nov 9 (YouTube only). Scheduled 006 shopping cart for Nov 12 as ONE post to YouTube + TikTok. Running count, worst case (cross-posts per network): published 5 (001 YT, 001 TT, 002 YT, 002 TT, 005 YT); scheduled 004 Nov 10 (YT), 003 Nov 11 (YT), 006 Nov 12 (YT+TT) -> 9 of 20 by Nov 12. 006 Metricool post uuid 1321449761553862175.
- Nov 9 afternoon (Hudson live): YouTube ONLY until real traction (006 updated to YouTube only, cover 1500 ms). Extra Short 007 airlines scheduled today 17:00 ET (uuid -5752663574413753750, cover 1500 ms). Count now: published 5; scheduled 007 Nov 9, 004 Nov 10, 003 Nov 11, 006 Nov 12 (all YouTube only) -> 9 of 20 by Nov 12.
- Nov 10 run (19:30 ET): 007 and 004 published. Scheduled 008 Black Friday deals for Nov 13 12:30 (YouTube only, cover 1500 ms, uuid -7018952521915809451). Count, worst case: published 7 (001 YT+TT, 002 YT+TT, 005, 007, 004); scheduled 003 Nov 11, 006 Nov 12, 008 Nov 13 -> 10 of 20 by Nov 13. Nov 13 calendar event (old popcorn repeat) updated to 008.
- Nov 11 run (15:10 ET): 003 published today. Scheduled 009 McDonald's real estate for Nov 14 12:30 (YouTube only, cover 1500 ms, uuid -4349776586941051807). Count, worst case: published 8 (001 YT+TT, 002 YT+TT, 005, 007, 004, 003); scheduled 006 Nov 12, 008 Nov 13, 009 Nov 14 -> 11 of 20 by Nov 14. Nov 14 "open slot" calendar event updated to 009.
- Nov 12 run (15:05 ET): 006 published today (YouTube XVq2VOtdQGo). Nov 13 and 14 already filled, so one new Short: 010 Spotify pay per stream for Nov 15 12:30 (YouTube only, cover 1500 ms, uuid 5048371595564564834). Count, worst case: published 9 (001 YT+TT, 002 YT+TT, 005, 007, 004, 003, 006); scheduled 008 Nov 13, 009 Nov 14, 010 Nov 15 -> 12 of 20 by Nov 15. Nov 15 planned calendar event updated to 010. Remaining planned events: latte (Nov 16), subscription traps (Nov 17), Netflix hikes (Nov 18), concert ticket fees (Nov 19).
- Nov 13 run (15:05 ET): 008 published today (YouTube _Q_FLsw9sgA). Nov 14 and 15 already filled, so one new Short: 011 Starbucks secret Short size for Nov 16 12:30 (YouTube only, cover 1500 ms, uuid 4375066299797884676). Count, worst case: published 10 (001 YT+TT, 002 YT+TT, 005, 007, 004, 003, 006, 008); scheduled 009 Nov 14, 010 Nov 15, 011 Nov 16 -> 13 of 20 by Nov 16. Nov 16 planned latte event updated to 011 (a '$7 latte costs X to make' number couldn't be confirmed from two sources, so the latte slot became the Starbucks Short-size trick). Remaining planned events: subscription traps (Nov 17), Netflix hikes (Nov 18), concert ticket fees (Nov 19), and 'Are Black Friday Deals Actually Deals?' (Nov 20), which REPEATS 008: swap Nov 20 for a fresh topic.

## Production notes
- 2026-11-07: bigword text wider than ~5 characters spills off the frame during the punch-in; keep bigwords to 4-5 characters. Node labels over ~13 characters get cut at the side edges. Emoji with square silhouettes (📅 ↩️) render as blank squares in node icons; use shaped ones (⏳ 🔓 💰 🔍).

- 2026-11-09: Flickr (live.staticflickr.com) and Wikimedia return 429 "CIDR range blocked" from the cloud session. Download Openverse results through Openverse's own proxy instead: `curl -sL https://api.openverse.org/v1/images/<id>/thumb/?full_size=true&compressed=false` (full 1024 px). Openverse search often 504s; retry it in a loop, queries in parallel. `photos.py get` (direct Flickr URL) fails while this lasts.
- 2026-11-09: faster-whisper 1.2.1 with av 19 can't decode files (`metadata_errors` TypeError); pass numpy arrays (the engine already does). The first `pip install -q` in setup.sh sat idle for 10+ min; a rerun without -q finished in under a minute.
- 2026-11-09: compare_bars reveal words near the END of a sentence leave the second bar on screen for under half a second; reveal the first bar on an early word and add a short tail phrase after the reveal word. Basket emoji 🧺 reads as a face in node icons; 👜 works.

- 2026-11-10: setup.sh's `pip install -q` hung again (5+ min, no output); killing it and rerunning without -q finished in under a minute. 🏬 (department store) renders as a blank square in node icons like 📅; 🛍️ works. Ticker takes `"plain": false` to print thousands separators (2,600).

- 2026-11-11: Openverse's thumb proxy returns "Thumbnail unavailable from provider" for Wikimedia results; only Flickr/StockSnap results download. split_bars: a part with color "text" renders as a white block with no label, and a single bar leaves most of the frame empty; use two bars or compare_bars. compare_bars reveals items in list order, so put the item named EARLY in the sentence first.

- 2026-11-12: rembg u2netp left the white background inside a headphone band; `isnet-general-use` cut it cleanly, but its soft alpha made the object look see-through on video. Harden the alpha (threshold ~60, 1 px blur) and crop off long cables, or the bbox shrinks the object on screen. Cutout `w` ~0.85 is needed for a wide object to read at full size. Bigwords: 4 characters (NONE, 100K) fit at rest; 5 (13.8K) clip during the punch-in. A proof scene lasts as long as its narration, so give it a 3+ s line.

- 2026-11-13: compare_bars with a reveal word mid-sentence leaves the chart empty for 1.5-2 s if the sentence opens with setup words; start the sentence with the first reveal word (e.g. "Product costs are just 32¢...") or reveal on the first number token ("2006"). photo_hook lines of 15 characters (NOT ON THE MENU) touch the frame edges at scale 0.12; 12 characters fit. A 4-letter bigword in wide letters (SAME) still clips the edges; 3 letters (ONE) fit. statement at scale 0.085 fits a 14-letter word (DISCRIMINATION).

## 2026-11-09: week 1 analytics (Monday report)
Data: vidIQ get_videos_by_ids (5 credits) at 14:45 ET Nov 9; Metricool YouTube per-video stats still null (2-3 day lag) and Metricool returned no TikTok post rows.
- 001 Costco hot dog (trick-style, 30 s, published Nov 7): 1,227 views, 12 likes, 1 comment, (likes+comments)/views 1.06%, ~25 views/hour.
- 002 Wolf of Wall Street (32 s, Nov 8): 816 views, 8 likes, 1 comment, 1.10%, ~31 views/hour (pacing ahead of Costco at the same age).
- 005 Popcorn (first Story Short, 62 s, Nov 9 12:30): 2 views and 1 comment 2 h after publishing, versus Costco's 452 at 5 h. Either a slow first test batch or the longer Story isn't being pushed; re-check at 24 h before judging the Story format.
Learnings applied this week:
1. Both 30 s stat Shorts landed at ~1.1% interaction, about a third of the niche winners (3-4%). Nothing yet beats the playbook; keep Story/Paradox on the next videos rather than reverting.
2. A person-and-twist story with a concrete date and an "everyone hated it" turn tests best in the study, so the Nov 12 Short (shopping cart) leads with the claim "built to make you spend more" plus the open loop "nobody would touch it".
3. Titles stay as the plain search question ("Why Was the Shopping Cart Invented?"); judge 005's packaging only after 24-72 h.
4. Metricool analytics lag means the Monday report should lean on vidIQ for videos under 3 days old; budget 5 credits a week (35 left until Dec 6).

## 2026-11-07: vidIQ study of the niche's highest-interaction Shorts
Our first Short (Costco, 30 s, stat-heavy) had 452 views, 1.8% likes and 1 comment after ~5 h. The same week, a 4K-subscriber
faceless channel posted the same topic as a 91 s story and got 469K views (3.3% likes, 97 comments). Breakouts studied
(views, likes/views, comments, length):
- Silas Business, "Why Costco's Hotdog is Only $1.50": 469K, 3.3%, 97, 91 s. 228 words (~152 wpm), 18 shots (~4.7 s each),
  3D animated scenes, cost-block margin graphic, year counter, supply-chain cross-out, founder quote as the turn, loops 1985 $1.50 -> still $1.50.
- Silas Business, "How Feastables Saved MrBeast": 713K, 2.1%, 44, 78 s.
- Business Explains The World, "How North Korea actually makes money": 389K, 4.3%, 575, 117 s. Paradox hook, legal/illicit buckets,
  black-and-yellow charts, highlighted article screenshots, three-item summary that loops. Human female narrator ~165 wpm, quiet music bed.
- Sisenco Digital, "Why does Apple let you play with their phones for hours?": 162K (1,823x channel average), 4.5%, 33, 34 s.
  Question hook about a familiar oddity, named concept (Endowment Effect), "made billions", one takeaway, follow CTA.
- PureBusiness "How Costco Was Founded" 229K/4.3%; Healer Of Wallets "Costco Secrets" 63K (35x)/4.0%; Ankit Bansal Costco loss leader 116K/3.1%.
- Comment magnets are "they're doing this to you" topics: TruthBro shrinkflation 828K / 2.2K comments (27 s), Mappelz "Shake Shack tried
  to pull a fast one" 5.1M / 2.7K, More Perfect Union "McDonald's doesn't want you to see this" 2.8M / 5.7K, pink tax 717K / 2.0K (10.6% likes).
Takeaways now in the runbook:
1. Story beats stats. Every winner is a narrative about a brand everyone knows, with a turn in the middle.
2. Length follows the format: stories run 60-120 s; only single-trick videos work at ~30 s. (This reverses the 22-30 s cap set earlier the same day.)
3. Every visual explains the sentence it sits under (margin bars, counters, maps), held 3-5 s with motion, rather than a new picture every second.
4. Human-sounding narration at 150-165 wpm, all three with a quiet music bed. Our free TTS and no-music rule are the two biggest remaining gaps.
5. Packaging is plain: titles are the question people ask ("Why Costco's Hotdog is Only $1.50"); descriptions are one line; tags barely matter.
6. Policy: YouTube's inauthentic-content policy (renamed July 2025, clarified July 2026, enforced in waves since Jan 2026) targets templated,
   mass-produced channels. Rotating formats and real research per video is also monetization insurance.

## A/B tests
- Approved Nov 7: female narrator (Kokoro af_heart, speed 1.0) on the next new video; quiet beat (Open Lo-Fi "Empty Street Static", CC0, -22 dB, ducked 4 dB under speech) on the one after. Previews: both transcribe word-for-word; the beat sits about 20 dB under the voice.
- Nov 7 evening: Hudson liked both previews. Rule now: scheduled videos stay as-is; new videos alternate Setup A (female narrator) and Setup B (current voice + quiet beat), starting with A. After 3+ videos each, switch to the winner if its interaction per view is 30%+ higher.
- Log: 006-shopping-cart (sched. Nov 12) = Setup A (af_heart, speed 1.0, no music), Story format. Next new video uses Setup B; make it a Trick or Paradox so formats spread across setups.
- Log: 007-how-airlines-make-money (Nov 9 17:00) = Setup B (default voice, speed 1.05, Empty Street Static -22 dB), Paradox format, 45 s. Next new video: Setup A.
- Log: 008-black-friday-fake-deals (Nov 13) = Setup A (af_heart, speed 1.0, no music), Trick format, 32 s, no proof scene (006 and 007 both had one). Setup A so far: Story (006) + Trick (008); Setup B: Paradox (007). Next new video: Setup B; make it a Story so formats keep spreading.
- Log: 009-mcdonalds-real-estate (Nov 14) = Setup B (default voice, speed 1.05, Empty Street Static -22 dB), Story format, 55 s, with proof scene (10-K quote). Setup A so far: Story (006) + Trick (008); Setup B: Paradox (007) + Story (009). Next new video: Setup A; make it a Paradox or Trick so formats keep spreading.
- Log: 010-spotify-pay-per-stream (Nov 15) = Setup A (af_heart, speed 1.0, no music), Paradox format, 55 s, with proof scene (Spotify for Artists quote). Setup A so far: Story (006) + Trick (008) + Paradox (010); Setup B: Paradox (007) + Story (009). Next new video: Setup B; make it a Trick so B gets all three formats. 010 is A's 3rd video: once it has 3+ days of data (Nov 18) and B's 3rd does too, apply the decision rule.
- Log: 011-starbucks-short-size (Nov 16) = Setup B (default voice, speed 1.10, Empty Street Static -22 dB), Trick format, 30.5 s, no proof scene (009 and 010 both had one). Setup A so far: Story (006) + Trick (008) + Paradox (010); Setup B: Paradox (007) + Story (009) + Trick (011). Both setups now have all three formats. Next new video: Setup A. Decision rule can run once 011 has 3+ days of data (Nov 19).

## Video reviews
- 2026-11-13 (Hudson asked for a fix; full Studio pull): channel 4.0K views in 28 days, 1.7K engaged, 44 likes, 2 subs; 55% swiped away overall, 96% of views from the Shorts feed.
  - 001 Costco: 1.2K views, 34% stayed, 38% avg viewed. Cause: frame 1 had no headline, and the line 1 number had no context. Fix: instant headline (engine).
  - 002 Wolf: 882, 45% stayed, 45% avg. Cause: same opening problem.
  - 005 Popcorn: 264, 53% stayed, 35% avg viewed. Cause: 62 s is too long for our retention. Fix: 30-45 s cap.
  - 007 Airlines: 1.2K, 60% stayed, 48% avg (best). Works: brand + "more than its whole profit" paradox in line 1, male voice + beat, 45 s, 17:00 post.
  - 006 Cart: 9 views, 60% swiped. Cause: female narrator + a slow 65 s story; YouTube stopped testing it.
  - 008 Black Friday: 40 views, 80% swiped. Cause: female narrator + an opening Christmas-tree photo that didn't show a deal or a price tag.
  - Applied today: A/B winner = Setup B for all videos; 010 Spotify switched to B; new hooks for 009 ("McDonald's isn't really a burger company") and 010 ("300 streams to make one dollar"); all three scheduled videos re-rendered with the instant headline.
- 2026-11-13 evening fixes, scheduled: 009 McDonald's moved to Nov 14 17:00 (44 s, new hook), 010 Spotify Nov 15 12:30 (33 s, Setup B, new hook), 011 Starbucks Nov 16 17:00 (30 s, instant headline). Post-time test: 009 = 17:00, 010 = 12:30, 011 = 17:00; next new videos keep alternating. All three use media/*-v2.mp4 at commit de8b278.
