"""Etsy data via public third-party pages: RankHero keyword pages + FindNiche product pages."""
import csv, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "thirdparty")
OFFLINE = "offline" in sys.argv
os.makedirs(os.path.join(RAW, "rh"), exist_ok=True)
os.makedirs(os.path.join(RAW, "fn"), exist_ok=True)

SEED_KW = ["coloring pages", "coloring pages printable", "adult coloring pages", "coloring book pdf",
           "bold and easy coloring", "cozy coloring pages", "kawaii coloring pages", "anime coloring pages",
           "manga coloring", "japanese coloring pages", "cute coloring pages", "mandala coloring",
           "kids coloring pages", "christmas coloring pages", "halloween coloring pages",
           "spooky cute coloring", "fantasy coloring", "cottagecore coloring", "grayscale coloring",
           "coloring bundle", "procreate coloring pages", "goodnotes coloring", "coloring book",
           "adult coloring book", "coloring page", "coloring sheets", "printable coloring pages",
           "anime coloring book", "kawaii coloring book", "cozy coloring book", "bold and easy coloring book",
           "cute coloring book", "christmas coloring book", "halloween coloring book", "mandala coloring pages",
           "grayscale coloring pages", "fairy coloring pages", "mermaid coloring pages", "cat coloring pages",
           "dragon coloring pages", "mushroom coloring pages", "horror coloring pages", "gothic coloring pages",
           "floral coloring pages", "botanical coloring pages", "animal coloring pages",
           "color by number", "coloring book for adults", "retro coloring pages", "y2k coloring pages",
           "chibi coloring pages", "japan coloring book", "fall coloring pages", "thanksgiving coloring pages",
           "valentines coloring pages", "easter coloring pages", "summer coloring pages",
           "cozy girl coloring", "kawaii coloring", "coloring pages for adults", "stress relief coloring",
           "witch coloring pages", "spooky coloring pages", "christmas coloring sheets", "mandala coloring book",
           "bible coloring pages", "quote coloring pages", "procreate coloring", "digital coloring pages",
           "coloring bookmarks", "ocean coloring pages", "princess coloring pages", "unicorn coloring pages",
           "dinosaur coloring pages", "food coloring pages", "kawaii food coloring", "cozy cottage coloring",
           "dark fantasy coloring", "victorian coloring pages", "anime girl coloring", "gaming coloring pages",
           "pixel art coloring", "frog coloring pages", "axolotl coloring pages", "capybara coloring pages"]


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def num(s):
    s = (s or "").replace(",", "").strip()
    m = re.match(r"([0-9.]+)\s*([KkMm]?)", s)
    if not m: return ""
    v = float(m.group(1)) * {"": 1, "k": 1e3, "m": 1e6}[m.group(2).lower()]
    return int(v)


def rankhero():
    kw_rows, li_rows, seen = [], [], set()
    queue = list(SEED_KW)
    while queue and len(seen) < 110:
        kw = queue.pop(0)
        slug = re.sub(r"[^a-z0-9]+", "-", kw.lower()).strip("-")
        if slug in seen: continue
        seen.add(slug)
        url = f"https://www.rankhero.com/keywords/{slug}"
        out = os.path.join(RAW, "rh", slug + ".html")
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            status, b = "200", open(out, encoding="utf-8", errors="ignore").read()
        elif OFFLINE:
            continue
        else:
            status, b = fetch("rankhero.com", url, out, 6, 9)
        if status != "200" or "Keyword overview" not in b:
            print("rh miss", slug, status, flush=True); continue
        t = text(b)
        import datetime as _dt
        ts = _dt.datetime.fromtimestamp(os.path.getmtime(out), _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        g = lambda p: (re.search(p, t) or [None, ""])[1]
        months = re.findall(r"((?:January|February|March|April|May|June|July|August|September|October|November|December) 20\d\d) ([0-9,]+)", t)
        kw_rows.append({"keyword": kw, "updated": g(r"Updated ([A-Z][a-z]+ \d+, \d{4})"),
                        "monthly_searches": num(g(r"Monthly search volume ([0-9,]+)")),
                        "etsy_listings": num(g(r"with ([0-9,]+) listings targeting")),
                        "competition": num(g(r"Competition ([0-9,]+)")),
                        "trend_sentence": g(r"(Search interest (?:dropped|rose|grew|increased|decreased|fell)[^.]*\.)"),
                        "median_price": g(r"most priced around (\$[0-9.]+)") or g(r"median sits at (\$[0-9.]+)"),
                        "price_range": g(r"typically sell between (\$[0-9.]+ and \$[0-9.]+)"),
                        "difficulty": g(r"Keyword difficulty ([0-9]+) ?/100"),
                        "cpc": g(r"Cost per click (\$[0-9.]+)"),
                        "us_share": g(r"accounts for (\d+)% of searches"),
                        "monthly_series": json.dumps([(m, num(v)) for m, v in months[:12]]),
                        "source_url": url, "fetched_at": ts, "fetch_route": "third_party"})
        i = b.find("Top Etsy listings for")
        for rank, card in enumerate(re.findall(r'<a href="https://www\.etsy\.com/listing/(\d+)"(.*?)</a>', b[i:], re.S), 1):
            lid, c = card
            c = html.unescape(c)
            title = re.search(r"<p[^>]*>([^<]+)</p>", c)
            price = re.search(r"([$£€][0-9.,]+|\b[A-Z]{3} [0-9.,]+)", c)
            nums = re.findall(r"</svg>\s*([0-9,.]+[KkMm]?)\s*</span>", c)
            shop = re.findall(r"<p[^>]*>([^<]+)</p>", c)
            li_rows.append({"keyword": kw, "rank": rank, "listing_id": lid,
                            "title": html.unescape(title.group(1)).strip() if title else "NOT SHOWN",  # c already unescaped once
                            "price": price.group(1) if price else "NOT SHOWN",
                            "favorites": num(nums[0]) if len(nums) > 0 else "NOT SHOWN",
                            "views": num(nums[1]) if len(nums) > 1 else "NOT SHOWN",
                            "shop": html.unescape(shop[-1]).strip() if len(shop) > 1 else "NOT SHOWN",
                            "source_url": url, "fetched_at": ts, "fetch_route": "third_party"})
        for rel in re.findall(r'href="/keywords/([a-z0-9-]+)"', b):
            if re.search(r"colou?r|mandala|kawaii|anime|manga", rel) and rel not in seen:
                queue.append(rel.replace("-", " "))
        print("rh", slug, len(months), "listings", rank if 'rank' in dir() else 0, flush=True)
        for name, rows in (("rankhero_keywords.csv", kw_rows), ("rankhero_listings.csv", li_rows)):
            if rows:
                with open(os.path.join(RAW, name), "w", newline="") as f:
                    w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def findniche(seeds, cap=160):
    rows, seen, queue = [], set(), list(seeds)
    while queue and len(seen) < cap:
        path = queue.pop(0)
        if path in seen: continue
        seen.add(path)
        url = "https://findniche.com" + path
        out = os.path.join(RAW, "fn", path.split("/")[-1][-60:] + ".html")
        status, b = fetch("findniche.com", url, out, 6, 9)
        t = text(b); ts = utcnow()
        g = lambda p: (re.search(p, t) or [None, "NOT SHOWN"])[1]
        lid = re.search(r"-(\d{6,})$", path)
        tags = g(r"Released \d{4}-\d\d-\d\d (.*?) Open Product Page")
        rows.append({"listing_id": lid.group(1) if lid else "", "title": g(r"^\s*(.*?) — Etsy Product"),
                     "total_sales": num(g(r"([0-9,.]+[KkM]?) Total Sales")), "total_revenue": g(r"(\$[0-9,.]+[KkM]?) Total Revenue"),
                     "favorites": num(g(r"([0-9,.]+[KkM]?) Favorites")), "reviews": num(g(r"([0-9,.]+[KkM]?) Reviews")),
                     "monthly_sales": num(g(r"Monthly Sales ↑?([0-9,.]+[KkM]?)")),
                     "bestseller": "yes" if "Best Seller" in t[:3000] else "no",
                     "price": g(r"Price ([$£€][0-9.,]+)"), "shop": g(r"Store (\S+) Store Rating"),
                     "shop_rating_count": g(r"Store Rating ([0-9,]+)"), "released": g(r"Released (\d{4}-\d\d-\d\d)"),
                     "tags": tags, "source_url": url, "fetched_at": ts, "fetch_route": "third_party"})
        for rel in re.findall(r'href="(/etsy-product/[a-z0-9-]+-\d{6,})"', b):
            if re.search(r"colou?r|mandala|coloring", rel) and rel not in seen:
                queue.append(rel)
        print("fn", path[-50:], rows[-1]["total_sales"], "queue", len(queue), flush=True)
        with open(os.path.join(RAW, "findniche_listings.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    try:
        if "rh" in sys.argv:
            rankhero()
        if "fn" in sys.argv:
            seeds = [l.strip() for l in open(os.path.join(RAW, "fn_seeds.txt")) if l.strip()]
            findniche(seeds)
    except SiteBlocked as e:
        print("BLOCKED", e)
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    print("DONE thirdparty", sys.argv[1:])
