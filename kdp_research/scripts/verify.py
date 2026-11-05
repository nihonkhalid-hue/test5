"""Verification: pick a random 5% of master rows (seed 42), then
 (1) re-parse the ORIGINAL saved page and compare with master  -> pipeline/verifier-bug rate
 (2) re-fetch the live page now, parse it the same way, compare -> real drift rate.
Amazon-direct rows cannot be re-fetched (Amazon blocked); they are only re-parsed."""
import csv, json, os, random, re, sys, collections, html
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
import profitable_harvest as PH
csv.field_size_limit(10 ** 9)
NS = "NOT SHOWN"
M = list(csv.DictReader(open(os.path.join(REPO, "master.csv"))))
random.seed(42)
S = random.sample(M, max(1, int(len(M) * 0.05)))
VD = os.path.join(BASE, "pages", "verify"); os.makedirs(VD, exist_ok=True)


def num(x):
    try: return float(str(x).replace(",", "").replace("$", ""))
    except Exception: return None


def same(a, b):
    na, nb = num(a), num(b)
    if na is not None and nb is not None: return abs(na - nb) < 0.011
    return str(a).strip() == str(b).strip()


def prof_lookup(fp, pid):
    try:
        _, data, _ = PH.parse(fp)
    except Exception:
        return None
    for b in data:
        if b.get("asin") == pid:
            return {"price_usd_est": round(b["priceUsd"] / 100, 2) if b.get("priceUsd") is not None else NS, "review_count": b.get("ratingCount"), "rating": b.get("rating"), "bsr": b.get("bsrTop")}
    return None


def gum_lookup(fp, pid):
    try: d = json.load(open(fp))
    except Exception: return None
    for p in d.get("products") or []:
        if p.get("id") == pid:
            r = p.get("ratings") or {}
            return {"price": f"{p['price_cents']/100:.2f}" if p.get("price_cents") is not None else NS, "review_count": r.get("count", NS), "rating": r.get("average", NS)}
    return None


def asi_lookup(fp, pid, url):
    import asinsight_harvest as A
    slug = url.rstrip("/").split("/")[-1]
    for r in A.parse(fp, slug, url, ""):
        if r["asin"] == pid:
            return {"monthly_sales_est_thirdparty": r["monthly_sales_est_thirdparty"], "rating": r["rating"]}
    return None


def tpt_lookup(fp, url_prod):
    b = open(fp, encoding="utf-8", errors="ignore").read()
    path = url_prod.replace("https://www.teacherspayteachers.com", "")
    for c in re.split(r'data-testid="ProductRow"', b)[1:]:
        if path in c:
            t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c)))
            rv = re.search(r"based on ([0-9,]+) reviews?", t); ra = re.search(r"Rated ([0-9.]+) out of 5", t)
            return {"review_count": rv.group(1).replace(",", "") if rv else NS, "rating": ra.group(1) if ra else NS}
    return None


RAWA = {}
for x in csv.DictReader(open(os.path.join(REPO, "raw", "amazon_asinsight.csv"))):
    RAWA.setdefault(x["asin"], x)          # first appearance = the row master took its source_url from
RAWG = {}
for x in csv.DictReader(open(os.path.join(REPO, "raw", "gumroad.csv"))):
    RAWG.setdefault(x["product_id"], x)
out = []
done_fetch = {}
for r in S:
    mk, route = r["marketplace"], r["fetch_route"]
    res = {"marketplace": mk, "product_id": r["product_id"], "title": r["title"][:80], "fetch_route": route}
    url = None; fields = []; lookup = None
    if route == "third_party:profitable.app":
        url = r["source_url"]; fields = ["price_usd_est", "review_count", "rating", "bsr"]
        nid_ins = re.sub(r"\W+", "_", (re.search(r"category=(\d+)", url).group(1) if "category=" in url else "ROOT") + "_" + (re.search(r"insight=([a-z-]+)", url).group(1) if "insight=" in url else "all"))
        orig = os.path.join(BASE, "pages", "profitable", nid_ins + ".html"); lookup = lambda fp: prof_lookup(fp, r["product_id"]); site = "profitable.app"
    elif mk == "gumroad":
        # first appearance url is in query_or_category; use the saved search JSON
        g = RAWG.get(r["product_id"])
        url = g["source_url"]; frm = re.search(r"from=(\d+)", url).group(1)
        orig = os.path.join(BASE, "pages", "gumroad", re.sub(r"\W+", "_", f"{g['query']}_{g['sort']}_{frm}") + ".json"); fields = ["price", "review_count", "rating"]
        r = dict(r); r["review_count"] = g["rating_count"] if g["rating_count"] not in ("", "None") else NS; r["rating"] = g["rating"] if g["rating"] not in ("", "None") else NS
        lookup = lambda fp: gum_lookup(fp, r["product_id"]); site = "gumroad.com"
    elif route == "third_party:asinsight":
        a0 = RAWA[r["product_id"]]; r = dict(r); r["monthly_sales_est_thirdparty"] = a0["monthly_sales_est_thirdparty"]; r["rating"] = a0["rating"]
        url = a0["source_url"]; slug = url.rstrip("/").split("/")[-1]
        orig = os.path.join(BASE, "pages", "asinsight", slug[:150] + ".html"); fields = ["monthly_sales_est_thirdparty", "rating"]
        lookup = lambda fp: asi_lookup(fp, r["product_id"], url); site = "asinsight.com"
    elif mk == "teacherspayteachers":
        q = r["query_or_category"].split(" | ")[0]
        orig = os.path.join(BASE, "pages", "tpt", f"tpt_{q.replace(' ', '_')}_1.html")
        url = "https://www.teacherspayteachers.com/browse?" + __import__("urllib.parse").parse.urlencode({"search": q})
        fields = ["review_count", "rating"]; lookup = lambda fp: tpt_lookup(fp, r["source_url"]); site = "teacherspayteachers.com"
    else:
        res.update({"reparse_status": "not checked (source not re-parseable in verifier)", "live_status": "not re-fetched"}); out.append(res); continue
    # (1) re-parse original
    o = lookup(orig) if os.path.exists(orig) else None
    if o is None:
        res["reparse_status"] = "row not found in saved page (page 2 / other view)"
    else:
        bad = [k for k in fields if not same(o.get(k, NS), r[k])]
        res["reparse_status"] = "match" if not bad else "MISMATCH " + ",".join(f"{k}:{r[k]}->{o.get(k)}" for k in bad)
    # (2) live re-fetch (one fetch per unique URL)
    try:
        if url not in done_fetch:
            fp = os.path.join(VD, re.sub(r"\W+", "_", url)[-150:] + (".json" if site == "gumroad.com" else ".html"))
            if not (os.path.exists(fp) and os.path.getsize(fp) > 1000):
                st, _ = fetch(site, url, fp, 7, 10, accept="application/json" if site == "gumroad.com" else None)
            done_fetch[url] = fp
        if not os.path.exists(done_fetch[url]):
            raise FileNotFoundError(done_fetch[url])
        n = lookup(done_fetch[url])
        if n is None:
            res["live_status"] = "row no longer on page (rank drift)"
        else:
            bad = [k for k in fields if not same(n.get(k, NS), r[k])]
            res["live_status"] = "match" if not bad else "DRIFT " + ",".join(f"{k}:{r[k]}->{n.get(k)}" for k in bad)
    except SiteBlocked as e:
        res["live_status"] = "BLOCKED " + str(e)[:80]
    except Exception as e:
        res["live_status"] = "fetch failed (network/curl error): " + str(e)[:60]
    except StopMorocco as e:
        print("STOP MOROCCO", e); break
    res["verified_at"] = utcnow(); out.append(res)
    print(res, flush=True)
keys = ["marketplace", "product_id", "title", "fetch_route", "reparse_status", "live_status", "verified_at"]
with open(os.path.join(REPO, "verification.csv"), "w", newline="") as fh:
    wr = csv.DictWriter(fh, keys, extrasaction="ignore", restval=""); wr.writeheader(); wr.writerows(out)
c1 = collections.Counter(x["reparse_status"].split(" ")[0] for x in out); c2 = collections.Counter(x["live_status"].split(" ")[0] for x in out)
print("sample", len(out), "reparse", c1, "live", c2)
