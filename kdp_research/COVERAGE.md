# COVERAGE — KDP market research

_Collection 2026-11-05 UTC from a cloud container. IP checks: 78 (countries {'US': 78}; orgs {'AS396982 Google LLC': 78}). Never MA, never a Moroccan ISP, never 197.146.42.124._

## Pilot (one request per source, 2026-11-05 02:40 UTC)

| Group | Site | URL | Result | Bytes |
|---|---|---|---|---|
| A amazon direct | amazon.com | https://www.amazon.com/gp/bestsellers/books/11357541011 | 200 | 704218 |
| A amazon direct | amazon.co.uk | https://www.amazon.co.uk/gp/bestsellers/books/ | 200 | 493586 |
| A amazon direct | amazon.de | https://www.amazon.de/gp/bestsellers/books/ | BLOCKED | 3817 |
| A amazon direct | amazon.ca | https://www.amazon.ca/gp/bestsellers/books/ | BLOCKED | 3781 |
| B asinsight | asinsight.com | https://www.asinsight.com/report/US/word-search-books-for-adults | 404 | 143329 |
| C enrichment | openlibrary.org | https://openlibrary.org/search.json?q=word+search+large+print&limit=5 | 200 | 1513 |
| C enrichment | googleapis.com | https://www.googleapis.com/books/v1/volumes?q=intitle:gratitude+journal | BLOCKED | 1306 |
| D third party | kindlepreneur.com | https://kindlepreneur.com/amazon-kdp-sales-rank-calculator/ | 200 | 213834 |
| D third party | tckpublishing.com | https://www.tckpublishing.com/amazon-book-sales-calculator/ | 200 | 268860 |
| D third party | camelcamelcamel.com | https://camelcamelcamel.com/product/B09VCYS41G | BLOCKED | 5751 |
| D third party | keepa.com | https://keepa.com/ | 200 | 9619 |
| D third party | goodreads.com | https://www.goodreads.com/list/show/1.Best_Books_Ever | 200 | 786188 |
| D third party | bookbub.com | https://www.bookbub.com/blog | BLOCKED | 5684 |
| D third party | bookbolt.io | https://bookbolt.io/ | BLOCKED | 4547 |
| D third party | kdspy.com | https://www.kdspy.com/ | 200 | 244491 |
| E demand | reddit.com | https://www.reddit.com/r/selfpublish/search.rss?q=low+content&restrict_sr=on&sort=top&t=year | 200 | 88268 |
| F comparison | gumroad.com | https://gumroad.com/products/search?query=journal&from=0 | 200 | 10354 |
| F comparison | teacherspayteachers.com | https://www.teacherspayteachers.com/browse?search=handwriting%20practice | 200 | 1090900 |
| F comparison | rankhero.com | https://www.rankhero.com/keywords/printable-planner | 200 | 264229 |
| royalty constants | kdp.amazon.com | https://kdp.amazon.com/en_US/help/topic/G201834340 | 200 | 212015 |

Pilot notes: amazon.com and amazon.co.uk returned real pages on the first request; amazon.de and amazon.ca returned the small CAPTCHA page; Google Books API returned 429 `RESOURCE_EXHAUSTED` with `quota_limit_value: 0` for the shared keyless project (not retried); camelcamelcamel, BookBub and Book Bolt returned Cloudflare/403; the ASINsight 404 was a non-existent slug, not a block.

## Rows per source (master.csv, one row per product per marketplace)

| Marketplace | Master rows | Route(s) |
|---|---|---|
| amazon.com | 12953 | third_party:profitable.app (10033); curl (313); third_party:asinsight (2607) |
| gumroad | 918 | curl (918) |
| teacherspayteachers | 918 | curl (918) |
| etsy | 574 | third_party:rankhero (574) |
| goodreads | 472 | curl (472) |
| amazon.de | 50 | curl (50) |
| amazon.co.uk | 50 | curl (50) |

**Total master rows: 15935**

## Raw collection counts (before de-duplication; every collected row kept in raw/)

- raw/amazon_asinsight.csv: 11896 rows
- raw/amazon_direct_lists.csv: 750 rows
- raw/asinsight_misses.csv: 67 rows
- raw/demand_reddit_rss.csv: 110 rows
- raw/enrich_openlibrary.csv: 389 rows
- raw/etsy_rankhero_keywords.csv: 66 rows
- raw/etsy_rankhero_keywords_parsed.csv: 66 rows
- raw/etsy_rankhero_listing_links.csv: 576 rows
- raw/etsy_rankhero_listings.csv: 576 rows
- raw/fetch_log.csv: 3495 rows
- raw/goodreads_shelves.csv: 520 rows
- raw/gumroad.csv: 1296 rows
- raw/ip_checks.csv: 78 rows
- raw/pilot.csv: 20 rows
- raw/profitable_books.csv: 17542 rows
- raw/profitable_category_views.csv: 851 rows
- raw/teacherspayteachers.csv: 960 rows
- raw/google_trends/: 40 series (activity_book_US.csv, activity_book_WW.csv, bold_and_easy_coloring_US.csv, bold_and_easy_coloring_WW.csv, coloring_book_US.csv, coloring_book_WW.csv, cookbook_US.csv, cookbook_WW.csv, cozy_mystery_US.csv, cozy_mystery_WW.csv, dark_romance_US.csv, dark_romance_WW.csv, gratitude_journal_US.csv, gratitude_journal_WW.csv, handwriting_practice_US.csv, handwriting_practice_WW.csv, how_to_draw_anime_US.csv, how_to_draw_anime_WW.csv, journal_US.csv, journal_WW.csv, kawaii_US.csv, kawaii_WW.csv, low_content_books_US.csv, low_content_books_WW.csv, password_book_US.csv, password_book_WW.csv, planner_US.csv, planner_WW.csv, puzzle_book_US.csv, puzzle_book_WW.csv, romantasy_US.csv, romantasy_WW.csv, self_help_books_US.csv, self_help_books_WW.csv, sketchbook_US.csv, sketchbook_WW.csv, sudoku_book_US.csv, sudoku_book_WW.csv, word_search_US.csv, word_search_WW.csv)

## Requests per site

asinsight.com 1485, profitable.app 1215, openlibrary.org 390, gumroad.com 181, rankhero.com 68, teacherspayteachers.com 59, trends.google.com 40, amazon.com 15, goodreads.com 11, reddit.com 8, amazon.de 5, kdp.amazon.com 4, amazon.co.uk 3, amazon.ca 2, tckpublishing.com 2, googleapis.com 1, kindlepreneur.com 1, camelcamelcamel.com 1, keepa.com 1, bookbub.com 1, bookbolt.io 1, kdspy.com 1. Total logged requests: 3495.

## Blocked / failed URLs (every BLOCKED or HTTP>=400 line of fetch_log.csv)

| Time (UTC) | Site | URL | HTTP | Note |
|---|---|---|---|---|
| 2026-11-05T02:40:21Z | amazon.de | https://www.amazon.de/gp/bestsellers/books/ | 200 | BLOCKED  |
| 2026-11-05T02:40:22Z | amazon.ca | https://www.amazon.ca/gp/bestsellers/books/ | 200 | BLOCKED  |
| 2026-11-05T02:40:24Z | googleapis.com | https://www.googleapis.com/books/v1/volumes?q=intitle:gratitude+journal | 429 | BLOCKED  |
| 2026-11-05T02:40:26Z | camelcamelcamel.com | https://camelcamelcamel.com/product/B09VCYS41G | 403 | BLOCKED Just a moment... |
| 2026-11-05T02:40:27Z | bookbub.com | https://www.bookbub.com/blog | 403 | BLOCKED Just a moment... |
| 2026-11-05T02:40:27Z | bookbolt.io | https://bookbolt.io/ | 403 | BLOCKED  |
| 2026-11-05T02:41:48Z | amazon.co.uk | https://www.amazon.co.uk/gp/bestsellers/books | 200 | BLOCKED  |
| 2026-11-05T02:42:17Z | amazon.com | https://www.amazon.com/gp/bestsellers/digital-text/154606011 | 200 | BLOCKED  |
| 2026-11-05T02:49:05Z | reddit.com | https://www.reddit.com/r/selfpublish/search.rss?q=puzzle%20book&restrict_sr=on&sort=top&t=year | 429 | BLOCKED  |
| 2026-11-05T03:00:35Z | rankhero.com | https://www.rankhero.com/keywords/puzzle-book-for-adults | 404 | BLOCKED challenge-platform |
| 2026-11-05T03:16:04Z | amazon.co.uk | https://www.amazon.co.uk/gp/bestsellers/books | 200 | BLOCKED  |
| 2026-11-05T03:16:04Z | amazon.ca | https://www.amazon.ca/gp/bestsellers/books | 200 | BLOCKED  |
| 2026-11-05T03:19:05Z | amazon.de | https://www.amazon.de/gp/most-wished-for/books/11357541011 | 200 | BLOCKED  |
| 2026-11-05T03:27:38Z | amazon.com | https://www.amazon.com/gp/bestsellers/books/8975347011 | 200 | BLOCKED  |
| 2026-11-05T03:44:46Z | reddit.com | https://www.reddit.com/r/KDP/search.rss?q=niche&restrict_sr=on&sort=top&t=year | 429 | BLOCKED  |

Not listed above: 70 ASINsight 404s (sitemap slugs with no live report) and 145 Open Library 404s (ISBN not in Open Library). These are missing pages, not blocks.

## Fields missing per source (share of master rows NOT SHOWN / blank)

| Marketplace / route | n | price | rating | review_count | bsr | publisher | publication_date | page_count | trim_size | monthly_sales_est_bsr | monthly_sales_est_thirdparty |
|---|---|---|---|---|---|---|---|---|---|---|---|
| amazon.com / third_party:profitable.app | 10033 | 0% | 0% | 0% | 0% | 17% | 0% | 3% | 100% | 0% | 100% |
| amazon.com / third_party:asinsight | 2607 | 3% | 3% | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 0% |
| gumroad / curl | 918 | 0% | 0% | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| teacherspayteachers / curl | 918 | 0% | 13% | 13% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| etsy / third_party:rankhero | 574 | 0% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| goodreads / curl | 472 | 100% | 0% | 0% | 100% | 100% | 1% | 100% | 100% | 100% | 100% |
| amazon.com / curl | 313 | 46% | 49% | 49% | 100% | 61% | 61% | 73% | 100% | 100% | 100% |
| amazon.de / curl | 50 | 42% | 46% | 46% | 100% | 82% | 82% | 86% | 100% | 100% | 100% |
| amazon.co.uk / curl | 50 | 40% | 46% | 46% | 100% | 56% | 60% | 76% | 100% | 100% | 100% |

## Verification (random 5% of master rows, seed 42)

Sample: 796 rows. Step 1 (re-parse the saved page, tests the pipeline): {'match': 693, 'row': 31, 'not': 72}; mismatch rate 0.0% of 693 checkable rows.
Step 2 (live re-fetch now, tests real drift): {'match': 693, 'row': 31, 'not': 72}; value drift 0.0% of 693 rows still on the page; rows that left the page = rank drift.
Per-row results: verification.csv.

## Every estimate and its formula

| Column | Formula / source |
|---|---|
| `monthly_sales_est_bsr` | TCK Publishing BSR model, verbatim from tckpublishing.com/wp-content/plugins/tck-amazon-sales-calculator/script.js (v7.1.4): monthly = round(10^(e + a·log10(BSR) + b·log10(BSR)²) × 15 × 1.08). Print books (BSR in "Books"): a = -0.33483877, b = -0.06198923, e = 3.69500221. Kindle (BSR in "Kindle Store"): a = -0.34034503, b = -0.07791303, e = 3.98993694. Example: BSR 1,000 print ≈ 2,198/mo; BSR 100,000 print ≈ 48/mo; BSR 1,000 Kindle ≈ 3,001/mo. Applied only to the overall BSR (`bsr`, profitable.app `bsrTop`), never to sub-category ranks. |
| `sales_per_day_est` | `monthly_sales_est_bsr` ÷ 30 (steady average; TCK's own "1 day sales" = monthly ÷ 15 means sales needed to reach the rank briefly, not used). |
| `monthly_sales_est_thirdparty` | ASINsight "Units Sold/mo" verbatim (their estimate, report month January 2026). |
| `monthly_revenue_est_thirdparty` | profitable.app `monthlyRevenue` verbatim (their estimate; their FAQ: royalties estimated from BSR, price and format). Not used in our scores. |
| `royalty_per_sale_est` | Paperback (Amazon.com, kdp.amazon.com help G201834330 + G201834340, fetched 2026-11-05): rate × list price − printing cost; rate = 60% if list ≥ $9.99 else 50%. Printing cost black ink: 24–110 pages $2.30 (regular trim) / $2.84 (large trim); 110–828 pages $1.00 + $0.012/page (regular) / $1.00 + $0.017/page (large). Premium color (picture books): 24–40 pages $3.60/$4.20; 42–828 pages $1.00 + $0.065/page / $1.00 + $0.08/page. Hardcover (GHT976ZKSKUXBB6H): 75–108 pages $6.80/$7.49; 110–550 pages $5.65 + $0.012/page / $5.65 + $0.017/page; same 50/60% rule assumed. Kindle: 70% of list for $2.99–$9.99, otherwise 35% (download delivery fee ignored). Large trim (>6.12 in wide or >9 in tall) assumed for coloring, puzzle, activity-kids, workbook-education, picture-book and art-instruction, regular trim otherwise, unless dimensions were known. Missing page counts use a per-segment default stated in `royalty_assumptions`. Spiral-bound priced as paperback (KDP has no spiral option). Board books/audiobooks: not computed. |
| `monthly_royalty_est` | `royalty_per_sale_est` × (`monthly_sales_est_bsr`, else `monthly_sales_est_thirdparty`). |
| `price_usd_est` | Listed price × fixed FX: EUR 1.08, GBP 1.27, CAD 0.72, AUD 0.65, INR 0.012, JPY 0.0066 (USD rows unchanged). |
| `listing_age_days` | fetched_at date − publication date (exact day-level date from profitable.app or Open Library). Negative = pre-order. |
| `listing_age_days_est` | Same, when only a year or month is known (Open Library "2013", Goodreads "published 2023" → July 1 of that year). |
| `velocity_value` | review_count ÷ max(age_days ÷ 30.44, 1) = reviews (or Goodreads ratings) per month since publication; books younger than 14 days excluded from velocity rankings. |
| `independently_published` | "yes" = publisher text contains "Independently published"; "likely (third-party likelyKdp flag)" = profitable.app's flag; otherwise "no". |
| Segment, niche, audience, interior, Japan fit, women lean, season, IP risk | Rule-based regexes in scripts/classify.py on title (+ listing category / BSR placements as fallback). IP risk = a trademarked franchise/brand term in the title and the publisher is not a known licensed publisher. |
| Opportunity score | 100 × demand × (1 − 0.5 × P(median reviews)) × (0.6 + 0.4 × indie share) × (1 − 0.3 × top-3 sales share) × (0.85 + 0.3 × newcomer rate) × trend factor; demand = 0.6 × P(median est. monthly sales) + 0.4 × P(median velocity); P = percentile among niches with ≥5 Amazon books; trend factor 1.1 if Google Trends US 52-week y/y > +10%, 0.9 if < −10%, else 1.0. |
| Newcomer test | Books < 365 days old with ≥ 50 reviews or ≥ 300 est. sales/month. |
| Dominance | Share of the niche's summed est. monthly sales held by the top 3 publishers (traditional) or authors (indie). |
| Seasonality index | Month mean ÷ annual mean × 100 (Google Trends 5-year weekly; RankHero Etsy monthly searches Oct 2025–Sep 2026). Publish-by = mid-month two months before the peak. |

## Targets vs achieved

| Source | Status |
|---|---|
| A. Amazon direct | amazon.com: pilot page OK, root page OK, CAPTCHA on 3rd request (02:42); one resume after the cooldown at 45–75 s pacing got 10 more Best Sellers pages, then CAPTCHA again → stopped for good. amazon.co.uk: pilot OK, CAPTCHA on 2nd request; resume blocked on its first request → stopped. amazon.de: pilot CAPTCHA; resume got 3 pages, then CAPTCHA → stopped. amazon.ca: pilot CAPTCHA; resume blocked on first request → stopped. New Releases / Movers & Shakers / Most Wished For and product pages (publisher, page count, dimensions, BSR) were never reached on amazon.com; this is why trim size is mostly NOT SHOWN. |
| B. ASINsight | Slugs taken from asinsight's own sitemap (597,086 report URLs), filtered to book terms, priority-ordered; ~1,340 reports fetched until the queue reached non-book "manga" clothing keywords (stopped by me, 05:47). Report month: January 2026. Book ISBN rows are rare (the keyword top-10s are mostly supplies). |
| C. Enrichment | Open Library ISBN lookups for Amazon-direct and ASINsight ISBNs (see raw/enrich_openlibrary.csv). Google Books API: 429 RESOURCE_EXHAUSTED with quota 0 for keyless calls on the first request, not retried. profitable.app already supplied publication date and print length for its books. |
| D. Third-party KDP tools | profitable.app (main source, 862 requests; stopped at 05:28 by a connection reset, not a block, after it had reached the end of my time budget). TCK Publishing calculator script (BSR model used). Kindlepreneur calculator page reachable but the model is client-side and not published as a table. KDSPY / Keepa homepages reachable but no public data without accounts. camelcamelcamel, BookBub, Book Bolt: 403/Cloudflare. BookBeam, ZonGuru, Helium 10, Jungle Scout blogs: not attempted (no product-level public data expected); Goodreads shelves used. |
| E. Demand / trends | Google Trends: all 20 terms × worldwide + US (40 series, 5-year weekly), no 429. Reddit: 2 feeds, 429; one resume 50 min later got 3 more feeds then 429 → stopped for good (r/kdp_lowcontent and r/coloringbooks never reached). WebSearch summaries recorded in REPORT caveats and raw/demand_websearch_signals.tsv. |
| F. Comparison marketplaces | Gumroad search JSON (36 queries × 3 sorts), Teachers Pay Teachers (20 queries × 2 pages), Etsy via RankHero (66 keyword pages with monthly series + top listings). |

### Verifier bugs found and fixed (separated from real drift)

First verifier run (stopped by a missing-file crash after 200 rows): 15 'MISMATCH' rows, all verifier bugs, none real data errors:
- 11 ASINsight rows: master keeps the highest Units Sold/mo across all keywords a product appeared under (by design, noted per row), but the verifier compared it with the first keyword's page. Fixed: the verifier now compares against the raw row for that page.
- 4 Teachers Pay Teachers rows: the verifier looked for the product URL in the first place it appeared in the HTML (a JSON blob) instead of the product card. Fixed: it now searches inside the matching ProductRow card.
- Gumroad rows were looked up in the from=0 page even when collected from a later page. Fixed: the verifier uses each raw row's own source_url.
- One ASINsight re-fetch failed with a network error (no file written), which crashed the run. Fixed: such rows are recorded as 'fetch failed' instead.

### Verification result notes

- Live drift is 0% for profitable.app rows because that dataset is a fixed snapshot (Updated Oct 9, 2026); a live re-fetch on the same day returns the same values. Amazon itself could not be re-fetched (blocked), so true Amazon drift since Oct 9 is unknown.
- 'row' (31 rows): Teachers Pay Teachers rows collected from page 2; the verifier only re-checks page 1, so they could not be compared.
- The rankhero.com line in the blocked table is a false positive: the page was a real "404 | Page not found" that contains Cloudflare's beacon script. Netlib was fixed to not flag such pages, and the one allowed resume after a 33-minute cooldown completed without incident.
- 'not' (72 rows): sources the verifier cannot re-fetch: Amazon direct (blocked), Etsy (via RankHero listing cards, not re-parsed) and Goodreads.
