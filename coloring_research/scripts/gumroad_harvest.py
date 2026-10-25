"""Gumroad tier A (search JSON) + tier B (product pages). Read-only, paced."""
import csv, html, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "gumroad")
os.makedirs(os.path.join(RAW, "pages"), exist_ok=True)
QUERIES = ["coloring pages", "coloring book", "anime coloring", "kawaii coloring", "procreate coloring",
           "adult coloring", "bold and easy coloring", "cozy coloring", "mandala coloring",
           "kids coloring pages", "christmas coloring", "halloween coloring", "grayscale coloring",
           "manga coloring", "coloring bundle", "goodnotes coloring", "fantasy coloring",
           "cottagecore coloring", "japanese coloring", "cute coloring pages", "spooky coloring",
           "coloring pages commercial use"]
SORTS = [("default", 3), ("most_reviewed", 3), ("newest", 1), ("hot_and_new", 1)]

rows, seen_pages = [], set()
FIELDS = ["query", "sort", "rank_on_page", "page_from", "product_id", "title", "creator", "price_cents",
          "currency", "pay_what_you_want", "rating", "rating_count", "native_type", "url",
          "fetched_at", "source_url"]


def harvest():
    for q in QUERIES:
        for sort, pages in SORTS:
            frm = 0
            for p in range(pages):
                params = {"query": q, "from": frm}
                if sort != "default":
                    params["sort"] = sort
                url = "https://gumroad.com/products/search?" + urllib.parse.urlencode(params)
                out = os.path.join(RAW, "pages", re.sub(r"\W+", "_", f"{q}_{sort}_{frm}") + ".json")
                status, body = fetch("gumroad.com", url, out, 6, 10, accept="application/json")
                try:
                    d = json.loads(body)
                except Exception:
                    print("non-json", url, status); break
                prods = d.get("products") or []
                ts = utcnow()
                for i, pr in enumerate(prods, 1):
                    rows.append({"query": q, "sort": sort, "rank_on_page": frm + i, "page_from": frm,
                                 "product_id": pr.get("id"), "title": pr.get("name"),
                                 "creator": (pr.get("seller") or {}).get("name"),
                                 "price_cents": pr.get("price_cents"), "currency": pr.get("currency_code"),
                                 "pay_what_you_want": pr.get("is_pay_what_you_want"),
                                 "rating": (pr.get("ratings") or {}).get("average"),
                                 "rating_count": (pr.get("ratings") or {}).get("count"),
                                 "native_type": pr.get("native_type"),
                                 "url": (pr.get("url") or "").split("?")[0],
                                 "fetched_at": ts, "source_url": url})
                print(q, sort, frm, "->", len(prods), "total", d.get("total"), flush=True)
                if p == 0 and sort == "default":
                    with open(os.path.join(RAW, "tags_" + re.sub(r"\W+", "_", q) + ".json"), "w") as f:
                        json.dump({"total": d.get("total"), "tags": d.get("tags_data"),
                                   "filetypes": d.get("filetypes_data")}, f)
                if len(prods) == 0:
                    break
                frm += len(prods)
        write_a()


def write_a():
    with open(os.path.join(RAW, "gumroad_tierA.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)


def tier_b(limit):
    import collections
    a = list(csv.DictReader(open(os.path.join(RAW, "gumroad_tierA.csv"))))
    best = collections.OrderedDict()
    colorish = re.compile(r"colou?r", re.I)
    for r in sorted(a, key=lambda r: -int(r["rating_count"] or 0)):
        if colorish.search(r["title"] or "") and r["url"] and r["url"] not in best:
            best[r["url"]] = r
    newest = [r for r in a if r["sort"] in ("newest", "hot_and_new") and colorish.search(r["title"] or "")]
    order = list(best.values())[: int(limit * 0.75)]
    for r in newest:
        if len(order) >= limit: break
        if r["url"] not in [o["url"] for o in order]:
            order.append(r)
    outp = os.path.join(RAW, "gumroad_tierB.csv")
    done = set()
    if os.path.exists(outp):
        done = {r["url"] for r in csv.DictReader(open(outp))}
    new = not os.path.exists(outp)
    with open(outp, "a", newline="") as f:
        w = csv.DictWriter(f, ["url", "title", "creator", "price_cents", "currency", "pwyw_min_cents",
                               "rating", "rating_count", "sales_count", "attributes", "page_count_attr",
                               "page_count_text", "formats_text", "summary", "native_type", "is_bundle",
                               "fetched_at"])
        if new: w.writeheader()
        for r in order:
            if r["url"] in done: continue
            out = os.path.join(RAW, "pages", "prod_" + re.sub(r"\W+", "_", r["url"])[-80:] + ".html")
            status, body = fetch("gumroad.com", r["url"], out, 6, 10)
            m = re.search(r'data-page="([^"]+)"', body)
            if not m:
                print("no data-page", r["url"], status); continue
            p = json.loads(html.unescape(m.group(1)))["props"].get("product") or {}
            attrs = p.get("attributes") or []
            pc = next((a["value"] for a in attrs if re.search(r"page|sheet|design|illustr", a.get("name", ""), re.I)), "")
            desc = re.sub(r"<[^>]+>", " ", p.get("description_html") or "") + " " + (p.get("summary") or "") + " " + (p.get("name") or "")
            pt = re.findall(r"(\d{1,4})\+?\s*(?:unique\s+|hand[- ]drawn\s+|printable\s+|high[- ]quality\s+)?(?:coloring\s+|colouring\s+)?(?:pages|sheets|designs|illustrations)", desc, re.I)
            fm = sorted(set(x.upper() for x in re.findall(r"\b(PDF|PNG|JPE?G|SVG|Procreate|GoodNotes|ZIP|brushset)\b", desc, re.I)))
            pwyw = p.get("pwyw") or {}
            w.writerow({"url": r["url"], "title": p.get("name"), "creator": (p.get("seller") or {}).get("name"),
                        "price_cents": p.get("price_cents"), "currency": p.get("currency_code"),
                        "pwyw_min_cents": pwyw.get("suggested_price_cents") if isinstance(pwyw, dict) else "",
                        "rating": (p.get("ratings") or {}).get("average"),
                        "rating_count": (p.get("ratings") or {}).get("count"),
                        "sales_count": p.get("sales_count") if p.get("sales_count") is not None else "NOT SHOWN",
                        "attributes": json.dumps(attrs)[:500], "page_count_attr": pc,
                        "page_count_text": pt[0] if pt else "", "formats_text": "|".join(fm),
                        "summary": (p.get("summary") or "")[:300], "native_type": p.get("native_type"),
                        "is_bundle": bool(p.get("bundle_products")) or p.get("native_type") == "bundle",
                        "fetched_at": utcnow()})
            f.flush()
            print("B", r["url"], p.get("sales_count"), flush=True)


if __name__ == "__main__":
    try:
        if "b" not in sys.argv:
            harvest()
        tier_b(int(sys.argv[-1]) if sys.argv[-1].isdigit() else 220)
    except SiteBlocked as e:
        write_a() if rows else None
        print("BLOCKED", e)
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    print("DONE gumroad", len(rows))
