"""Build master.csv + analysis tables from raw harvests."""
import csv, html, datetime as dt, glob, json, math, os, re, statistics as st, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import classify as C

BASE = "/tmp/claude-0/-home-user-test5/f1949923-2992-520a-80c3-c501569412ac/scratchpad"
RAW = os.path.join(BASE, "raw")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
TODAY = dt.date(2026, 10, 25)
FX = {"USD": 1.0, "EUR": 1.08, "GBP": 1.27, "CAD": 0.73, "AUD": 0.66, "NOK": 0.093, "MAD": 0.10, "INR": 0.012,
      "NZD": 0.60, "SEK": 0.095, "DKK": 0.145, "CHF": 1.13, "PLN": 0.25, "JPY": 0.0067, "SGD": 0.75, "HKD": 0.128,
      "MXN": 0.054, "TRY": 0.029, "ZAR": 0.055, "PHP": 0.017, "MYR": 0.22, "VND": 0.00004, "ILS": 0.27, "BRL": 0.18}  # fixed approx rates (estimate)

COLS = ["marketplace", "query", "rank_on_page", "title", "seller", "price", "currency", "sale_price", "price_usd_est",
        "rating", "review_count", "sales_shown", "sales_est_thirdparty", "monthly_sales_est_thirdparty",
        "bestseller_badge", "baskets_text", "favorites", "views", "listing_date", "listing_date_est",
        "listing_age_days", "listing_age_days_est", "bsr", "sales_per_day_est", "format", "page_count", "is_bundle",
        "niche", "style", "audience", "anime_japan_kawaii_fit", "women_lean", "evergreen_or_seasonal", "season",
        "ip_risk", "velocity_metric", "velocity_value", "source_url", "fetched_at", "fetch_route", "notes"]


def rd(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def money(s):
    s = (s or "").strip()
    m2 = re.match(r"([A-Z]{3}) ([0-9][0-9,]*\.?[0-9]*)", s)
    if m2:
        return float(m2.group(2).replace(",", "")), m2.group(1)
    m = re.search(r"([$£€])?\s*([0-9][0-9,]*\.?[0-9]*)", s)
    if not m: return "", ""
    cur = {"$": "USD", "£": "GBP", "€": "EUR"}.get(m.group(1) or "$", "USD")
    return float(m.group(2).replace(",", "")), cur


def fnum(x):
    try:
        return float(str(x).replace(",", ""))
    except Exception:
        return None


def base_row(**kw):
    r = {c: "" for c in COLS}
    r.update(kw)
    r["title"] = html.unescape(html.unescape(r["title"] or ""))
    t = r["title"] if r["title"] != "NOT SHOWN" else ""
    q = r["query"]
    r["niche"] = C.niche(t, q)
    r["style"] = C.style(t)
    r["audience"] = C.audience(t)
    r["anime_japan_kawaii_fit"] = C.japan_fit(t) if t else C.japan_fit(q)
    r["women_lean"] = C.women_lean(t, r["audience"])
    r["evergreen_or_seasonal"], r["season"] = C.season(t or q)
    r["ip_risk"] = C.ip_risk(t)
    if not r["format"]: r["format"] = C.fmt(t)
    if r["page_count"] == "": r["page_count"] = C.page_count(t)
    r["is_bundle"] = C.is_bundle(t, r["page_count"])
    if r["price"] not in ("", "NOT SHOWN") and r["currency"]:
        r["price_usd_est"] = round(float(r["price"]) * FX.get(r["currency"].upper(), 1.0), 2)
    return r


# ---------- Etsy ID -> date estimate ----------
def id_date_model():
    anchors = []
    for r in rd(os.path.join(RAW, "thirdparty", "etsy_id_date_anchors.csv")) + rd(os.path.join(RAW, "thirdparty", "findniche_listings.csv")):
        d = r.get("released", "")
        if re.match(r"\d{4}-\d\d-\d\d", d or ""):
            anchors.append((int(r["listing_id"]), dt.date.fromisoformat(d)))
    anchors = sorted(set(anchors))
    # keep a monotone chain (drop anchors that go backwards in time)
    chain = []
    for a in anchors:
        if not chain or a[1] >= chain[-1][1]:
            chain.append(a)
    return chain


def est_date(lid, chain):
    if len(chain) < 2: return None
    lid = int(lid)
    if lid <= chain[0][0]:
        return chain[0][1]  # older than earliest anchor: anchor date used as upper bound (age is a lower bound)
    elif lid >= chain[-1][0]:
        a, b = chain[-2], chain[-1]
    else:
        for a, b in zip(chain, chain[1:]):
            if a[0] <= lid <= b[0]: break
    span = (b[1] - a[1]).days
    frac = (lid - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0
    d = a[1] + dt.timedelta(days=round(span * frac))
    return min(d, TODAY)


def main():
    rows = []
    chain = id_date_model()

    # ---- Gumroad ----
    ga = rd(os.path.join(RAW, "gumroad", "gumroad_tierA.csv"))
    gb = {r["url"]: r for r in rd(os.path.join(RAW, "gumroad", "gumroad_tierB.csv"))}
    by = defaultdict(list)
    for r in ga:
        by[r["url"]].append(r)
    for url, rs in by.items():
        r0 = min(rs, key=lambda r: int(r["rank_on_page"]))
        b = gb.get(url, {})
        pc = b.get("page_count_attr") or b.get("page_count_text") or ""
        pc = int(re.sub(r"\D", "", pc)) if re.sub(r"\D", "", str(pc)) and len(re.sub(r"\D", "", str(pc))) < 7 else ""
        price = int(r0["price_cents"]) / 100 if r0["price_cents"] else ""
        rows.append(base_row(
            marketplace="gumroad", query=r0["query"], rank_on_page=r0["rank_on_page"], title=r0["title"],
            seller=r0["creator"], price=price, currency=(r0["currency"] or "usd").upper(),
            rating=r0["rating"] if int(r0["rating_count"] or 0) > 0 else "NOT SHOWN", review_count=r0["rating_count"],
            sales_shown=b.get("sales_count", "NOT FETCHED") if b else "NOT FETCHED",
            bestseller_badge="n/a", format=C.fmt(r0["title"], (b.get("formats_text", "") or "").replace("|", " ")),
            page_count=pc, source_url=url, fetched_at=b.get("fetched_at") or r0["fetched_at"],
            fetch_route="curl (tier A search JSON" + (" + tier B product page)" if b else ")"),
            notes=f"pwyw={r0['pay_what_you_want']}; type={r0['native_type']}; queries={'|'.join(sorted({x['query'] + ':' + x['sort'] for x in rs}))[:300]}"))
    # ---- Etsy via RankHero (+FindNiche) ----
    fn = {r["listing_id"]: r for r in rd(os.path.join(RAW, "thirdparty", "findniche_listings.csv"))}
    rh = defaultdict(list)
    for r in rd(os.path.join(RAW, "thirdparty", "rankhero_listings.csv")):
        rh[r["listing_id"]].append(r)
    ws = [dict(zip(["query", "url", "title", "price", "notes"], l.rstrip("\n").split("\t")))
          for l in open(os.path.join(RAW, "websearch", "ws_rows.tsv"), encoding="utf-8") if l.strip()]
    ws_by_lid = defaultdict(list)
    for w in ws:
        m = re.search(r"etsy\.com/(?:[a-z-]+/)?listing/(\d+)", w["url"])
        if m: ws_by_lid[m.group(1)].append(w)
    etsy_ids = list(rh) + [k for k in fn if k not in rh and "colo" in (fn[k]["title"] or "").lower()] + \
        [k for k in ws_by_lid if k not in rh and k not in fn]
    for lid in etsy_ids:
        rs, f, w = rh.get(lid, []), fn.get(lid), ws_by_lid.get(lid, [])
        r0 = min(rs, key=lambda r: int(r["rank"])) if rs else None
        title = (r0 or {}).get("title") or (f or {}).get("title") or next((x["title"] for x in w if x["title"] != "NOT SHOWN"), "NOT SHOWN")
        if r0:
            p, cur = money(r0["price"])
        elif f:
            p, cur = money(f["price"])
        else:
            p, cur = (fnum(w[0]["price"].split()[0]) if w and w[0]["price"] not in ("NOT SHOWN", "") else ""), \
                (w[0]["price"].split()[1] if w and len(w[0]["price"].split()) > 1 else "")
        led = est_date(lid, chain)
        released = (f or {}).get("released", "") if f and re.match(r"\d{4}", (f or {}).get("released", "")) else ""
        age = (TODAY - dt.date.fromisoformat(released)).days if released else ""
        age_est = (TODAY - led).days if led else ""
        routes = []
        if rs: routes.append("third_party:rankhero")
        if f: routes.append("third_party:findniche")
        if w: routes.append("websearch")
        baskets = next((re.search(r"In \d+ carts", x["notes"]).group(0) for x in w if re.search(r"In \d+ carts", x["notes"])), "")
        favs = int(r0["favorites"]) if r0 and str(r0["favorites"]).isdigit() else (f or {}).get("favorites", "")
        row = base_row(
            marketplace="etsy", query=(r0 or {}).get("keyword") or (w[0]["query"] if w else "findniche"),
            rank_on_page=(r0 or {}).get("rank", ""), title=title, seller=(r0 or {}).get("shop") or (f or {}).get("shop", ""),
            price=p, currency=cur, review_count=(f or {}).get("reviews", "NOT SHOWN") if f else "NOT SHOWN",
            sales_shown="NOT SHOWN", sales_est_thirdparty=(f or {}).get("total_sales", ""),
            monthly_sales_est_thirdparty=(f or {}).get("monthly_sales", ""),
            bestseller_badge=(f or {}).get("bestseller", "NOT SHOWN") if f else "NOT SHOWN", baskets_text=baskets,
            favorites=favs, views=(r0 or {}).get("views", ""), listing_date=released,
            listing_date_est=led.isoformat() if led else "", listing_age_days=age, listing_age_days_est=age_est,
            source_url=f"https://www.etsy.com/listing/{lid}", fetched_at=(r0 or f or {}).get("fetched_at", ""),
            fetch_route="+".join(routes) + ("; age_est is LOWER BOUND (id older than earliest anchor)" if chain and int(lid) < chain[0][0] else ""),
            notes=("rankhero_keywords=" + "|".join(sorted({x['keyword'] for x in rs}))[:250] + "; " if rs else "") +
                  ("findniche tags=" + (f or {}).get("tags", "")[:150] + "; " if f else "") +
                  ("websearch: " + "; ".join(x["notes"] for x in w if x["notes"])[:200] if w else ""))
        rows.append(row)
    # ---- other WebSearch-only rows (payhip, gumroad not in harvest, creative market, tiktok, itch...) ----
    known = {r["source_url"].split("?")[0] for r in rows}
    for w in ws:
        if re.search(r"etsy\.com/(?:[a-z-]+/)?listing/", w["url"]): continue
        u = w["url"].split("?")[0]
        if u in known: continue
        known.add(u)
        dom = re.sub(r"^www\.", "", re.match(r"https?://([^/]+)", u).group(1))
        mk = "gumroad" if dom.endswith("gumroad.com") else dom.split(".")[0] if dom != "tiktokshop.com" else "tiktokshop"
        pr = w["price"].split()
        rows.append(base_row(marketplace=mk, query=w["query"], title=w["title"], price=fnum(pr[0]) if pr and pr[0] != "NOT" else "",
                             currency=pr[1] if len(pr) > 1 else "", rating="NOT SHOWN", review_count="NOT SHOWN",
                             sales_shown=(re.search(r"'(\d+) sold'", w["notes"]).group(1) if re.search(r"'(\d+) sold'", w["notes"]) else "NOT SHOWN"),
                             source_url=u, fetched_at="2026-10-25 (WebSearch)", fetch_route="websearch", notes="summary: " + w["notes"]))
    # ---- Amazon via ASINsight ----
    for r in rd(os.path.join(RAW, "thirdparty", "asinsight_amazon.csv")):
        ms = fnum(r["monthly_sales_est_thirdparty"])
        rows.append(base_row(marketplace="amazon", query=r["keyword"], rank_on_page=r["rank"], title=r["title"],
                             seller="NOT SHOWN", price=fnum(r["price"]) or "", currency="USD", rating=r["rating"],
                             review_count=r["reviews"], monthly_sales_est_thirdparty=r["monthly_sales_est_thirdparty"],
                             sales_per_day_est=round(ms / 30.4, 1) if ms else "", bsr="NOT SHOWN (Amazon blocked)",
                             source_url="https://www.amazon.com/dp/" + r["asin"], fetched_at=r["fetched_at"],
                             fetch_route="third_party:asinsight",
                             notes=f"report_month={r['report_month']}; is_book={r['is_book']}; via {r['source_url']}"))
        if r["is_book"] == "no":
            rows[-1]["niche"] = "supplies-not-a-book"
    # ---- TpT ----
    seen = set()
    for r in rd(os.path.join(RAW, "others", "tpt.csv")):
        if r["url"] in seen: continue
        seen.add(r["url"])
        p = fnum(r["price"].replace("$", "")) if r["price"].startswith("$") else (0.0 if r["price"] == "Free" else "")
        rows.append(base_row(marketplace="teacherspayteachers", query=r["query"], rank_on_page=r["rank"], title=r["title"],
                             seller=r["seller"] or "NOT SHOWN", price=p, currency="USD", rating=r["rating"],
                             review_count=r["reviews"], source_url=r["url"], fetched_at=r["fetched_at"], fetch_route="curl",
                             notes="grades=" + r["grades"]))
        rows[-1]["audience"] = "kids" if rows[-1]["audience"] == "all" else rows[-1]["audience"]
    for r in rd(os.path.join(RAW, "others", "itch.csv")):
        rows.append(base_row(marketplace="itch.io", query=r["query"], rank_on_page=r["rank"], title=r["title"], seller=r["seller"],
                             price=fnum(re.sub(r"[^0-9.]", "", r["price"])) if re.search(r"\d", r["price"]) else "",
                             currency="USD" if re.search(r"\d", r["price"]) else "", rating=r["rating"],
                             review_count=r["reviews"], source_url=r["url"], fetched_at=r["fetched_at"], fetch_route="curl"))
    # ---- velocity ----
    for r in rows:
        age = r["listing_age_days"] or r["listing_age_days_est"]
        if age not in ("", None) and int(age) > 0:
            months = max(int(age) / 30.4, 1.0)
            rc = fnum(r["review_count"])
            if rc:
                r["velocity_metric"], r["velocity_value"] = "reviews_per_month", round(rc / months, 2)
            elif fnum(r["favorites"]):
                r["velocity_metric"], r["velocity_value"] = "favorites_per_month(est age)", round(fnum(r["favorites"]) / months, 2)
        if not r["velocity_value"] and fnum(r["monthly_sales_est_thirdparty"]):
            r["velocity_metric"], r["velocity_value"] = "monthly_sales_est_thirdparty", fnum(r["monthly_sales_est_thirdparty"])
    with open(os.path.join(OUT, "master.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)
    print("master rows", len(rows), Counter(r["marketplace"] for r in rows).most_common())
    json.dump({"anchors": [(a, b.isoformat()) for a, b in chain]}, open(os.path.join(OUT, "_anchors.json"), "w"))
    return rows


if __name__ == "__main__":
    main()
