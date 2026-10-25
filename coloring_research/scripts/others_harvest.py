"""Teachers Pay Teachers search pages + itch.io + Creative Market probes. Read-only, paced."""
import csv, html, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "others")
os.makedirs(RAW, exist_ok=True)


def text(b):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", b, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()


def save(name, rows):
    if rows:
        with open(os.path.join(RAW, name), "w", newline="") as f:
            w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def tpt():
    rows = []
    for q in ["coloring pages", "kawaii coloring pages", "anime coloring pages", "halloween coloring pages",
              "christmas coloring pages", "mandala coloring pages", "cute coloring pages", "japan coloring pages",
              "fall coloring pages", "coloring book", "color by number", "bold and easy coloring"]:
        for page in (1, 2):
            url = "https://www.teacherspayteachers.com/browse?" + urllib.parse.urlencode(
                {"search": q} | ({"page": page} if page > 1 else {}))
            try:
                fp = os.path.join(RAW, f"tpt_{q.replace(' ', '_')}_{page}.html")
                if os.path.exists(fp) and os.path.getsize(fp) > 100000:
                    b = open(fp, encoding="utf-8", errors="ignore").read()
                else:
                    status, b = fetch("teacherspayteachers.com", url, fp, 6, 10)
                    b = open(fp, encoding="utf-8", errors="ignore").read()
            except SiteBlocked as e:
                print("BLOCKED", e, flush=True); save("tpt.csv", rows); return
            cards = re.split(r'data-testid="ProductRow"', b)[1:]
            ts = utcnow()
            for i, c in enumerate(cards, 1):
                link = re.search(r'href="(/Product/[^"]+)"', c)
                t = text("<x " + c)
                title = re.search(r'<a [^>]*href="/Product/[^"]+"[^>]*>(.*?)</a>', c, re.S)
                rows.append({"query": q, "page": page, "rank": (page - 1) * len(cards) + i,
                             "title": t.split(" Created by ")[0][:250] if " Created by " in t else "NOT SHOWN",
                             "seller": text((re.search(r'data-testid="prc-seller-byline"[^>]*>(.*?)</(?:div|span|p)>', c, re.S) or [None, "NOT SHOWN"])[1]).replace("Created by", "").strip()[:80],
                             "price": (re.search(r"(\$[0-9.]+) Original Price", t) or re.search(r"(\$[0-9.]+|Free)", t) or [None, "NOT SHOWN"])[1],
                             "rating": (re.search(r"Rated ([0-9.]+) out of 5", t) or [None, "NOT SHOWN"])[1],
                             "reviews": (re.search(r"based on ([0-9,]+) reviews?", t) or [None, "NOT SHOWN"])[1].replace(",", ""),
                             "grades": (re.search(r"(PreK - \d+ ?\w*|K - \d+ ?\w*|\d+(?:st|nd|rd|th) - \d+ ?\w*|Not Grade Specific)", t) or [None, ""])[1],
                             "url": "https://www.teacherspayteachers.com" + link.group(1) if link else "",
                             "fetched_at": ts, "source_url": url, "fetch_route": "curl"})
            print("tpt", q, page, len(cards), flush=True)
            save("tpt.csv", rows)
            if not cards: break


def itch():
    rows = []
    for q in ["coloring book", "anime coloring", "coloring pages"]:
        url = "https://itch.io/search?" + urllib.parse.urlencode({"q": q, "classification": "assets"})
        try:
            status, b = fetch("itch.io", url, os.path.join(RAW, f"itch_{q.replace(' ', '_')}.html"), 6, 10)
        except SiteBlocked as e:
            print("BLOCKED", e); break
        ts = utcnow()
        for i, c in enumerate(re.split(r'class="game_cell has_cover', b)[1:], 1):
            title = re.search(r'class="title game_link"[^>]*>([^<]+)<', c)
            link = re.search(r'href="(https://[^"]+\.itch\.io/[^"]+)"', c)
            price = re.search(r'class="price_value">([^<]+)<', c)
            author = re.search(r'class="game_author"><a[^>]*>([^<]+)<', c)
            rating = re.search(r'title="Rated ([0-9.]+) out of 5 stars"', c)
            rc = re.search(r'class="rating_count"[^>]*>\(?([0-9,]+)', c)
            rows.append({"query": q, "rank": i, "title": html.unescape(title.group(1)) if title else "NOT SHOWN",
                         "seller": html.unescape(author.group(1)) if author else "NOT SHOWN",
                         "price": price.group(1) if price else "free/PWYW or NOT SHOWN",
                         "rating": rating.group(1) if rating else "NOT SHOWN",
                         "reviews": rc.group(1).replace(",", "") if rc else "NOT SHOWN",
                         "url": link.group(1) if link else "", "fetched_at": ts, "source_url": url, "fetch_route": "curl"})
        print("itch", q, status, flush=True)
        save("itch.csv", rows)


def creativemarket():
    url = "https://creativemarket.com/search?q=coloring%20pages"
    try:
        status, b = fetch("creativemarket.com", url, os.path.join(RAW, "cm_probe.html"), 6, 10)
        print("creativemarket", status, len(b), flush=True)
    except SiteBlocked as e:
        print("BLOCKED", e, flush=True)


if __name__ == "__main__":
    try:
        tpt(); itch(); creativemarket()
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    print("DONE others")
