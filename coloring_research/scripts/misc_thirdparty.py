"""ASINsight Amazon keyword reports (third-party sales estimates) + Kupkaike Etsy niche pages."""
import csv, html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "thirdparty")


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def k(s):
    s = (s or "").replace(",", "")
    m = re.match(r"([0-9.]+)([KkM]?)", s)
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "k": 1e3, "M": 1e6}[m.group(2)]) if m else ""


def asinsight(slugs=None):
    rows = list(csv.DictReader(open(os.path.join(RAW, "asinsight_amazon.csv")))) if slugs and os.path.exists(os.path.join(RAW, "asinsight_amazon.csv")) else []
    for slug in slugs or ["adult-coloring-books", "coloring-book", "coloring-books-for-adults", "coloring-books",
                 "coloring-books-for-kids", "anime-coloring-book", "bold-and-easy-coloring-book",
                 "cozy-coloring-book", "kawaii-coloring-book", "coloring-book-for-adults",
                 "christmas-coloring-book", "halloween-coloring-book", "mandala-coloring-book"]:
        url = f"https://www.asinsight.com/report/US/{slug}"
        try:
            status, b = fetch("asinsight.com", url, os.path.join(RAW, f"asinsight_{slug}.html"), 6, 9)
        except SiteBlocked as e:
            print("BLOCKED", e); break
        t = text(b)
        if status != "200" or "Units Sold/mo" not in t:
            print("miss", slug, status, flush=True); continue
        month = (re.search(r"Market Trends ([A-Z][a-z]+ \d{4})", t) or [None, ""])[1]
        tracked = (re.search(r"(\d[\d,]*) Products Tracked", t) or [None, ""])[1]
        for m in re.finditer(r"(?:🏆 )?#?(\d{1,2}) (B0[0-9A-Z]{8}|\d{9}[0-9X]) (?:\$([0-9.]+) ★ ([0-9.]+) \(([0-9.KM]+)\) (.*?)|(.*?)) ([0-9,]+) Units Sold/mo(?: \$([0-9.]+) Price ★ ([0-9.]+) Rating ([0-9.KM]+) Reviews)?", t):
            rank, asin = m.group(1), m.group(2)
            title = (m.group(6) or m.group(7) or "").strip()
            rows.append({"keyword": slug.replace("-", " "), "report_month": month, "products_tracked": tracked,
                         "rank": rank, "asin": asin, "title": title[:250],
                         "price": m.group(3) or m.group(9), "rating": m.group(4) or m.group(10),
                         "reviews": k(m.group(5) or m.group(11)),
                         "monthly_sales_est_thirdparty": m.group(8).replace(",", ""),
                         "is_book": "no" if re.search(r"pencil|marker|pen[s ,]|crayon|paint|gel|sharpener", title, re.I) else "yes",
                         "source_url": url, "fetched_at": utcnow(), "fetch_route": "third_party"})
        print("asinsight", slug, month, len(rows), flush=True)
        with open(os.path.join(RAW, "asinsight_amazon.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def kupkaike():
    rows, seen = [], set()
    queue = ["colouring-pages", "children-s-coloring-book-for-ages-4-8", "cute-cozy-coloring-pages-bundle",
             "anime-colouring-books", "kawaii-coloring-pages", "coloring-pages", "adult-coloring-pages",
             "bold-and-easy-coloring-pages", "cozy-coloring-pages", "anime-coloring-pages", "mandala-coloring-pages",
             "halloween-coloring-pages", "christmas-coloring-pages", "grayscale-coloring-pages",
             "procreate-coloring-pages", "manga-coloring-pages", "japanese-coloring-pages"]
    while queue and len(seen) < 40:
        slug = queue.pop(0)
        if slug in seen: continue
        seen.add(slug)
        url = f"https://kupkaike.com/niche/{slug}"
        try:
            status, b = fetch("kupkaike.com", url, os.path.join(RAW, f"kk_{slug}.html"), 6, 9)
        except SiteBlocked as e:
            print("BLOCKED", e); break
        t = text(b)
        if status != "200" or "Etsy" not in t:
            print("miss", slug, status, flush=True); continue
        g = lambda p: (re.search(p, t) or [None, ""])[1]
        rows.append({"niche": slug.replace("-", " "), "status": g(r"is rated (\w+) for digital"),
                     "score": g(r"(\d+)/100"), "competition": g(r"Competition (\w+)"),
                     "price_range": g(r"typically priced at (\$[0-9]+-\$[0-9]+)"),
                     "active_listings": g(r"([0-9,]+) relevant active listings"),
                     "raw_listings": g(r"[0-9,]+ of ([0-9,]+) truly relevant"),
                     "median_price": g(r"Median (\$[0-9.]+)"), "share_under_5": g(r"(\d+)% under \$5"),
                     "top100_shops": g(r"(\d+) shops share the top 100"),
                     "verified": g(r"(?:last verified|Measured on live Etsy listings ·) ([A-Z][a-z]+ \d+, \d{4})"),
                     "source_url": url, "fetched_at": utcnow(), "fetch_route": "third_party"})
        for rel in re.findall(r'href="/niche/([a-z0-9-]+)"', b):
            if re.search(r"colou?r", rel) and rel not in seen:
                queue.append(rel)
        print("kk", slug, rows[-1]["status"], rows[-1]["active_listings"], flush=True)
        with open(os.path.join(RAW, "kupkaike_niches.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            asinsight(sys.argv[1:])
        else:
            asinsight(); kupkaike()
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    print("DONE misc")
