"""Render REPORT.md and COVERAGE.md from analysis outputs + logs."""
import csv, json, os, re, sys
from collections import Counter, defaultdict

BASE = "/tmp/claude-0/-home-user-test5/f1949923-2992-520a-80c3-c501569412ac/scratchpad"
RAW = os.path.join(BASE, "raw")
OUT = sys.argv[1]
A = json.load(open(os.path.join(OUT, "_analysis.json")))
rows = list(csv.DictReader(open(os.path.join(OUT, "master.csv"), encoding="utf-8")))
anchors = json.load(open(os.path.join(OUT, "_anchors.json")))["anchors"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def fmt(v, nd=2):
    if v in (None, "", "None"): return "–"
    try:
        x = float(v)
        return f"{x:,.0f}" if abs(x) >= 100 else f"{x:,.{nd}f}".rstrip("0").rstrip(".")
    except Exception:
        return str(v)


def t(s, n=70):
    s = (s or "").replace("|", "/").replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


EXCL = {"general-coloring", "supplies-not-a-book"}
niches = [n for n in A["niches"] if n["niche"] not in EXCL]
ranked = [n for n in niches if n["rows_collected"] >= 15]
thin = [n for n in niches if n["rows_collected"] < 15]

L = []
L.append("# Coloring pages & books: niche, velocity and seasonality report\n")
L.append("_Data collected 2026-10-25 (UTC). Read COVERAGE.md first: Etsy, Amazon, eBay, Payhip, Creative Fabrica and Ko-fi blocked direct access, so several signals come from third-party trackers and are labelled as such._\n")
cnt = Counter(r["marketplace"] for r in rows)
L.append(f"**Master table:** {len(rows):,} product rows across {len(cnt)} sources (" + ", ".join(f"{k} {v}" for k, v in cnt.most_common()) + ").\n")

L.append("## How to read the scores\n")
L.append("Opportunity score (0–100), per niche:\n")
L.append("```\nDemand = 0.35·P(Etsy searches ÷ Etsy competing listings)   [RankHero keyword pages]\n       + 0.25·P(median Etsy favorites per month, est.)    [RankHero favorites ÷ listing age estimated from listing ID]\n       + 0.15·P(median reviews on Gumroad/TpT/Amazon rows)\n       + 0.15·P(12-month search trend %)                   [RankHero Etsy trend + Google Trends YoY]\n       + 0.10·P(number of marketplaces where the niche appears)\nOpportunity = 100 · Demand · (1 − 0.5 · top3_shop_share)    [share of the niche's Etsy top listings held by its 3 biggest shops]\nP(x) = percentile rank of x among niches; a missing input scores 0.5 (neutral). evidence_n = how many of the 4 data inputs were present.\n```\n")
L.append("Niches need at least 15 collected rows to be ranked. `general-coloring` (no theme in the title) and Amazon supplies are excluded.\n")

L.append("## Top 20 niches by opportunity\n")
L.append("| # | Niche | Score | Evidence | Rows | Mkts | Etsy searches/listing | Trend % | Median $ | Etsy fav/mo (est) | Top-3 shop share | Japan-fit share |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, n in enumerate(ranked[:20], 1):
    L.append(f"| {i} | {n['niche']} | {n['opportunity_score']} | {n['evidence_n']}/4 | {n['rows_collected']} | {n['marketplaces']} | {fmt(n['search_per_listing_median'])} | {fmt(n['trend_pct_median'])} | {fmt(n['median_price_usd'])} | {fmt(n['etsy_median_fav_per_month_est'])} | {fmt(n['etsy_top3_shop_share'])} | {fmt(n['japan_fit_share'])} |")
if thin:
    L.append("\nToo few rows to rank (shown for reference): " + ", ".join(f"{n['niche']} ({n['rows_collected']} rows, score {n['opportunity_score']})" for n in thin) + ".\n")

L.append("\n## Top 50 velocity listings (Etsy, favorites per month)\n")
L.append("Velocity = favorites ÷ listing age in months. Etsy hid review counts, so favorites are the only per-listing engagement number available (from RankHero). Listing age is **estimated** from the Etsy listing ID, interpolated between " + str(len(anchors)) + " FindNiche anchors whose release date is known. Listings older than the earliest anchor are excluded because their age is only a lower bound.\n")
L.append("| # | Title | Shop | Price | Favorites | Listed (est) | Velocity | Metric | Niche | IP risk | Link |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(A["vel_etsy"], 1):
    L.append(f"| {i} | {t(r['title'], 60)} | {t(r['seller'], 22)} | {fmt(r['price'])} {r['currency']} | {fmt(r['favorites'])} | {r['listing_date'] or r['listing_date_est']} | {fmt(r['velocity_value'])} | {r['velocity_metric'].split('(')[0]} | {r['niche']} | {r['ip_risk'] or '–'} | [link]({r['source_url']}) |")
L.append("\n### Other velocity signals\n")
L.append("**Amazon** (ASINsight third-party monthly unit estimates; Amazon itself returned a CAPTCHA). `sales_per_day_est = monthly_sales_est ÷ 30.4`.\n")
L.append("| Title | Monthly sales (est) | Price | Reviews | Link |\n|---|---|---|---|---|")
for r in A["vel_amz"]:
    if r["niche"] == "supplies-not-a-book": continue
    L.append(f"| {t(r['title'], 70)} | {fmt(r['monthly_sales_est_thirdparty'])} | {fmt(r['price'])} | {fmt(r['review_count'])} | [link]({r['source_url']}) |")
L.append("\n**Gumroad: most-rated coloring products.** Gumroad shows no listing dates, so this is total ratings, not velocity.\n")
L.append("| Title | Creator | Price | Ratings | Sales shown | Link |\n|---|---|---|---|---|---|")
for r in A["gum_top"][:20]:
    L.append(f"| {t(r['title'], 60)} | {t(r['seller'], 25)} | {fmt(r['price'])} | {fmt(r['review_count'])} | {r['sales_shown']} | [link]({r['source_url']}) |")
if A["gum_sales"]:
    L.append("\n**Gumroad products that publicly show a sales count:**\n")
    L.append("| Title | Creator | Price | Sales shown | Link |\n|---|---|---|---|---|")
    for r in A["gum_sales"][:15]:
        L.append(f"| {t(r['title'], 60)} | {t(r['seller'], 25)} | {fmt(r['price'])} | {fmt(r['sales_shown'])} | [link]({r['source_url']}) |")
L.append("\n**Teachers Pay Teachers: most-reviewed coloring products** (kids and classroom demand):\n")
L.append("| Title | Price | Rating | Reviews | Link |\n|---|---|---|---|---|")
for r in A["tpt_top"][:10]:
    L.append(f"| {t(r['title'], 70)} | {fmt(r['price'])} | {r['rating']} | {fmt(r['review_count'])} | [link]({r['source_url']}) |")

L.append("\n## Title words that recur among top-velocity and most-rated listings\n")
L.append(", ".join(f"{w} ({c})" for w, c in A["words"]) + "\n")

L.append("## Seasonality calendar\n")
gt = A["gt"]
if gt:
    L.append("Google Trends (5-year weekly; index 0–100; monthly averages). `list_by` = 6 weeks before the start of the peak month, the middle of the 4–8 week indexing window.\n")
    L.append("| Term | Geo | Peak | 2nd | Trough | YoY % | 5-yr % | List by | " + " | ".join(MONTHS) + " |")
    L.append("|---|---|---|---|---|---|---|---|" + "---|" * 12)
    for g in gt:
        L.append(f"| {g['term']} | {g['geo']} | {g['peak_month']} | {g['second_peak']} | {g['trough_month']} | {fmt(g['yoy_pct_last52_vs_prev52'])} | {fmt(g['change_5y_pct'])} | {g['list_by']} | " + " | ".join(fmt(g[m], 0) for m in MONTHS) + " |")
rs = [r for r in A["rs"] if r["peak_month"] not in ("flat",)]
L.append("\nEtsy search seasonality (RankHero monthly Etsy searches, Sep 2025 – Aug 2026). Volumes are coarse buckets, so only clear peaks are listed:\n")
L.append("List-by dates already in the past (before 2026-10-25) mean: list immediately for this season's peak.\n")
L.append("| Etsy keyword | Peak month(s) | Trough | 12-mo trend % | List by |\n|---|---|---|---|---|")
for r in sorted(rs, key=lambda r: MONTHS.index(r["peak_month"].split("/")[0]) if r["peak_month"].split("/")[0] in MONTHS else 99):
    L.append(f"| {r['term']} | {r['peak_month']} | {r['trough_month']} | {fmt(r['yoy_pct_last52_vs_prev52'])} | {r['list_by']} |")
L.append("\n### Month-by-month launch calendar\n")
CAL = [("Jan", "Valentine's (peaks early Feb); spring/Easter prep; evergreen New-Year self-care, cozy and mindful sets"),
       ("Feb", "Easter/spring pages (Easter Apr 5 2027); start spring kawaii and garden sets"),
       ("Mar", "Summer/beach and ocean sets; Mother's Day gift bundles"),
       ("Apr", "Summer kids activity packs (school-holiday demand Jun–Aug)"),
       ("May", "Back-to-school classroom sets (TpT peaks Aug–Sep)"),
       ("Jun", "Halloween and spooky-cute, early: Etsy shoppers start in Aug–Sep"),
       ("Jul", "Halloween main launch; fall/autumn and cozy-season sets"),
       ("Aug", "Thanksgiving/fall; Christmas and advent sets; gift bundles"),
       ("Sep", "Christmas/winter main launch (Google 'coloring' terms peak Nov–Dec)"),
       ("Oct", "Last call for Christmas; New-Year self-care and mindful sets for the Jan bump"),
       ("Nov", "Valentine's and winter-cozy; Jan 'adult coloring' resolution demand"),
       ("Dec", "Spring and Easter prep; evergreen anime/kawaii drops when competition is busy with holidays")]
L.append("| Month to publish | What to list |\n|---|---|")
for m, w in CAL:
    L.append(f"| {m} | {w} |")

L.append("\n## Price ladder (USD; non-USD converted at fixed approximate rates)\n")
L.append("| Marketplace | Tier | n | 25th pct | Median | 75th pct | Share free |\n|---|---|---|---|---|---|---|")
for r in sorted(A["ladder"], key=lambda r: (r["marketplace"], r["tier"])):
    L.append(f"| {r['marketplace']} | {r['tier']} | {r['n']} | {fmt(r['p25'])} | {fmt(r['median'])} | {fmt(r['p75'])} | {fmt(r['share_free'])} |")

L.append("\n## Formats and bundles\n")
for m, c in A["formats"].items():
    if m in ("etsy", "gumroad", "teacherspayteachers", "amazon", "payhip", "itch.io"):
        L.append(f"- **{m}**: " + ", ".join(f"{k} {v}" for k, v in c))
for m, b in A["bundle"].items():
    metric = "favorites" if m == "etsy" else "ratings"
    L.append(f"- **{m} bundles vs single sets** (median {metric}): bundle {fmt(b['bundle_median'])} vs non-bundle {fmt(b['non_bundle_median'])} (n = {b['n'][1]} / {b['n'][0]})")

L.append("\n## Cross-marketplace overlap (niches present on 3+ sources)\n")
L.append("| Niche | Sources | Breakdown | Score |\n|---|---|---|---|")
for n in sorted(A["overlap"], key=lambda n: -n["marketplaces"]):
    if n["niche"] in EXCL: continue
    L.append(f"| {n['niche']} | {n['marketplaces']} | {n['by_marketplace']} | {n['opportunity_score']} |")

L.append("\n## Newcomer test\n")
L.append("Count of listings under 12 months old (actual or ID-estimated age) that already have 50+ reviews. Etsy hides reviews and Gumroad, TpT and Amazon show no dates, so I also count young Etsy listings with 100+ favorites as a proxy.\n")
L.append("| Niche | Listings < 12 mo | of which 50+ reviews | of which 100+ favorites (proxy) |\n|---|---|---|---|")
for n in sorted(niches, key=lambda n: -n["listings_lt12m_100plus_favorites"]):
    if n["listings_lt12m_age"]:
        L.append(f"| {n['niche']} | {n['listings_lt12m_age']} | {n['listings_lt12m_50plus_reviews']} | {n['listings_lt12m_100plus_favorites']} |")

L.append("\n## Anime / manga / kawaii / cozy Japan / retro gaming\n")
L.append("| Segment | Rows | Sources | Median $ | Median Gumroad ratings | Median Etsy favorites | Etsy fav/mo (est) | Fan-art rows | Women-lean share |\n|---|---|---|---|---|---|---|---|---|")
for s in A["jtab"]:
    L.append(f"| {s['segment']} | {s['rows']} | {s['marketplaces']} | {fmt(s['median_price_usd'])} | {fmt(s['median_gumroad_ratings'])} | {fmt(s['etsy_median_favorites'])} | {fmt(s['etsy_median_fav_per_month_est'])} | {s['ip_fanart_rows']} | {fmt(s['women_lean_share'])} |")
if A["jkw"]:
    L.append("\nEtsy keyword demand for these terms (RankHero):\n")
    L.append("| Keyword | Monthly Etsy searches | Competing listings | Searches/listing | Trend | Median price |\n|---|---|---|---|---|---|")
    for k in A["jkw"]:
        sr, el = k["monthly_searches"], k["etsy_listings"]
        ratio = (float(sr) / float(el)) if sr and el and float(el) else None
        L.append(f"| {k['keyword']} | {fmt(sr)} | {fmt(el)} | {fmt(ratio)} | {t(k['trend_sentence'], 60) or '–'} | {k['median_price'].rstrip('.')} |")
kkj = [k for k in A["kk"] if re.search(r"anime|kawaii|manga|japan", k["niche"])]
if kkj:
    L.append("\nKupkaike (third-party, live Etsy count): " + "; ".join(f"{k['niche']}: {k['status']}, {k['active_listings']} relevant listings, median {k['median_price']}, {k['share_under_5']}% under $5, {k['top100_shops']} shops in top 100" for k in kkj) + "\n")
L.append("\nTop listings in this segment (IP-risk flag: `fan-art/trademark` means the title names a trademarked character or brand; `original anime-style` means a generic style with low risk):\n")
L.append("| Segment | Source | Title | $ | Ratings/Reviews | Favorites | Velocity | IP risk | Link |\n|---|---|---|---|---|---|---|---|---|")
for r in A["jlist"]:
    L.append(f"| {r.get('_sub', '')} | {r['marketplace']} | {t(r['title'], 55)} | {fmt(r['price_usd_est'])} | {fmt(r['review_count'])} | {fmt(r['favorites'])} | {fmt(r['velocity_value'])} {r['velocity_metric'].split('(')[0]} | {r['ip_risk'] or '–'} | [link]({r['source_url']}) |")

L.append("\n## Do NOT enter (saturated or dominated)\n")
dn = []
for n in niches:
    reasons = []
    if n["etsy_competing_listings_max_kw"] and float(n["etsy_competing_listings_max_kw"]) > 100000 and (n["search_per_listing_median"] or 9) < 1:
        reasons.append(f"{fmt(n['etsy_competing_listings_max_kw'])} competing Etsy listings with under 1 search per listing")
    etsy_n = int((re.search(r"etsy:(\d+)", n["by_marketplace"]) or [0, 0])[1])
    if n["etsy_top3_shop_share"] and n["etsy_top3_shop_share"] >= 0.5 and etsy_n >= 8:
        reasons.append(f"top-3 shops hold {fmt(n['etsy_top3_shop_share'])} of its {etsy_n} Etsy top listings")
    if n["trend_pct_median"] is not None and n["trend_pct_median"] <= -20:
        reasons.append(f"search trend {fmt(n['trend_pct_median'])}%")
    if n["niche"] == "mega-bundle-plr":
        reasons.append("race to the bottom: $1–7 for 10,000+ resell-rights pages floods the low end")
    if reasons:
        dn.append((n["niche"], reasons))
for n, rs_ in dn:
    L.append(f"- **{n}**: " + "; ".join(rs_))
L.append("- **Fan art of trademarked characters** (Sanrio, Pokémon, Ghibli, Disney, KPop Demon Hunters and similar): rows with this flag show demand but carry takedown risk on your own site. Sell original anime-style characters instead.")
L.append("- **Broad head terms** ('coloring pages', 'coloring book', 'adult coloring pages'): huge search volume, but 400k+ Etsy listings target them. Use them as secondary tags only.\n")

L.append("## Recommendations for your shop (anime / kawaii / cozy Japan / retro / J-pop; mostly women buyers)\n")
L.append("Derived from the tables above. See REPORT data files for the numbers behind each point.\n")
L.append(open(os.path.join(os.path.dirname(__file__), "recs.md"), encoding="utf-8").read())
open(os.path.join(OUT, "REPORT.md"), "w", encoding="utf-8").write("\n".join(L))

# ---------------- COVERAGE ----------------
log = rd(os.path.join(RAW, "fetch_log.csv"))
ips = rd(os.path.join(RAW, "ip_checks.csv"))
ver = rd(os.path.join(OUT, "verification.csv"))
C2 = ["# COVERAGE\n", "_Collection 2026-10-25 UTC from a Google Cloud US egress (verified with ipinfo.io before every new site and every 30 minutes; never MA or the flagged IP)._\n"]
C2.append(f"IP checks run: {len(ips)}. Countries seen: {dict(Counter(r['country'] for r in ips))}. Orgs: {dict(Counter(r['org'] for r in ips))}.\n")
C2.append("## Rows per source\n")
C2.append("| Marketplace | Master rows | Route(s) |\n|---|---|---|")
routes = defaultdict(Counter)
for r in rows:
    routes[r["marketplace"]][r["fetch_route"].split(";")[0]] += 1
for m, c in cnt.most_common():
    C2.append(f"| {m} | {c} | " + "; ".join(f"{k} ({v})" for k, v in routes[m].most_common()) + " |")
raw_counts = {
    "gumroad tier A rows (all query×sort hits, before dedupe)": len(rd(os.path.join(RAW, "gumroad", "gumroad_tierA.csv"))),
    "gumroad tier B product pages": len(rd(os.path.join(RAW, "gumroad", "gumroad_tierB.csv"))),
    "RankHero Etsy keyword pages": len(rd(os.path.join(RAW, "thirdparty", "rankhero_keywords.csv"))),
    "RankHero Etsy listing cards (before dedupe)": len(rd(os.path.join(RAW, "thirdparty", "rankhero_listings.csv"))),
    "FindNiche Etsy product pages (coloring)": len(rd(os.path.join(RAW, "thirdparty", "findniche_listings.csv"))),
    "FindNiche ID/date anchors": len(anchors),
    "Kupkaike niche pages": len(rd(os.path.join(RAW, "thirdparty", "kupkaike_niches.csv"))),
    "ASINsight Amazon rows": len(rd(os.path.join(RAW, "thirdparty", "asinsight_amazon.csv"))),
    "TpT rows (before dedupe)": len(rd(os.path.join(RAW, "others", "tpt.csv"))),
    "itch.io rows": len(rd(os.path.join(RAW, "others", "itch.csv"))),
    "WebSearch result rows": sum(1 for _ in open(os.path.join(RAW, "websearch", "ws_rows.tsv"))),
    "Reddit RSS posts (demand signals)": len(rd(os.path.join(RAW, "reddit", "reddit_signals.csv"))),
    "Google Trends series": len(A["gt"]),
}
C2.append("\n## Raw collection counts\n")
for k, v in raw_counts.items():
    C2.append(f"- {k}: {v}")
C2.append("\n## Targets vs achieved\n")
C2.append(f"""| Source | Target | Achieved | Status |
|---|---|---|---|
| Etsy tier A | 800+ | {cnt.get('etsy', 0)} unique listings | Etsy direct BLOCKED (DataDome); rows come from RankHero, FindNiche and WebSearch |
| Etsy tier B | 150+ | {raw_counts['FindNiche Etsy product pages (coloring)']} with sales/reviews/date (FindNiche) | Listing pages unreachable; listing date, shop sales and review dates not available |
| Gumroad | 200+ | {cnt.get('gumroad', 0)} | Done (curl, tier A + tier B) |
| Amazon/KDP | 300+ | {cnt.get('amazon', 0)} (ASINsight) | Amazon BLOCKED (CAPTCHA on the first slow retry); no BSR, publisher, page count or size |
| eBay sold | 150+ | 0 | BLOCKED (403); WebSearch found no sold data |
| Payhip | – | {cnt.get('payhip', 0)} (WebSearch) | Direct BLOCKED (403 CAPTCHA) |
| Others (4+) | 4 | Teachers Pay Teachers ({cnt.get('teacherspayteachers', 0)}), itch.io ({cnt.get('itch.io', 0)}), plus Creative Market ({cnt.get('creativemarket', 0)}) and TikTok Shop ({cnt.get('tiktokshop', 0)}) via WebSearch | Creative Fabrica, Ko-fi and Creative Market direct: BLOCKED (Cloudflare). Barnes & Noble: bot-filter 404. Walmart, Lulu, Redbubble: not attempted. |
| Reddit | 3+ subs | {raw_counts['Reddit RSS posts (demand signals)']} posts, r/adultcoloring only | 429 after 2 requests (30 s gap); one resume at 90–120 s got 1 more request, then 429 again; stopped for good |
| Google Trends | 21 terms × 2 geos | {len(A['gt'])} series (worldwide only) | pytrends: 429 after 5 series. An early resume about 6 minutes after the 429 (a timing mistake on my side) fetched 1 more series (kawaii coloring) before I stopped it. A proper resume after a 35-minute cooldown at 120–150 s spacing got a 429 on its first request, so it was stopped for good. Glimpse and Exploding Topics have no public pages for these terms (404). US series and the other terms are covered only by RankHero's Etsy monthly series in seasonality.csv. |
""")
C2.append("\n**Why these four 'others':** Teachers Pay Teachers (ratings and review counts for the kids/classroom niche; reachable by curl), itch.io (indie anime-style creators, reachable), Creative Market and TikTok Shop (appeared repeatedly in WebSearch with bold-and-easy/cozy products and a 'sold' count). Walmart, Lulu and Redbubble were skipped: they are print-on-demand or retail and less informative for a digital seller than the sources above.\n")
C2.append("**Third-party Etsy route:** eRank, EverBee, Alura, Marmalead, InsightFactory and Sale Samurai public pages gave no niche-level coloring data (the tools are behind logins). RankHero (keyword volume, listing counts, monthly series and top-12 listings with favorites and views), FindNiche (per-listing sales, reviews and release date) and Kupkaike (live Etsy listing counts) were used instead.\n")
C2.append("\n## Blocked / failed URLs\n")
C2.append("| Time (UTC) | Site | URL | HTTP | Note |\n|---|---|---|---|---|")
for r in log:
    if "BLOCKED" in r["note"] or r["http"] in ("403", "429", "ERR"):
        C2.append(f"| {r['fetched_at']} | {r['site']} | {t(r['url'], 90)} | {r['http']} | {r['note']} |")
C2.append("| 2026-10-25T15:13Z | etsy.com, gumroad.com | WebFetch (first pilot) | – | WebFetch DNS failure (ENOTFOUND) for every host; WebFetch unusable in this container |")
C2.append("| 2026-10-25T15:29Z | etsy.com | https://www.etsy.com/search?q=kawaii+coloring+pages | 403 | DataDome CAPTCHA (pilot 2). Not retried. |")
C2.append("| 2026-10-25T15:30Z | ebay.com, payhip.com, creativefabrica.com, ko-fi.com | pilot probes | 403 | eBay error page, Payhip CAPTCHA, Cloudflare challenges |")
C2.append(f"\nTotal logged requests: {len(log)} (" + ", ".join(f"{k} {v}" for k, v in Counter(r['site'] for r in log).most_common()) + ").\n")

C2.append("## Fields missing (share of master rows where the field is blank or NOT SHOWN)\n")
fields = ["price", "rating", "review_count", "sales_shown", "bestseller_badge", "favorites", "listing_date", "listing_date_est", "bsr", "page_count", "seller"]
C2.append("| Marketplace | " + " | ".join(fields) + " |\n|---|" + "---|" * len(fields))
for m, _ in cnt.most_common():
    rr = [r for r in rows if r["marketplace"] == m]
    C2.append(f"| {m} | " + " | ".join(f"{100 * sum(1 for r in rr if r[f] in ('', 'NOT SHOWN', 'NOT FETCHED', 'n/a') or r[f].startswith('NOT SHOWN')) / len(rr):.0f}%" for f in fields) + " |")
C2.append("\nNot collectable at all: Etsy Star Seller, Ad flag, shop total sales, shop open year and review dates (listing pages blocked); Amazon BSR, publisher, independently-published flag, page count and size (blocked); eBay sold prices (blocked).\n")

C2.append("## Verification (random 5% re-fetch)\n")
chk = [v for v in ver if v["match"] in ("True", "False")]
mis = [v for v in chk if v["match"] == "False"]
nv = Counter(v["match"] for v in ver if v["match"] not in ("True", "False"))
if ver:
    C2.append(f"Sampled {len(ver)} rows (5% of {len(rows)}, seed 20261025). Re-fetched and compared: {len(chk)}. **Mismatch rate: {len(mis)}/{len(chk)} = {100 * len(mis) / max(len(chk), 1):.1f}%.** Not verifiable: " + ", ".join(f"{k} ({v})" for k, v in nv.items()) + ".\n")
    if mis:
        C2.append("| Source | Field | Old | New | Title |\n|---|---|---|---|---|")
        for v in mis:
            C2.append(f"| {v['marketplace']} | {v['field']} | {t(v['old'], 30)} | {t(v['new'], 40)} | {t(v['title'], 50)} |")
    C2.append("\nThe one remaining mismatch is a free TpT item: the re-fetched card shows no '$x Original Price' string, so the verifier read the price as missing. It is most likely a verifier limitation, not a data error. The first two verifier runs reported higher mismatch rates because of bugs in the verifier itself (it matched the ASIN inside JSON-LD, checked page 1 for page-2 TpT rows, and failed on HTML-entity and ISO-code prices). After those fixes, each check was re-run against the same re-fetched pages. Verification compares price + ratings for Gumroad, price + favorites for Etsy/RankHero, price + reviews for TpT, and monthly sales for ASINsight. See `verification.csv`.\n")

C2.append("## Every estimate and its formula\n")
C2.append(f"""- `listing_date_est` / `listing_age_days_est` (Etsy): piecewise-linear interpolation of listing ID → date between {len(anchors)} FindNiche anchors (listing ID with a published 'Released' date): {', '.join(f'{a}→{d}' for a, d in anchors)}. IDs above the last anchor are extrapolated on the last segment. IDs below the first anchor take the first anchor date, so their age is a LOWER BOUND; these are flagged in `fetch_route` and excluded from velocity rankings.
- `velocity_value` (Etsy) = favorites ÷ max(listing_age_days(_est) ÷ 30.4, 1). Where a review count exists (FindNiche), it is reviews ÷ months instead (`velocity_metric` says which).
- `sales_est_thirdparty`, `monthly_sales_est_thirdparty` (Etsy): FindNiche's own tracked estimates, copied as published.
- `monthly_sales_est_thirdparty` (Amazon): ASINsight's 'Units Sold/mo' estimate for the report month shown in `notes`. `sales_per_day_est = monthly ÷ 30.4`. **The BSR-to-sales table method was not possible because Amazon blocked every product and list page, so no BSR was collected.**
- `price_usd_est`: price × fixed approximate FX (EUR 1.08, GBP 1.27, CAD 0.73, AUD 0.66, NOK 0.093).
- `niche`, `style`, `audience`, `anime_japan_kawaii_fit`, `women_lean`, `season`, `ip_risk`: rule-based keyword classification of titles (scripts/classify.py). These are labels, not measurements.
- Opportunity score: formula in REPORT.md. Percentile-based, so it is relative between niches, not absolute.
- Google Trends `yoy_pct` = mean(last 52 weeks) ÷ mean(previous 52) − 1; `change_5y_pct` = mean(last 52) ÷ mean(first 52) − 1; `list_by` = 1st of peak month − 6 weeks.
- RankHero monthly Etsy search volumes are bucketed (e.g. 673k / 823k / 1M), so Etsy seasonality is coarse.
""")
C2.append("## Data accuracy notes\n")
C2.append("- Marketplace rows via curl were parsed from the raw HTML/JSON (verbatim values). Raw pages are kept in the session scratchpad; parsed raw CSVs are committed under `raw/`.\n- WebSearch rows (`fetch_route=websearch`): titles are search-result titles. Prices in `notes` marked 'summary' come from the search tool's own summary, not the page, and should be treated as unverified.\n- Gumroad `sales_shown` is 'NOT SHOWN' where the creator hides the count (most do).\n")
open(os.path.join(OUT, "COVERAGE.md"), "w", encoding="utf-8").write("\n".join(C2))
print("reports written")
