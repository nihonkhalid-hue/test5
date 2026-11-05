"""ASINsight public keyword reports (Amazon US top products with Units Sold/mo estimates).
Slugs come from asinsight's own sitemap (filtered to book/KDP terms, priority-ordered). 6-9 s pacing."""
import csv, html, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
D = os.path.join(BASE, "pages", "asinsight"); os.makedirs(D, exist_ok=True)
SM = os.path.join(BASE, "pages", "asi_sm", "b3.txt")
OUT = os.path.join(REPO, "raw", "amazon_asinsight.csv")
PRI = [r"colou?ring-book|coloring-pages|coloring-books", r"word-search|sudoku|crossword|puzzle|maze|dot-to-dot|brain-games|logic",
       r"journal|diary", r"planner", r"workbook|tracing|handwriting|activity|sticker-book|preschool|kindergarten|learn",
       r"manga|anime|kawaii|drawing|how-to-draw|sketchbook|sketch-book|art-book",
       r"romance|novel|romantasy|fantasy|mystery|thriller|smut|fiction|cookbook|devotional|self-help|bible",
       r"password|log|record-book|guest-book|ledger|address-book|recipe",
       r"books?-for-|book$|books$|picture-book|board-book|composition", r"."]
NOT = re.compile(r"food-coloring|hair-coloring|coloring-gel|gel-food|egg-coloring|-dye")


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def k(s):
    s = (s or "").replace(",", "")
    m = re.match(r"([0-9.]+)([KkM]?)", s)
    return str(int(float(m.group(1)) * {"": 1, "K": 1e3, "k": 1e3, "M": 1e6}[m.group(2)])) if m else "NOT SHOWN"


BOOKISH = re.compile(r"book|journal|notebook|planner|diary|novel|edition|paperback|hardcover|volume|vol\.|workbook|"
                     r"puzzles?|word search|sudoku|coloring|colouring|sketchbook|log ?book|for kids|ages|stories|"
                     r"guide|bible|devotional|manga|series", re.I)
SUPPLY = re.compile(r"pencils?\b|markers?\b|\bpens?\b|crayons?|paint|gel\b|sharpener|eraser|highlighter|stickers? pack|"
                    r"\bpack of\b|\bcase\b|holder|tablet|ipad|cover for|storage", re.I)


def parse(fp, slug, url, ts):
    t = text(open(fp, encoding="utf-8", errors="ignore").read())
    if "Units Sold/mo" not in t: return []
    month = (re.search(r"Market Trends ([A-Z][a-z]+ \d{4})", t) or [None, "NOT SHOWN"])[1]
    tracked = (re.search(r"(\d[\d,]*) Products Tracked", t) or [None, "NOT SHOWN"])[1]
    rows, seen = [], set()
    for m in re.finditer(r"(?:🏆 )?#?(\d{1,3}) (B0[0-9A-Z]{8}|\d{9}[0-9X]) (?:\$([0-9.,]+) ★ ([0-9.]+) \(([0-9.KM]+)\) (.*?)|(.*?)) ([0-9,.]+K?) Units Sold/mo(?: \$([0-9.,]+) Price ★ ([0-9.]+) Rating ([0-9.KM]+) Reviews)?", t):
        rank, asin = m.group(1), m.group(2)
        if (rank, asin) in seen: continue
        seen.add((rank, asin))
        title = (m.group(6) or m.group(7) or "").strip()
        if " Units/sold " in title: title = "NOT SHOWN (summary card)"
        isb = "yes" if (asin[0].isdigit() or (BOOKISH.search(title) and not SUPPLY.search(title))) else ("unclear" if title.startswith("NOT SHOWN") else "no")
        rows.append({"keyword": slug.replace("-", " "), "slug": slug, "report_month": month, "products_tracked": tracked.replace(",", ""),
                     "rank": rank, "asin": asin, "isbn10_asin": "yes" if asin[0].isdigit() else "no", "title": title[:300],
                     "price": (m.group(3) or m.group(9) or "NOT SHOWN").replace(",", ""),
                     "rating": m.group(4) or m.group(10) or "NOT SHOWN",
                     "reviews": k(m.group(5) or m.group(11)),
                     "monthly_sales_est_thirdparty": k(m.group(8)), "is_book": isb,
                     "source_url": url, "fetched_at": ts, "fetch_route": "third_party:asinsight"})
    # exact title/price/rating/review count from the page's schema.org ItemList (JSON-LD)
    import json
    raw = open(fp, encoding="utf-8", errors="ignore").read()
    ld = {}
    for js in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            d = json.loads(js)
        except Exception:
            continue
        if d.get("@type") == "ItemList":
            for el in d.get("itemListElement", []):
                it = el.get("item") or {}
                ld[it.get("sku")] = it
    for r in rows:
        it = ld.get(r["asin"])
        r["title_ld"] = it.get("name", "NOT SHOWN")[:300] if it else "NOT SHOWN"
        r["review_count_exact"] = str((it.get("aggregateRating") or {}).get("reviewCount", "NOT SHOWN")) if it else "NOT SHOWN"
        r["price_ld"] = str((it.get("offers") or {}).get("price", "NOT SHOWN")) if it else "NOT SHOWN"
        if r["title"].startswith("NOT SHOWN") and it:
            t2 = r["title_ld"]
            r["is_book"] = "yes" if (r["asin"][0].isdigit() or (BOOKISH.search(t2) and not SUPPLY.search(t2))) else "no"
    return rows


def main():
    slugs = [s.strip() for s in open(SM) if s.strip() and not NOT.search(s)]
    extra = [s for s in sys.argv[1:]]
    order = extra + [s for p in PRI for s in slugs if re.search(p, s)]
    seen, plan = set(), []
    for s in order:
        if s not in seen: seen.add(s); plan.append(s)
    limit = int(os.environ.get("ASI_LIMIT", "1600"))
    done = set()
    if os.path.exists(OUT):
        done = {r["slug"] for r in csv.DictReader(open(OUT))}
    miss_f = os.path.join(REPO, "raw", "asinsight_misses.csv")
    if os.path.exists(miss_f): done |= {l.split(",")[0] for l in open(miss_f)}
    n = 0; t0 = time.time()
    for slug in plan[:limit]:
        if slug in done: continue
        url = f"https://www.asinsight.com/report/US/{slug}"
        fp = os.path.join(D, slug[:150] + ".html")
        st, _ = fetch("asinsight.com", url, fp, 6, 9)
        rows = parse(fp, slug, url, utcnow()) if st == "200" else []
        n += 1
        if not rows:
            open(miss_f, "a").write(f"{slug},{st},{utcnow()}\n")
        else:
            new = not os.path.exists(OUT)
            with open(OUT, "a", newline="") as f:
                w = csv.DictWriter(f, list(rows[0].keys()))
                if new: w.writeheader()
                w.writerows(rows)
        print(n, slug, st, len(rows), f"{(time.time()-t0)/60:.0f}m", flush=True)


if __name__ == "__main__":
    try:
        main()
    except SiteBlocked as e:
        print("BLOCKED", e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE asinsight", flush=True)
