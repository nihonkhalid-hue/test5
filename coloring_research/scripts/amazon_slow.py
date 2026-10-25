"""Single slow Amazon retry: 20-30 s between requests, stop for good at first CAPTCHA."""
import csv, html, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "amazon")
os.makedirs(os.path.join(RAW, "pages"), exist_ok=True)
NODE = "11357541011"  # Books > Crafts, Hobbies & Home > Coloring Books for Grown-Ups
rows, books = [], []


def T(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def parse_list(body, list_name, url):
    ts = utcnow()
    items = re.split(r'id="gridItemRoot"', body)[1:]
    for it in items:
        asin = re.search(r'/dp/([A-Z0-9]{10})', it)
        rank = re.search(r'zg-bdg-text">#(\d+)<', it)
        title = re.search(r'line-clamp-\d[^"]*">([^<]+)<', it)
        auth = re.search(r'class="a-size-small a-link-child">([^<]+)<', it) or \
            re.search(r'<div class="_cDEzb_p13n-sc-css-line-clamp-1_[^"]*">([^<]+)<', it)
        rating = re.search(r'a-icon-alt">([0-9.]+) out of 5', it)
        revs = re.search(r'a-size-small">([0-9,]+)</span>', it)
        price = re.search(r'(\$[0-9,]+\.\d\d)', it)
        fmt = re.search(r'a-size-small a-color-secondary a-text-normal">([^<]+)<', it)
        rows.append({"list": list_name, "rank": rank.group(1) if rank else "", "asin": asin.group(1) if asin else "",
                     "title": html.unescape(title.group(1)) if title else "NOT SHOWN",
                     "author": html.unescape(auth.group(1)) if auth else "NOT SHOWN",
                     "rating": rating.group(1) if rating else "NOT SHOWN",
                     "reviews": revs.group(1).replace(",", "") if revs else "NOT SHOWN",
                     "price": price.group(1) if price else "NOT SHOWN",
                     "format": fmt.group(1) if fmt else "", "fetched_at": ts, "source_url": url})
    return len(items)


def parse_search(body, q, url):
    ts = utcnow(); n = 0
    for blk in re.split(r'data-component-type="s-search-result"', body)[1:]:
        asin = re.search(r'data-asin="([A-Z0-9]{10})"', blk) or re.search(r'/dp/([A-Z0-9]{10})', blk)
        title = re.search(r'<h2[^>]*>(.*?)</h2>', blk, re.S)
        rating = re.search(r'([0-9.]+) out of 5 stars', blk)
        revs = re.search(r'aria-label="([0-9,.]+K?) ratings?"', blk) or re.search(r's-underline-text">\(?([0-9,.]+K?)\)?<', blk)
        price = re.search(r'a-offscreen">(\$[0-9,.]+)<', blk)
        n += 1
        rows.append({"list": "search:" + q, "rank": n, "asin": asin.group(1) if asin else "",
                     "title": T(title.group(1)) if title else "NOT SHOWN", "author": "NOT SHOWN",
                     "rating": rating.group(1) if rating else "NOT SHOWN",
                     "reviews": revs.group(1) if revs else "NOT SHOWN",
                     "price": price.group(1) if price else "NOT SHOWN", "format": "",
                     "fetched_at": ts, "source_url": url})
    return n


def parse_book(body, asin, url):
    t = T(body)
    g = lambda pat: (re.search(pat, t) or [None, "NOT SHOWN"])[1]
    bsr = re.findall(r"#([0-9,]+) in ([A-Z][^#(]{2,60}?)(?= \(| #|$)", g(r"Best Sellers Rank:?\s*(.{0,400})") or "")
    books.append({"asin": asin, "title": T((re.search(r'id="productTitle"[^>]*>(.*?)</span>', body, re.S) or [None, "NOT SHOWN"])[1]),
                  "publisher": g(r"Publisher\s*:?\s*‏?\s*:?\s*‎?\s*([^‏‎]{2,80}?)\s+(?:\(|Publication|Language)"),
                  "publication_date": g(r"Publication date\s*:?\s*‏?\s*:?\s*‎?\s*([A-Z][a-z]+ \d{1,2}, \d{4})"),
                  "pages": g(r"(?:Print length|Paperback)\s*:?\s*‏?\s*:?\s*‎?\s*([0-9,]+) pages"),
                  "dimensions": g(r"Dimensions\s*:?\s*‏?\s*:?\s*‎?\s*([0-9.]+ x [0-9.]+ x [0-9.]+ inches)"),
                  "bsr_raw": g(r"Best Sellers Rank:?\s*(.{0,300}?)(?:Customer Reviews|$)"),
                  "bsr_overall": bsr[0][0].replace(",", "") if bsr else "NOT SHOWN",
                  "rating": g(r"([0-9.]+) out of 5 stars"), "reviews": g(r"([0-9,]+) ratings"),
                  "price": g(r"(\$[0-9]+\.[0-9]{2})"),
                  "fetched_at": utcnow(), "source_url": url})


def save():
    with open(os.path.join(RAW, "amazon_lists.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, ["list", "rank", "asin", "title", "author", "rating", "reviews", "price", "format",
                               "fetched_at", "source_url"]); w.writeheader(); w.writerows(rows)
    if books:
        with open(os.path.join(RAW, "amazon_books.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, list(books[0].keys())); w.writeheader(); w.writerows(books)


def get(url, name):
    out = os.path.join(RAW, "pages", name)
    return fetch("amazon.com", url, out, 20, 30)[1]


def main():
    lists = [("bestsellers", f"https://www.amazon.com/gp/bestsellers/books/{NODE}"),
             ("new-releases", f"https://www.amazon.com/gp/new-releases/books/{NODE}"),
             ("movers-and-shakers", f"https://www.amazon.com/gp/movers-and-shakers/books/{NODE}"),
             ("most-wished-for", f"https://www.amazon.com/gp/most-wished-for/books/{NODE}")]
    subs = []
    for name, url in lists:
        for pg in (1, 2):
            u = url + ("?pg=2" if pg == 2 else "")
            body = get(u, f"{name}_{pg}.html")
            n = parse_list(body, name, u); print(name, pg, n, flush=True); save()
            if name == "bestsellers" and pg == 1:
                for h, txt in re.findall(r'href="(/[^"]*zgbs/books/(\d+))[^"]*"[^>]*>([^<]{3,80})<', body) and \
                        [(m[0], m[2]) for m in re.findall(r'href="(/[^"]*zgbs/books/(\d+))[^"]*"[^>]*>([^<]{3,80})<', body)]:
                    if NODE not in h and h not in [s[0] for s in subs]:
                        subs.append((h, html.unescape(txt)))
                print("links", subs[:30], flush=True)
    # children's coloring + subcategories of adult coloring (those appearing after the node in the tree)
    for q in ["anime coloring book", "kawaii coloring book", "cozy coloring book", "bold and easy coloring book",
              "japanese coloring book", "manga coloring book", "coloring book for kids"]:
        u = "https://www.amazon.com/s?" + urllib.parse.urlencode({"k": q, "i": "stripbooks"})
        body = get(u, "s_" + q.replace(" ", "_") + ".html")
        print("search", q, parse_search(body, q, u), flush=True); save()
    asins = []
    for r in rows:
        if r["asin"] and r["asin"] not in asins:
            asins.append(r["asin"])
    for a in asins[:120]:
        u = f"https://www.amazon.com/dp/{a}"
        body = get(u, f"dp_{a}.html"); parse_book(body, a, u); save(); print("dp", a, books[-1]["bsr_overall"], flush=True)


if __name__ == "__main__":
    try:
        main()
    except SiteBlocked as e:
        print("BLOCKED - stopping Amazon for good:", e)
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    save()
    print("DONE amazon rows", len(rows), "books", len(books))
