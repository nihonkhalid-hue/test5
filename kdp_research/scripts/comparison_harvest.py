"""Comparison marketplaces + demand signals. One site per process: python3 comparison_harvest.py <site>.
Read-only, paced (6-10 s; reddit 30-40 s). Stops a site at first block."""
import csv, html, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
RAWR = os.path.join(REPO, "raw"); P = os.path.join(BASE, "pages")


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()


def save(name, rows):
    if rows:
        keys = []
        for r in rows:
            for k in r:
                if k not in keys: keys.append(k)
        with open(os.path.join(RAWR, name), "w", newline="") as f:
            w = csv.DictWriter(f, keys, restval=""); w.writeheader(); w.writerows(rows)


def gumroad():
    d = os.path.join(P, "gumroad"); os.makedirs(d, exist_ok=True)
    Q = ["journal", "guided journal", "gratitude journal", "prayer journal", "shadow work journal", "planner",
         "2027 planner", "digital planner", "budget planner", "reading journal", "workbook", "kids workbook",
         "handwriting practice", "tracing worksheets", "puzzle book", "word search", "sudoku", "crossword",
         "activity book", "coloring book", "low content", "kdp interior", "kdp template", "notebook",
         "sketchbook", "recipe book", "password log", "anime journal", "kawaii planner", "manga drawing",
         "how to draw anime", "japanese journal", "romance novel", "ebook", "self help ebook", "cookbook"]
    rows = []
    for q in Q:
        for sort, pages in [("default", 2), ("most_reviewed", 1), ("newest", 1)]:
            frm = 0
            for p in range(pages):
                prm = {"query": q, "from": frm} | ({"sort": sort} if sort != "default" else {})
                url = "https://gumroad.com/products/search?" + urllib.parse.urlencode(prm)
                fp = os.path.join(d, re.sub(r"\W+", "_", f"{q}_{sort}_{frm}") + ".json")
                st, _ = fetch("gumroad.com", url, fp, 6, 10, accept="application/json")
                try:
                    js = json.load(open(fp))
                except Exception:
                    print("non-json", url, st); break
                prods = js.get("products") or []; ts = utcnow()
                for i, pr in enumerate(prods, 1):
                    rows.append({"query": q, "sort": sort, "rank_on_page": frm + i, "product_id": pr.get("id"),
                                 "title": pr.get("name"), "creator": (pr.get("seller") or {}).get("name"),
                                 "price_cents": pr.get("price_cents"), "currency": pr.get("currency_code"),
                                 "pay_what_you_want": pr.get("is_pay_what_you_want"),
                                 "rating": (pr.get("ratings") or {}).get("average", "NOT SHOWN"),
                                 "rating_count": (pr.get("ratings") or {}).get("count", "NOT SHOWN"),
                                 "native_type": pr.get("native_type"), "url": (pr.get("url") or "").split("?")[0],
                                 "total_results": js.get("total"), "fetched_at": ts, "source_url": url, "fetch_route": "curl"})
                print("gum", q, sort, frm, len(prods), flush=True)
                save("gumroad.csv", rows)
                if not prods: break
                frm += len(prods)


def tpt():
    d = os.path.join(P, "tpt"); os.makedirs(d, exist_ok=True)
    Q = ["handwriting practice", "tracing worksheets", "preschool workbook", "kindergarten workbook",
         "word search", "sudoku for kids", "mazes", "dot to dot", "activity book", "journal prompts",
         "reading log", "writing journal", "math workbook", "phonics workbook", "summer workbook",
         "kawaii", "anime", "japan", "planner", "coloring book"]
    rows = []
    for q in Q:
        for page in (1, 2):
            url = "https://www.teacherspayteachers.com/browse?" + urllib.parse.urlencode({"search": q} | ({"page": page} if page > 1 else {}))
            fp = os.path.join(d, f"tpt_{q.replace(' ', '_')}_{page}.html")
            st, _ = fetch("teacherspayteachers.com", url, fp, 6, 10)
            b = open(fp, encoding="utf-8", errors="ignore").read()
            cards = re.split(r'data-testid="ProductRow"', b)[1:]; ts = utcnow()
            for i, c in enumerate(cards, 1):
                link = re.search(r'href="(/Product/[^"]+)"', c); t = text("<x " + c)
                rows.append({"query": q, "page": page, "rank": (page - 1) * len(cards) + i,
                             "title": t.split(" Created by ")[0][:250] if " Created by " in t else "NOT SHOWN",
                             "seller": text((re.search(r'data-testid="prc-seller-byline"[^>]*>(.*?)</(?:div|span|p)>', c, re.S) or [None, "NOT SHOWN"])[1]).replace("Created by", "").strip()[:80],
                             "price": (re.search(r"(\$[0-9.]+) Original Price", t) or re.search(r"(\$[0-9.]+|Free)", t) or [None, "NOT SHOWN"])[1],
                             "rating": (re.search(r"Rated ([0-9.]+) out of 5", t) or [None, "NOT SHOWN"])[1],
                             "reviews": (re.search(r"based on ([0-9,]+) reviews?", t) or [None, "NOT SHOWN"])[1].replace(",", ""),
                             "grades": (re.search(r"(PreK - \d+ ?\w*|K - \d+ ?\w*|\d+(?:st|nd|rd|th) - \d+ ?\w*|Not Grade Specific)", t) or [None, "NOT SHOWN"])[1],
                             "url": "https://www.teacherspayteachers.com" + link.group(1) if link else "",
                             "fetched_at": ts, "source_url": url, "fetch_route": "curl"})
            print("tpt", q, page, len(cards), flush=True); save("teacherspayteachers.csv", rows)
            if not cards: break


def rankhero():
    d = os.path.join(P, "rankhero"); os.makedirs(d, exist_ok=True)
    if len(sys.argv) > 2:
        Q = sys.argv[2:]
        return _rh(d, Q, append=True)
    Q = ["printable-planner", "digital-planner", "2027-planner", "budget-planner", "gratitude-journal",
         "prayer-journal", "reading-journal", "journal-prompts", "word-search-printable", "sudoku-printable",
         "puzzle-book", "activity-book", "kids-activity-book", "handwriting-worksheets", "tracing-worksheets",
         "recipe-book", "password-log", "kdp-interior", "kdp-template", "low-content-book", "coloring-book",
         "kawaii-planner", "anime-planner", "journal", "planner", "sticker-book", "manga-template",
         "habit-tracker", "shadow-work-journal", "wedding-planner", "teacher-planner", "self-care-journal"]
    _rh(d, Q)


def _rh(d, Q, append=False):
    kw = list(csv.DictReader(open(os.path.join(RAWR, "etsy_rankhero_keywords.csv")))) if append else []
    lst = list(csv.DictReader(open(os.path.join(RAWR, "etsy_rankhero_listing_links.csv")))) if append else []
    for q in Q:
        if os.path.exists(os.path.join(d, q + ".html")): continue
        url = f"https://www.rankhero.com/keywords/{q}"
        fp = os.path.join(d, q + ".html")
        st, _ = fetch("rankhero.com", url, fp, 7, 11)
        b = open(fp, encoding="utf-8", errors="ignore").read(); t = text(b); ts = utcnow()
        g = lambda p: (re.search(p, t, re.I) or [None, "NOT SHOWN"])[1]
        kw.append({"keyword": q.replace("-", " "), "http": st, "search_volume": g(r"([0-9,.]+K?) (?:monthly )?searches"),
                   "competition_listings": g(r"([0-9,.]+K?) (?:competing )?(?:listings|results)"),
                   "page_text_head": t[:600], "fetched_at": ts, "source_url": url, "fetch_route": "third_party:rankhero"})
        for m in re.finditer(r'href="(https://www\.etsy\.com/listing/(\d+)[^"]*)"', b):
            lst.append({"keyword": q.replace("-", " "), "listing_id": m.group(2), "url": m.group(1).split("?")[0],
                        "fetched_at": ts, "source_url": url, "fetch_route": "third_party:rankhero"})
        print("rh", q, st, flush=True)
        save("etsy_rankhero_keywords.csv", kw); save("etsy_rankhero_listing_links.csv", lst)


def reddit():
    d = os.path.join(P, "reddit"); os.makedirs(d, exist_ok=True)
    plan = [("selfpublish", "low content"), ("selfpublish", "KDP niche"), ("selfpublish", "puzzle book"),
            ("selfpublish", "coloring book"), ("selfpublish", "journal"), ("KDP", "niche"), ("KDP", "sales"),
            ("KDP", "low content"), ("kdp_lowcontent", "niche"), ("kdp_lowcontent", "sales"),
            ("coloringbooks", "favorite"), ("selfpublish", "romance"), ("KDP", "coloring"), ("KDP", "planner")]
    rows = list(csv.DictReader(open(os.path.join(RAWR, "demand_reddit_rss.csv")))) if os.path.exists(os.path.join(RAWR, "demand_reddit_rss.csv")) else []
    done = {(r["subreddit"], r["term"]) for r in rows}
    gap = (60, 90) if rows else (30, 40)
    for sub, term in plan:
        if (sub, term) in done: continue
        url = f"https://www.reddit.com/r/{sub}/search.rss?q={urllib.parse.quote(term)}&restrict_sr=on&sort=top&t=year"
        fp = os.path.join(d, re.sub(r"\W+", "_", f"{sub}_{term}") + ".xml")
        st, body = fetch("reddit.com", url, fp, *gap, accept="application/atom+xml")
        entries = re.findall(r"<entry>(.*?)</entry>", body, re.S); ts = utcnow()
        for i, e in enumerate(entries, 1):
            g = lambda tag: html.unescape((re.search(f"<{tag}[^>]*>(.*?)</{tag}>", e, re.S) or [None, ""])[1])
            link = re.search(r'<link href="([^"]+)"', e)
            rows.append({"subreddit": sub, "term": term, "rank": i, "title": g("title"),
                         "published": g("published") or g("updated"), "link": link.group(1) if link else "",
                         "fetched_at": ts, "source_url": url, "fetch_route": "curl", "signal_type": "demand"})
        print("rd", sub, term, st, len(entries), flush=True); save("demand_reddit_rss.csv", rows)


def goodreads():
    d = os.path.join(P, "goodreads"); os.makedirs(d, exist_ok=True)
    L = ["https://www.goodreads.com/shelf/show/romantasy", "https://www.goodreads.com/shelf/show/dark-romance",
         "https://www.goodreads.com/shelf/show/cozy-mystery", "https://www.goodreads.com/shelf/show/self-published",
         "https://www.goodreads.com/shelf/show/kindle-unlimited", "https://www.goodreads.com/shelf/show/self-help",
         "https://www.goodreads.com/shelf/show/cozy-fantasy", "https://www.goodreads.com/shelf/show/manga",
         "https://www.goodreads.com/shelf/show/litrpg", "https://www.goodreads.com/shelf/show/reverse-harem"]
    rows = []
    for url in L:
        fp = os.path.join(d, url.split("/")[-1] + ".html")
        st, _ = fetch("goodreads.com", url, fp, 8, 12)
        b = open(fp, encoding="utf-8", errors="ignore").read(); ts = utcnow()
        for i, blk in enumerate(re.split(r'class="elementList"', b)[1:], 1):
            t = text("<x " + blk)
            title = re.search(r'class="bookTitle"[^>]*>(.*?)</a>', blk, re.S)
            auth = re.search(r'class="authorName"[^>]*><span[^>]*>(.*?)</span>', blk, re.S)
            rows.append({"shelf": url.split("/")[-1], "rank": i, "title": text(title.group(1)) if title else "NOT SHOWN",
                         "author": text(auth.group(1)) if auth else "NOT SHOWN",
                         "avg_rating": (re.search(r"avg rating ([0-9.]+)", t) or [None, "NOT SHOWN"])[1],
                         "ratings": (re.search(r"([0-9,]+) ratings", t) or [None, "NOT SHOWN"])[1].replace(",", ""),
                         "published_year": (re.search(r"published (\d{4})", t) or [None, "NOT SHOWN"])[1],
                         "fetched_at": ts, "source_url": url, "fetch_route": "curl"})
        print("gr", url, st, flush=True); save("goodreads_shelves.csv", rows)


if __name__ == "__main__":
    fn = {"gumroad": gumroad, "tpt": tpt, "rankhero": rankhero, "reddit": reddit, "goodreads": goodreads}[sys.argv[1]]
    try:
        fn()
    except SiteBlocked as e:
        print("BLOCKED", e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE", sys.argv[1], flush=True)
