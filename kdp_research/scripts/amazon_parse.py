"""Parse saved Amazon pages (best-seller-type lists + dp product pages) -> raw/amazon_direct_lists.csv, raw/amazon_direct_dp.csv.
Values verbatim; NOT SHOWN where absent. CAPTCHA pages are skipped (logged as BLOCKED in fetch_log)."""
import csv, glob, html, json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from netlib import BASE, REPO
P = os.path.join(BASE, "pages")


def T(s): return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def mtime(fp): return datetime.datetime.fromtimestamp(os.path.getmtime(fp), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def index():
    idx = {}
    for f in glob.glob(os.path.join(P, "amazon_*", "index.csv")):
        for r in csv.DictReader(open(f)):
            idx[os.path.join(os.path.dirname(f), r["file"])] = r
    idx[os.path.join(P, "pilot", "amazon_com.html")] = {"list": "bestsellers", "node_path": "books/11357541011", "node_name": "Coloring Books for Grown-Ups", "page": "1", "url": "https://www.amazon.com/gp/bestsellers/books/11357541011", "fetched_at": ""}
    idx[os.path.join(P, "pilot", "amazon_co_uk.html")] = {"list": "bestsellers", "node_path": "books", "node_name": "Books (root)", "page": "1", "url": "https://www.amazon.co.uk/gp/bestsellers/books/", "fetched_at": ""}
    return idx


def parse_list(fp, meta, mk):
    b = open(fp, encoding="utf-8", errors="ignore").read()
    if "validateCaptcha" in b or len(b) < 50000: return []
    title = T((re.search(r"<title>(.*?)</title>", b, re.S) or [None, ""])[1])
    ts = meta.get("fetched_at") or mtime(fp)
    out, rendered = [], {}
    for it in re.split(r'id="gridItemRoot"', b)[1:]:
        asin = re.search(r'data-asin="([A-Z0-9]{10})"', it) or re.search(r'/dp/([A-Z0-9]{10})', it)
        if not asin: continue
        g = lambda p: (re.search(p, it, re.S) or [None, None])[1]
        rv = re.search(r'aria-label="([0-9.]+) out of 5 stars, ([0-9,]+) ratings?"', it)
        pr = g(r'p13n-sc-price[^"]*">([^<]+)<') or g(r'class="a-color-price"[^>]*>(?:<span[^>]*>)?([^<]+)<')
        rendered[asin.group(1)] = {
            "title": html.unescape(g(r'line-clamp-\d[^"]*">([^<]+)<') or "NOT SHOWN"),
            "author": html.unescape(g(r'class="a-size-small a-link-child"[^>]*>(?:<div[^>]*>)?([^<]+)<') or g(r'<span class="a-size-small a-color-base">([^<]+)<') or "NOT SHOWN"),
            "rating": rv.group(1) if rv else "NOT SHOWN", "reviews": rv.group(2).replace(",", "") if rv else "NOT SHOWN",
            "format": html.unescape(g(r'a-size-small a-color-secondary a-text-normal">([^<]+)<') or "NOT SHOWN"),
            "price": html.unescape(pr.strip()) if pr else "NOT SHOWN"}
    m = re.search(r'data-client-recs-list="([^"]+)"', b)
    recs = json.loads(html.unescape(m.group(1))) if m else []
    page = int(meta.get("page") or 1)
    for it in recs:
        md = it.get("metadataMap", {})
        a = it["id"]; r = rendered.get(a, {})
        out.append({"marketplace": mk, "list": meta.get("list"), "node_path": meta.get("node_path"), "node_name": meta.get("node_name"),
                    "page_title": title, "page": page, "rank": md.get("render.zg.rank", "NOT SHOWN"), "asin": a,
                    "title": r.get("title", "NOT SHOWN (not rendered server-side)"), "author": r.get("author", "NOT SHOWN"),
                    "rating": r.get("rating", "NOT SHOWN"), "reviews": r.get("reviews", "NOT SHOWN"),
                    "format": r.get("format", "NOT SHOWN"), "price": r.get("price", "NOT SHOWN"),
                    "ms_current_sales_rank": md.get("render.zg.bsms.currentSalesRank") or "NOT SHOWN",
                    "ms_pct_change": md.get("render.zg.bsms.percentageChange") or "NOT SHOWN",
                    "ms_rank_24h_ago": md.get("render.zg.bsms.twentyFourHourOldSalesRank") or "NOT SHOWN",
                    "fetched_at": ts, "source_url": meta.get("url"), "fetch_route": "curl"})
    return out


def parse_dp(fp, mk, meta):
    b = open(fp, encoding="utf-8", errors="ignore").read()
    if "validateCaptcha" in b or len(b) < 50000: return None
    t = T(re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S))
    g = lambda p: (re.search(p, t) or [None, "NOT SHOWN"])[1].strip()
    sep = r"\s*[:‏‎‏‎]*\s*"
    bsr = g(r"Best Sellers Rank" + sep + r"(.{0,400}?)(?:Customer Reviews|Videos|$)")
    return {"marketplace": mk, "asin": os.path.basename(fp)[3:13], "title": T((re.search(r'id="productTitle"[^>]*>(.*?)</span>', b, re.S) or [None, "NOT SHOWN"])[1]),
            "publisher": g(r"Publisher" + sep + r"([^‏‎]{2,80}?)\s*(?:\(|Publication date|Language|$)"),
            "publication_date": g(r"Publication date" + sep + r"([A-Z][a-z]+ \d{1,2}, \d{4})"),
            "print_length": g(r"(?:Print length|Paperback|Spiral-bound|Hardcover)" + sep + r"([0-9,]+ pages)"),
            "dimensions": g(r"Dimensions" + sep + r"([0-9.]+ x [0-9.]+ x [0-9.]+ (?:inches|cm))"),
            "bsr_text": bsr[:400], "fetched_at": meta.get("fetched_at") or mtime(fp), "source_url": meta.get("url", ""), "fetch_route": "curl"}


def main():
    idx = index(); L, DP = [], []
    for fp, meta in idx.items():
        if not os.path.exists(fp): continue
        mk = "amazon.co.uk" if "co_uk" in fp else "amazon.de" if "amazon_de" in fp else "amazon.ca" if "amazon_ca" in fp else "amazon.com"
        if meta.get("list") == "dp":
            r = parse_dp(fp, mk, meta)
            if r: DP.append(r)
        else:
            L += parse_list(fp, meta, mk)
    for name, rows in (("amazon_direct_lists.csv", L), ("amazon_direct_dp.csv", DP)):
        if rows:
            with open(os.path.join(REPO, "raw", name), "w", newline="") as f:
                w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("lists rows", len(L), "dp rows", len(DP))


if __name__ == "__main__":
    main()
