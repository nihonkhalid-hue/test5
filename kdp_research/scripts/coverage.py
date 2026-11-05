"""Writes COVERAGE.md from raw files, fetch log, ip checks, verification."""
import csv, collections, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from netlib import REPO
csv.field_size_limit(10 ** 9)
R = os.path.join(REPO, "raw"); NS = "NOT SHOWN"


def rd(p):
    p = os.path.join(REPO, p)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


M = rd("master.csv"); FL = rd("raw/fetch_log.csv"); IP = rd("raw/ip_checks.csv"); PI = rd("raw/pilot.csv"); V = rd("verification.csv")
L = []
L.append("# COVERAGE — KDP market research\n")
L.append(f"_Collection 2026-11-05 UTC from a cloud container. IP checks: {len(IP)} (countries {dict(collections.Counter(r['country'] for r in IP))}; orgs {dict(collections.Counter(r['org'] for r in IP))}). Never MA, never a Moroccan ISP, never 197.146.42.124._\n")
L.append("## Pilot (one request per source, 2026-11-05 02:40 UTC)\n\n| Group | Site | URL | Result | Bytes |\n|---|---|---|---|---|")
for r in PI: L.append(f"| {r['group']} | {r['site']} | {r['url']} | {r['http_or_block']} | {r['bytes']} |")
L.append("\nPilot notes: amazon.com and amazon.co.uk returned real pages on the first request; amazon.de and amazon.ca returned the small CAPTCHA page; Google Books API returned 429 `RESOURCE_EXHAUSTED` with `quota_limit_value: 0` for the shared keyless project (not retried); camelcamelcamel, BookBub and Book Bolt returned Cloudflare/403; the ASINsight 404 was a non-existent slug, not a block.\n")
L.append("## Rows per source (master.csv, one row per product per marketplace)\n\n| Marketplace | Master rows | Route(s) |\n|---|---|---|")
by = collections.defaultdict(collections.Counter)
for r in M: by[r["marketplace"]][r["fetch_route"]] += 1
for mk, c in sorted(by.items(), key=lambda x: -sum(x[1].values())):
    L.append(f"| {mk} | {sum(c.values())} | " + "; ".join(f"{k} ({v})" for k, v in c.items()) + " |")
L.append(f"\n**Total master rows: {len(M)}**\n")
L.append("## Raw collection counts (before de-duplication; every collected row kept in raw/)\n")
for f in sorted(os.listdir(R)):
    if f.endswith(".csv"):
        n = len(rd("raw/" + f)); L.append(f"- raw/{f}: {n} rows")
gt = os.listdir(os.path.join(R, "google_trends")) if os.path.exists(os.path.join(R, "google_trends")) else []
L.append(f"- raw/google_trends/: {len(gt)} series ({', '.join(sorted(gt))})")
L.append("\n## Requests per site\n")
c = collections.Counter(r["site"] for r in FL)
L.append(", ".join(f"{k} {v}" for k, v in c.most_common()) + f". Total logged requests: {len(FL)}.\n")
L.append("## Blocked / failed URLs (every BLOCKED or HTTP>=400 line of fetch_log.csv)\n\n| Time (UTC) | Site | URL | HTTP | Note |\n|---|---|---|---|---|")
nb = 0
for r in FL:
    if "BLOCKED" in r["note"] or (r["http"].isdigit() and int(r["http"]) >= 400 and r["site"] not in ("asinsight.com", "openlibrary.org")):
        L.append(f"| {r['fetched_at']} | {r['site']} | {r['url'][:110]} | {r['http']} | {r['note'][:70]} |"); nb += 1
a404 = sum(1 for r in FL if r["site"] == "asinsight.com" and r["http"] == "404")
o404 = sum(1 for r in FL if r["site"] == "openlibrary.org" and r["http"] == "404")
L.append(f"\nNot listed above: {a404} ASINsight 404s (sitemap slugs with no live report) and {o404} Open Library 404s (ISBN not in Open Library). These are missing pages, not blocks.\n")
L.append("## Fields missing per source (share of master rows NOT SHOWN / blank)\n")
F = ["price", "rating", "review_count", "bsr", "publisher", "publication_date", "page_count", "trim_size", "monthly_sales_est_bsr", "monthly_sales_est_thirdparty"]
L.append("| Marketplace / route | n | " + " | ".join(F) + " |\n|---|---|" + "---|" * len(F))
g = collections.defaultdict(list)
for r in M: g[(r["marketplace"], r["fetch_route"])].append(r)
for (mk, rt), rs in sorted(g.items(), key=lambda x: -len(x[1])):
    L.append(f"| {mk} / {rt} | {len(rs)} | " + " | ".join(f"{round(100*sum(1 for r in rs if r[k] in (NS, '', 'None'))/len(rs))}%" for k in F) + " |")
L.append("\n## Verification (random 5% of master rows, seed 42)\n")
if V:
    c1 = collections.Counter(x["reparse_status"].split(" ")[0] for x in V); c2 = collections.Counter(x["live_status"].split(" ")[0] for x in V)
    rp = [x for x in V if x["reparse_status"] in ("match",) or x["reparse_status"].startswith("MISMATCH")]
    lv = [x for x in V if x["live_status"] == "match" or x["live_status"].startswith("DRIFT")]
    L.append(f"Sample: {len(V)} rows. Step 1 (re-parse the saved page, tests the pipeline): {dict(c1)}; mismatch rate {round(100*sum(1 for x in rp if x['reparse_status'].startswith('MISMATCH'))/max(1,len(rp)),1)}% of {len(rp)} checkable rows.")
    L.append(f"Step 2 (live re-fetch now, tests real drift): {dict(c2)}; value drift {round(100*sum(1 for x in lv if x['live_status'].startswith('DRIFT'))/max(1,len(lv)),1)}% of {len(lv)} rows still on the page; rows that left the page = rank drift.")
    L.append("Per-row results: verification.csv.\n")
open(os.path.join(REPO, "COVERAGE_auto.md"), "w").write("\n".join(L))
print("coverage written", nb, "blocked lines")

EST = r"""
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
"""
open(os.path.join(REPO, "COVERAGE_auto.md"), "a").write(EST)
