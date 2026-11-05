"""Offline parser for saved RankHero Etsy keyword pages -> raw/etsy_rankhero_keywords_parsed.csv, raw/etsy_rankhero_listings.csv."""
import csv, datetime, glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import BASE, REPO


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def num(s):
    s = (s or "").replace(",", "").strip()
    m = re.match(r"([0-9.]+)\s*([KkMm]?)", s)
    return int(float(m.group(1)) * {"": 1, "k": 1e3, "m": 1e6}[m.group(2).lower()]) if m else "NOT SHOWN"


kw_rows, li_rows = [], []
fetched = {r["source_url"]: r["fetched_at"] for r in csv.DictReader(open(os.path.join(REPO, "raw", "etsy_rankhero_keywords.csv")))}
for fp in sorted(glob.glob(os.path.join(BASE, "pages", "rankhero", "*.html"))):
    slug = os.path.basename(fp)[:-5]; url = f"https://www.rankhero.com/keywords/{slug}"
    b = open(fp, encoding="utf-8", errors="ignore").read()
    if "Keyword overview" not in b: continue
    t = text(b); ts = fetched.get(url, "")
    g = lambda p: (re.search(p, t) or [None, "NOT SHOWN"])[1]
    months = re.findall(r"((?:January|February|March|April|May|June|July|August|September|October|November|December) 20\d\d) ([0-9,]+)", t)
    kw_rows.append({"keyword": slug.replace("-", " "), "monthly_searches": num(g(r"Monthly search volume ([0-9,]+)")),
                    "etsy_competition_listings": num(g(r"Competition ([0-9,]+)")), "cpc": g(r"Cost per click (\$[0-9.]+)"),
                    "difficulty": g(r"Keyword difficulty ([0-9]+) ?/100"), "share_under_10": g(r"Under \$10 (\d+%)"),
                    "monthly_series": json.dumps([(m, num(v)) for m, v in months[:12]]),
                    "source_url": url, "fetched_at": ts, "fetch_route": "third_party:rankhero"})
    i = b.find("Top Etsy listings for")
    for rank, (lid, c) in enumerate(re.findall(r'<a href="https://www\.etsy\.com/listing/(\d+)"(.*?)</a>', b[i:], re.S), 1):
        title = re.search(r"<p[^>]*>([^<]+)</p>", c)
        price = re.search(r'tabular-nums">\s*([^<\s][^<]*?)\s*</span>', c)
        nums = re.findall(r"</svg>\s*([0-9,.]+[KkMm]?)\s*</span>", c)
        shop = re.findall(r"<p[^>]*>([^<]+)</p>", c)
        li_rows.append({"keyword": slug.replace("-", " "), "rank": rank, "listing_id": lid,
                        "title": html.unescape(title.group(1)).strip() if title else "NOT SHOWN",
                        "price": html.unescape(price.group(1)).strip() if price else "NOT SHOWN",
                        "favorites": num(nums[0]) if nums else "NOT SHOWN", "views": num(nums[1]) if len(nums) > 1 else "NOT SHOWN",
                        "shop": html.unescape(shop[-1]).strip() if len(shop) > 1 else "NOT SHOWN",
                        "url": f"https://www.etsy.com/listing/{lid}", "source_url": url, "fetched_at": ts, "fetch_route": "third_party:rankhero"})
for name, rows in (("etsy_rankhero_keywords_parsed.csv", kw_rows), ("etsy_rankhero_listings.csv", li_rows)):
    with open(os.path.join(REPO, "raw", name), "w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(kw_rows), len(li_rows)); print(kw_rows[0]); print(li_rows[0])
