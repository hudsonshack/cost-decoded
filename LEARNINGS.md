# Learnings

Append weekly findings from analytics here.

## Metricool post count
- 2026-11: 5 of 20 used (001 Nov 7, 002 Nov 8, 005 Nov 9, 004 Nov 10, 003 moved to Nov 11)

## Production notes
- 2026-11-07: bigword text wider than ~5 characters spills off the frame during the punch-in; keep bigwords to 4-5 characters. Node labels over ~13 characters get cut at the side edges. Emoji with square silhouettes (📅 ↩️) render as blank squares in node icons; use shaped ones (⏳ 🔓 💰 🔍).

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
