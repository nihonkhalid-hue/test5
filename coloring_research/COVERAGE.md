# COVERAGE

_Collection 2026-10-25 UTC from a Google Cloud US egress (verified with ipinfo.io before every new site and every 30 minutes; never MA or the flagged IP)._

IP checks run: 38. Countries seen: {'US': 38}. Orgs: {'AS396982 Google LLC': 38}.

## Rows per source

| Marketplace | Master rows | Route(s) |
|---|---|---|
| gumroad | 735 | curl (tier A search JSON) (498); curl (tier A search JSON + tier B product page) (218); websearch (19) |
| etsy | 699 | third_party:rankhero (658); websearch (34); third_party:rankhero+websearch (3); third_party:findniche+websearch (2); third_party:findniche (2) |
| teacherspayteachers | 511 | curl (511) |
| amazon | 139 | third_party:asinsight (139) |
| itch.io | 104 | curl (104) |
| payhip | 19 | websearch (19) |
| creativemarket | 3 | websearch (3) |
| monsterone | 1 | websearch (1) |
| templatemonster | 1 | websearch (1) |
| baldhamster | 1 | websearch (1) |
| tiktokshop | 1 | websearch (1) |

## Raw collection counts

- gumroad tier A rows (all query×sort hits, before dedupe): 1525
- gumroad tier B product pages: 218
- RankHero Etsy keyword pages: 76
- RankHero Etsy listing cards (before dedupe): 684
- FindNiche Etsy product pages (coloring): 4
- FindNiche ID/date anchors: 35
- Kupkaike niche pages: 5
- ASINsight Amazon rows: 139
- TpT rows (before dedupe): 576
- itch.io rows: 104
- WebSearch result rows: 85
- Reddit RSS posts (demand signals): 56
- Google Trends series: 6

## Targets vs achieved

| Source | Target | Achieved | Status |
|---|---|---|---|
| Etsy tier A | 800+ | 699 unique listings | Etsy direct BLOCKED (DataDome); rows come from RankHero, FindNiche and WebSearch |
| Etsy tier B | 150+ | 4 with sales/reviews/date (FindNiche) | Listing pages unreachable; listing date, shop sales and review dates not available |
| Gumroad | 200+ | 735 | Done (curl, tier A + tier B) |
| Amazon/KDP | 300+ | 139 (ASINsight) | Amazon BLOCKED (CAPTCHA on the first slow retry); no BSR, publisher, page count or size |
| eBay sold | 150+ | 0 | BLOCKED (403); WebSearch found no sold data |
| Payhip | – | 19 (WebSearch) | Direct BLOCKED (403 CAPTCHA) |
| Others (4+) | 4 | Teachers Pay Teachers (511), itch.io (104), plus Creative Market (3) and TikTok Shop (1) via WebSearch | Creative Fabrica, Ko-fi and Creative Market direct: BLOCKED (Cloudflare). Barnes & Noble: bot-filter 404. Walmart, Lulu, Redbubble: not attempted. |
| Reddit | 3+ subs | 56 posts, r/adultcoloring only | 429 after 2 requests (30 s gap); one resume at 90–120 s got 1 more request, then 429 again; stopped for good |
| Google Trends | 21 terms × 2 geos | 6 series (worldwide only) | pytrends: 429 after 5 series. An early resume about 6 minutes after the 429 (a timing mistake on my side) fetched 1 more series (kawaii coloring) before I stopped it. A proper resume after a 35-minute cooldown at 120–150 s spacing got a 429 on its first request, so it was stopped for good. Glimpse and Exploding Topics have no public pages for these terms (404). US series and the other terms are covered only by RankHero's Etsy monthly series in seasonality.csv. |


**Why these four 'others':** Teachers Pay Teachers (ratings and review counts for the kids/classroom niche; reachable by curl), itch.io (indie anime-style creators, reachable), Creative Market and TikTok Shop (appeared repeatedly in WebSearch with bold-and-easy/cozy products and a 'sold' count). Walmart, Lulu and Redbubble were skipped: they are print-on-demand or retail and less informative for a digital seller than the sources above.

**Third-party Etsy route:** eRank, EverBee, Alura, Marmalead, InsightFactory and Sale Samurai public pages gave no niche-level coloring data (the tools are behind logins). RankHero (keyword volume, listing counts, monthly series and top-12 listings with favorites and views), FindNiche (per-listing sales, reviews and release date) and Kupkaike (live Etsy listing counts) were used instead.


## Blocked / failed URLs

| Time (UTC) | Site | URL | HTTP | Note |
|---|---|---|---|---|
| 2026-10-25T15:38:32Z | reddit.com | https://www.reddit.com/r/adultcoloring/search.rss?q=cozy&restrict_sr=on&sort=top&t=year | 429 | BLOCKED  |
| 2026-10-25T15:38:36Z | amazon.com | https://www.amazon.com/gp/bestsellers/books/11357541011 | 200 | BLOCKED captcha page (validateCaptcha) - Amazon stopped for good |
| 2026-10-25T15:45:42Z | trends.google.com | pytrends kawaii coloring  | ERR | BLOCKED The request failed: Google returned a response with code 429 |
| 2026-10-25T15:48:59Z | reddit.com | https://www.reddit.com/r/adultcoloring/search.rss?q=bold%20easy&restrict_sr=on&sort=top&t… | 429 | BLOCKED  |
| 2026-10-25T15:49:19Z | creativemarket.com | https://creativemarket.com/search?q=coloring%20pages | 403 | BLOCKED Just a moment... |
| 2026-10-25T15:51:47Z | rankhero.com | https://www.rankhero.com/keywords/cozy-cottage-coloring | 404 | BLOCKED challenge-platform |
| 2026-10-25T16:21:26Z | trends.google.com | pytrends anime coloring  | ERR | BLOCKED The request failed: Google returned a response with code 429 |
| 2026-10-25T15:13Z | etsy.com, gumroad.com | WebFetch (first pilot) | – | WebFetch DNS failure (ENOTFOUND) for every host; WebFetch unusable in this container |
| 2026-10-25T15:29Z | etsy.com | https://www.etsy.com/search?q=kawaii+coloring+pages | 403 | DataDome CAPTCHA (pilot 2). Not retried. |
| 2026-10-25T15:30Z | ebay.com, payhip.com, creativefabrica.com, ko-fi.com | pilot probes | 403 | eBay error page, Payhip CAPTCHA, Cloudflare challenges |

Total logged requests: 691 (gumroad.com 428, rankhero.com 102, teacherspayteachers.com 45, findniche.com 42, asinsight.com 31, kupkaike.com 18, trends.google.com 8, reddit.com 5, itch.io 4, amazon.com 2, meetglimpse.com 2, explodingtopics.com 2, creativemarket.com 1, barnesandnoble.com 1).

## Fields missing (share of master rows where the field is blank or NOT SHOWN)

| Marketplace | price | rating | review_count | sales_shown | bestseller_badge | favorites | listing_date | listing_date_est | bsr | page_count | seller |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gumroad | 1% | 33% | 3% | 97% | 100% | 100% | 100% | 100% | 100% | 91% | 3% |
| etsy | 4% | 100% | 99% | 100% | 99% | 5% | 99% | 0% | 100% | 84% | 5% |
| teacherspayteachers | 2% | 36% | 36% | 100% | 100% | 100% | 100% | 100% | 100% | 93% | 100% |
| amazon | 8% | 8% | 8% | 100% | 100% | 100% | 100% | 100% | 100% | 86% | 100% |
| itch.io | 35% | 100% | 84% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 0% |
| payhip | 74% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| creativemarket | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| monsterone | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| templatemonster | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| baldhamster | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| tiktokshop | 100% | 100% | 100% | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

Not collectable at all: Etsy Star Seller, Ad flag, shop total sales, shop open year and review dates (listing pages blocked); Amazon BSR, publisher, independently-published flag, page count and size (blocked); eBay sold prices (blocked).

## Verification (random 5% re-fetch)

Sampled 111 rows (5% of 2214, seed 20261025). Re-fetched and compared: 108. **Mismatch rate: 1/108 = 0.9%.** Not verifiable: NOT VERIFIABLE (websearch/blocked source) (3).

| Source | Field | Old | New | Title |
|---|---|---|---|---|
| teacherspayteachers | price|reviews | 0.0/20 | /20 | Cute Animals Coloring Pages , Free Gift For You ,… |

The one remaining mismatch is a free TpT item: the re-fetched card shows no '$x Original Price' string, so the verifier read the price as missing. It is most likely a verifier limitation, not a data error. The first two verifier runs reported higher mismatch rates because of bugs in the verifier itself (it matched the ASIN inside JSON-LD, checked page 1 for page-2 TpT rows, and failed on HTML-entity and ISO-code prices). After those fixes, each check was re-run against the same re-fetched pages. Verification compares price + ratings for Gumroad, price + favorites for Etsy/RankHero, price + reviews for TpT, and monthly sales for ASINsight. See `verification.csv`.

## Every estimate and its formula

- `listing_date_est` / `listing_age_days_est` (Etsy): piecewise-linear interpolation of listing ID → date between 35 FindNiche anchors (listing ID with a published 'Released' date): 733736582→2019-10-26, 1004634776→2021-05-13, 1070448687→2021-08-19, 1413455244→2023-02-28, 1483679759→2023-05-16, 1581100221→2023-10-04, 1679237029→2024-02-16, 1864690497→2025-01-26, 4302574537→2025-05-08, 4309041358→2025-05-22, 4320632782→2025-06-14, 4329798999→2025-07-03, 4350596583→2025-08-12, 4354476237→2025-08-18, 4364973626→2025-09-06, 4376958217→2025-09-27, 4388535117→2025-10-17, 4440897309→2026-01-14, 4448566283→2026-01-28, 4455478402→2026-02-10, 4466558752→2026-03-04, 4469234956→2026-03-09, 4480199311→2026-03-30, 4481877480→2026-04-02, 4482369277→2026-04-03, 4485709997→2026-04-09, 4492750007→2026-04-22, 4494853441→2026-04-26, 4498990703→2026-05-04, 4506520095→2026-05-17, 4509210419→2026-05-21, 4510687031→2026-05-24, 4515069995→2026-06-02, 4516292402→2026-06-04, 4533075438→2026-07-05. IDs above the last anchor are extrapolated on the last segment. IDs below the first anchor take the first anchor date, so their age is a LOWER BOUND; these are flagged in `fetch_route` and excluded from velocity rankings.
- `velocity_value` (Etsy) = favorites ÷ max(listing_age_days(_est) ÷ 30.4, 1). Where a review count exists (FindNiche), it is reviews ÷ months instead (`velocity_metric` says which).
- `sales_est_thirdparty`, `monthly_sales_est_thirdparty` (Etsy): FindNiche's own tracked estimates, copied as published.
- `monthly_sales_est_thirdparty` (Amazon): ASINsight's 'Units Sold/mo' estimate for the report month shown in `notes`. `sales_per_day_est = monthly ÷ 30.4`. **The BSR-to-sales table method was not possible because Amazon blocked every product and list page, so no BSR was collected.**
- `price_usd_est`: price × fixed approximate FX (EUR 1.08, GBP 1.27, CAD 0.73, AUD 0.66, NOK 0.093).
- `niche`, `style`, `audience`, `anime_japan_kawaii_fit`, `women_lean`, `season`, `ip_risk`: rule-based keyword classification of titles (scripts/classify.py). These are labels, not measurements.
- Opportunity score: formula in REPORT.md. Percentile-based, so it is relative between niches, not absolute.
- Google Trends `yoy_pct` = mean(last 52 weeks) ÷ mean(previous 52) − 1; `change_5y_pct` = mean(last 52) ÷ mean(first 52) − 1; `list_by` = 1st of peak month − 6 weeks.
- RankHero monthly Etsy search volumes are bucketed (e.g. 673k / 823k / 1M), so Etsy seasonality is coarse.

## Data accuracy notes

- Marketplace rows via curl were parsed from the raw HTML/JSON (verbatim values). Raw pages are kept in the session scratchpad; parsed raw CSVs are committed under `raw/`.
- WebSearch rows (`fetch_route=websearch`): titles are search-result titles. Prices in `notes` marked 'summary' come from the search tool's own summary, not the page, and should be treated as unverified.
- Gumroad `sales_shown` is 'NOT SHOWN' where the creator hides the count (most do).
