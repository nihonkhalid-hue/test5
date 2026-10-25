"""Refetch a random 5% of master rows and compare key fields. Writes verification.csv."""
import csv, html, json, os, random, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

OUT = sys.argv[1]
VDIR = os.path.join(BASE, "raw", "verify"); os.makedirs(VDIR, exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(OUT, "master.csv"), encoding="utf-8")))
random.seed(20261025)
sample = random.sample(rows, max(1, round(len(rows) * 0.05)))
res = []


def num(x):
    try:
        return float(str(x).replace(",", "").replace("$", ""))
    except Exception:
        return None


def cmp(field, a, b, tol=0.0):
    a2, b2 = num(a), num(b)
    if a2 is None and b2 is None:
        return str(a).strip() == str(b).strip()
    if a2 is None or b2 is None:
        return False
    return abs(a2 - b2) <= tol * max(abs(a2), 1)


page_cache = {}


def get(site, url, gap=(6, 10)):
    if url in page_cache: return page_cache[url]
    fp = os.path.join(VDIR, re.sub(r"\W+", "_", url)[-120:] + ".html")
    if not (os.path.exists(fp) and os.path.getsize(fp) > 2000):  # reuse this verification pass's own re-fetch
        st, _ = fetch(site, url, fp, *gap)
    b = open(fp, encoding="utf-8", errors="ignore").read()
    page_cache[url] = b
    return b


blocked_sites = set()
for r in sample:
    m = r["marketplace"]; route = r["fetch_route"]
    out = {"marketplace": m, "title": r["title"][:80], "source_url": r["source_url"], "route": route}
    try:
        if m == "gumroad" and route.startswith("curl"):
            b = get("gumroad.com", r["source_url"])
            p = json.loads(html.unescape(re.search(r'data-page="([^"]+)"', b).group(1)))["props"]["product"]
            out.update(field="price|ratings_count|title", old=f"{r['price']}|{r['review_count']}",
                       new=f"{(p.get('price_cents') or 0)/100}|{(p.get('ratings') or {}).get('count')}",
                       match=cmp("p", r["price"], (p.get("price_cents") or 0) / 100) and cmp("r", r["review_count"], (p.get("ratings") or {}).get("count"))
                       and p.get("name", "").strip() == r["title"].strip())
        elif m == "etsy" and "rankhero" in route:
            kwd = re.search(r"rankhero_keywords=([^|;]+)", r["notes"]).group(1)
            slug = re.sub(r"[^a-z0-9]+", "-", kwd.lower()).strip("-")
            b = get("rankhero.com", f"https://www.rankhero.com/keywords/{slug}")
            lid = r["source_url"].rsplit("/", 1)[-1]
            c = re.search(r'<a href="https://www\.etsy\.com/listing/' + lid + r'"(.*?)</a>', b, re.S)
            if not c:
                out.update(field="listing present", old="present", new="absent (list rotated)", match=False)
            else:
                cc = html.unescape(c.group(1))
                nums = re.findall(r"</svg>\s*([0-9,.]+[KkM]?)\s*</span>", cc)
                pm = re.search(r"([$£€][0-9.,]+|\b[A-Z]{3} [0-9.,]+)", cc)
                price = re.sub(r"[^0-9.,]", "", pm.group(1)) if pm else ""
                out.update(field="price|favorites", old=f"{r['price']}|{r['favorites']}", new=f"{price}|{nums[0] if nums else ''}",
                           match=cmp("p", r["price"], price) and cmp("f", r["favorites"], nums[0] if nums else None))
        elif m == "teacherspayteachers":
            pg = 2 if int(r["rank_on_page"] or 1) > 24 else 1
            b = get("teacherspayteachers.com", "https://www.teacherspayteachers.com/browse?search=" + r["query"].replace(" ", "+") + ("&page=2" if pg == 2 else ""))
            path = r["source_url"].replace("https://www.teacherspayteachers.com", "")
            card = next((c for c in re.split(r'data-testid="ProductRow"', b)[1:] if path in c), None)
            if card is None:
                out.update(field="listing present", old="present", new="absent from page (rank moved / was page 2)", match=False)
            else:
                seg = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", card)))
                rv = re.search(r"based on ([0-9,]+) reviews?", seg); pr = re.search(r"(\$[0-9.]+) Original Price", seg)
                out.update(field="price|reviews", old=f"{r['price']}|{r['review_count']}",
                           new=f"{pr.group(1) if pr else ''}|{rv.group(1) if rv else ''}",
                           match=cmp("p", r["price"], pr.group(1) if pr else None) and (cmp("r", r["review_count"], rv.group(1) if rv else None) or (r["review_count"] in ("", "NOT SHOWN") and not rv)))
        elif m == "amazon":
            src = re.search(r"via (\S+)", r["notes"]).group(1)
            b = get("asinsight.com", src)
            asin = r["source_url"].rsplit("/", 1)[-1]
            tx = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", b, flags=re.S))))
            ms = re.search(re.escape(asin) + r" .{0,600}?([0-9,]+) Units Sold/mo", tx)
            out.update(field="monthly_sales_est", old=r["monthly_sales_est_thirdparty"], new=ms.group(1) if ms else "absent",
                       match=cmp("m", r["monthly_sales_est_thirdparty"], ms.group(1) if ms else None))
        elif m == "itch.io":
            out.update(field="-", old="", new="", match="")
            b = get("itch.io", "https://itch.io/search?q=" + r["query"].replace(" ", "+") + "&classification=assets")
            out.update(field="title present", old="present", new="present" if html.escape(r["title"])[:40] in b or r["title"][:40] in b else "absent", match=(r["title"][:40] in b or html.escape(r["title"])[:40] in b))
        else:
            out.update(field="-", old="", new="", match="NOT VERIFIABLE (websearch/blocked source)")
    except SiteBlocked as e:
        out.update(field="-", old="", new=str(e)[:80], match="BLOCKED")
    except StopMorocco:
        raise
    except Exception as e:
        out.update(field="-", old="", new="parse error " + str(e)[:60], match=False)
    out["checked_at"] = utcnow()
    res.append(out)
    print(out["marketplace"], out.get("match"), flush=True)

with open(os.path.join(OUT, "verification.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, ["marketplace", "title", "field", "old", "new", "match", "route", "source_url", "checked_at"])
    w.writeheader(); w.writerows(res)
checked = [x for x in res if x["match"] in (True, False)]
print("sample", len(res), "checked", len(checked), "mismatch", sum(1 for x in checked if x["match"] is False))
