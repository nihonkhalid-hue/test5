"""Build master.csv (one row per product per marketplace) from raw per-source CSVs.
Raw values are copied verbatim; every derived number is in a *_est column (formulas in COVERAGE.md)."""
import csv, datetime, json, math, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from netlib import REPO
import classify as C
csv.field_size_limit(10 ** 9)
RAW = os.path.join(REPO, "raw")
NS = "NOT SHOWN"
TODAY = datetime.date(2026, 11, 5)
FX = {"USD": 1.0, "EUR": 1.08, "GBP": 1.27, "CAD": 0.72, "AUD": 0.65, "INR": 0.012, "JPY": 0.0066, "MAD": 0.10, "BRL": 0.18, "PHP": 0.017, "SGD": 0.74, "MXN": 0.055}
COLS = ["marketplace", "product_id", "query_or_category", "appearances", "rank_on_page", "title", "author_or_brand", "publisher",
        "independently_published", "format", "price", "currency", "price_usd_est", "rating", "review_count", "bsr", "bsr_category",
        "category_ranks", "best_category_rank", "monthly_sales_est_thirdparty", "monthly_revenue_est_thirdparty", "monthly_sales_est_bsr",
        "sales_per_day_est", "royalty_per_sale_est", "monthly_royalty_est", "royalty_assumptions", "publication_date", "listing_age_days",
        "listing_age_days_est", "page_count", "trim_size", "interior", "segment", "niche", "audience", "anime_japan_kawaii_fit", "women_lean",
        "evergreen_or_seasonal", "season", "ip_risk", "kindle_unlimited", "is_book", "velocity_metric", "velocity_value",
        "source_url", "fetched_at", "fetch_route", "notes"]


def rd(name):
    p = os.path.join(RAW, name)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []


def fnum(x):
    try:
        v = float(str(x).replace(",", "").replace("$", "").strip())
        return v if math.isfinite(v) else None
    except Exception:
        return None


def pdate(s):
    s = (s or "").strip()
    for f in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d %B %Y", "%B %Y", "%Y", "%b %Y", "%B %d %Y"):
        try:
            return datetime.datetime.strptime(s, f).date(), f
        except Exception:
            pass
    return None, None


# TCK Publishing BSR-to-sales model (tckpublishing.com/amazon-book-sales-calculator, plugin script.js v7.1.4)
TCK = {"book": (-0.33483877, -0.06198923, 3.69500221), "ebook": (-0.34034503, -0.07791303, 3.98993694)}


def tck_monthly(bsr, kind):
    a, b, e = TCK[kind]
    L = math.log10(bsr)
    return round(10 ** (e + a * L + b * L * L) * 15 * 1.08)


# KDP printing cost constants, Amazon.com (kdp.amazon.com help G201834340 paperback, GHT976ZKSKUXBB6H hardcover), fetched 2026-11-05
def print_cost(fmt, pages, ink, large):
    if fmt == "paperback":
        if ink == "color":
            if pages <= 40: return 4.20 if large else 3.60
            return 1.00 + pages * (0.08 if large else 0.065)
        if pages <= 110: return 2.84 if large else 2.30
        return 1.00 + pages * (0.017 if large else 0.012)
    if fmt == "hardcover":
        if pages <= 108: return 7.49 if large else 6.80
        return 5.65 + pages * (0.017 if large else 0.012)
    return None


LARGE_SEG = {"coloring", "puzzle", "activity-kids", "workbook-education", "picture-book", "art-instruction"}


def royalty(fmt, price, pages, seg, trim_known):
    """Return (royalty_per_sale_est, assumption text)."""
    if price is None or price <= 0: return NS, "no price"
    if fmt in ("kindle", "ebook"):
        rate = 0.70 if 2.99 <= price <= 9.99 else 0.35
        return round(rate * price, 2), f"ebook {int(rate*100)}% x list (delivery fee ignored)"
    if fmt in ("paperback", "hardcover", "spiral"):
        f2 = "paperback" if fmt == "spiral" else fmt
        if pages is None:
            pages = {"coloring": 104, "puzzle": 110, "activity-kids": 100, "workbook-education": 110, "picture-book": 32, "journal": 120,
                     "planner": 160, "logbook": 120, "notebook": 120, "art-instruction": 120, "cookbook": 200}.get(seg, 300)
            pa = f"pages assumed {pages}"
        else:
            pa = f"pages {pages}"
        ink = "color" if seg == "picture-book" else "bw"
        large = trim_known if trim_known is not None else (seg in LARGE_SEG)
        pc = print_cost(f2, int(pages), ink, large)
        rate = 0.60 if price >= 9.99 else 0.50
        return round(rate * price - pc, 2), f"{f2} {int(rate*100)}% x list - print {pc:.2f} ({ink}, {'large' if large else 'regular'} trim{'' if trim_known is not None else ' assumed'}, {pa})" + ("; spiral not a KDP format, priced as paperback" if fmt == "spiral" else "")
    return NS, "format not KDP"


def trim_from_dims(d):
    m = re.search(r"([0-9.]+) x ([0-9.]+) x ([0-9.]+) (inches|cm)", d or "")
    if not m: return NS, None
    v = sorted([float(m.group(1)), float(m.group(2)), float(m.group(3))])
    if m.group(4) == "cm": v = [x / 2.54 for x in v]
    w, h = v[1], v[2]
    return f"{w:.2f} x {h:.2f} in", (w > 6.12 or h > 9.0)


def fmt_norm(f):
    f = (f or "").lower()
    if "kindle" in f or "ebook" in f: return "kindle"
    if "hardcover" in f or "board" in f: return "hardcover"
    if "spiral" in f: return "spiral"
    if "paperback" in f: return "paperback"
    if "audible" in f or "audio" in f: return "audiobook"
    return f or NS


def classify(r, cat_text=""):
    t = r["title"] if r["title"] != NS else ""
    seg = C.segment(t, cat_text)
    r["segment"] = seg; r["niche"] = C.niche(seg, t)
    r["interior"] = C.interior(seg, t) if r.get("is_book", "yes") != "no" else "n/a"
    r["audience"] = C.audience(t, cat_text)
    full = t + " " + cat_text
    r["anime_japan_kawaii_fit"] = C.japan_fit(t)
    r["women_lean"] = C.women_lean(full, seg, r["audience"])
    r["evergreen_or_seasonal"], r["season"] = C.season(t)
    r["ip_risk"] = C.ip_risk(t, r.get("publisher", ""))


def finish(r, pages, trim_large):
    price = r["price_usd_est"] if isinstance(r["price_usd_est"], float) else fnum(r["price_usd_est"])
    if r.get("is_book") != "no":
        roy, why = royalty(r["format"], price, pages, r["segment"], trim_large)
    else:
        roy, why = NS, "not a book"
    r["royalty_per_sale_est"], r["royalty_assumptions"] = roy, why
    ms = fnum(r["monthly_sales_est_bsr"]) or fnum(r["monthly_sales_est_thirdparty"])
    r["monthly_royalty_est"] = round(roy * ms, 0) if isinstance(roy, float) and ms is not None else NS
    rev = fnum(r["review_count"])
    age = r["listing_age_days"] if isinstance(r["listing_age_days"], int) else (r["listing_age_days_est"] if isinstance(r["listing_age_days_est"], int) else None)
    if rev is not None and age is not None and age >= 0:
        r["velocity_metric"] = "reviews_per_month_since_publication"
        r["velocity_value"] = round(rev / max(age / 30.44, 1.0), 2)
    else:
        r["velocity_metric"], r["velocity_value"] = NS, NS


def blank():
    return {c: NS for c in COLS}


def main():
    master = {}
    notes = collections.Counter()
    # ---------- OpenLibrary + Amazon dp enrichment ----------
    ol = {r["isbn10"]: r for r in rd("enrich_openlibrary.csv") if r["http"] == "200"}
    dp = {(r["marketplace"], r["asin"]): r for r in rd("amazon_direct_dp.csv")}
    # ---------- profitable.app ----------
    for b in rd("profitable_books.csv"):
        key = ("amazon.com", b["asin"])
        view = f"profitable:{b['view_node_name']}[{b['insight']}]"
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            continue
        r = blank(); r.update({"marketplace": "amazon.com", "product_id": b["asin"], "query_or_category": view, "appearances": 1,
                               "rank_on_page": b["rank_on_page"], "title": (b["title"] + (": " + b["subtitle"] if b["subtitle"] not in ("", NS) else "")) or NS,
                               "author_or_brand": b["author"], "publisher": b["publisher"], "format": fmt_norm(b["format"]),
                               "currency": "USD", "rating": b["rating"], "review_count": b["ratingCount"],
                               "kindle_unlimited": b["isKindleUnlimited"], "is_book": "yes",
                               "source_url": b["source_url"], "fetched_at": b["fetched_at"], "fetch_route": b["fetch_route"]})
        pc = fnum(b["priceUsd"]); r["price"] = f"{pc/100:.2f}" if pc is not None else NS; r["price_usd_est"] = round(pc / 100, 2) if pc is not None else NS
        pub = (b["publisher"] or "")
        r["independently_published"] = "yes" if re.search(r"independently published", pub, re.I) else ("likely (third-party likelyKdp flag)" if b["likelyKdp"] == "True" else "no")
        bsr = fnum(b["bsrTop"])
        r["bsr"] = int(bsr) if bsr else NS; r["bsr_category"] = b["bsrTopCategory"]
        r["category_ranks"] = (b["allPlacementsText"] or NS).replace("\n", " | ")
        r["best_category_rank"] = f"#{b['bestSubCategoryRank']} in {b['bestSubCategoryName']}"
        r["monthly_revenue_est_thirdparty"] = round(fnum(b["monthlyRevenue"]), 2) if fnum(b["monthlyRevenue"]) is not None else NS
        if bsr and b["bsrTopCategory"] in ("Books", "Kindle Store"):
            kind = "ebook" if b["bsrTopCategory"] == "Kindle Store" else "book"
            mo = tck_monthly(bsr, kind); r["monthly_sales_est_bsr"] = mo; r["sales_per_day_est"] = round(mo / 30, 2)
        d, _ = pdate(b["publishedAt"]); r["publication_date"] = b["publishedAt"]
        if d: r["listing_age_days"] = (datetime.date.fromisoformat(b["fetched_at"][:10]) - d).days
        pg = re.match(r"(\d+)", b["printLength"] or ""); pages = int(pg.group(1)) if pg else None
        r["page_count"] = pages if pages else NS
        trim_large = None
        dpr = dp.get(key)
        if dpr: r["trim_size"], trim_large = trim_from_dims(dpr["dimensions"])
        o = ol.get(b["asin"])
        if o and r["trim_size"] == NS and o["physical_dimensions"] != NS:
            r["trim_size"] = o["physical_dimensions"] + " (openlibrary)"
        classify(r, (b["view_node_name"] or "") + " " + r["category_ranks"])
        finish(r, pages, trim_large)
        master[key] = r
    # ---------- Amazon direct lists ----------
    for b in rd("amazon_direct_lists.csv"):
        key = (b["marketplace"], b["asin"]); view = f"{b['list']}:{b['node_name']}"
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            m["notes"] = (m["notes"] if m["notes"] != NS else "") + f"[also in Amazon {view} #{b['rank']}]"
            if b["ms_pct_change"] != NS: m["notes"] += f"[M&S {b['ms_pct_change']}% rank {b['ms_current_sales_rank']} from {b['ms_rank_24h_ago']}]"
            continue
        r = blank(); cur = "GBP" if b["marketplace"] == "amazon.co.uk" else "EUR" if b["marketplace"] == "amazon.de" else "CAD" if b["marketplace"] == "amazon.ca" else "USD"
        r.update({"marketplace": b["marketplace"], "product_id": b["asin"], "query_or_category": view, "appearances": 1, "rank_on_page": b["rank"],
                  "title": b["title"], "author_or_brand": b["author"], "format": fmt_norm(b["format"]) if b["format"] != NS else NS,
                  "price": b["price"], "currency": cur, "rating": b["rating"], "review_count": b["reviews"], "is_book": "yes",
                  "source_url": b["source_url"], "fetched_at": b["fetched_at"], "fetch_route": "curl"})
        p = fnum(re.sub(r"[^0-9.]", "", b["price"])) if b["price"] != NS else None
        r["price_usd_est"] = round(p * FX[cur], 2) if p else NS
        if b["ms_current_sales_rank"] != NS:
            r["bsr"] = b["ms_current_sales_rank"]; r["notes"] = f"M&S {b['ms_pct_change']}% (24h ago rank {b['ms_rank_24h_ago']})"
        dpr = dp.get(key); pages = None; trim_large = None
        if dpr:
            r["publisher"] = dpr["publisher"]; r["publication_date"] = dpr["publication_date"]
            r["independently_published"] = "yes" if re.search(r"independently published", dpr["publisher"], re.I) else "no"
            pg = re.match(r"(\d+)", dpr["print_length"]); pages = int(pg.group(1)) if pg else None
            r["page_count"] = pages or NS; r["trim_size"], trim_large = trim_from_dims(dpr["dimensions"])
            r["category_ranks"] = dpr["bsr_text"]
            mm = re.search(r"#([0-9,]+) in Books", dpr["bsr_text"])
            if mm and b["marketplace"] == "amazon.com":
                r["bsr"] = int(mm.group(1).replace(",", "")); r["bsr_category"] = "Books"
                mo = tck_monthly(r["bsr"], "book"); r["monthly_sales_est_bsr"] = mo; r["sales_per_day_est"] = round(mo / 30, 2)
            d, _ = pdate(dpr["publication_date"])
            if d: r["listing_age_days"] = (datetime.date.fromisoformat(r["fetched_at"][:10]) - d).days
        o = ol.get(b["asin"])
        if o:
            if r["publisher"] == NS: r["publisher"] = o["publishers"]; r["independently_published"] = "yes" if re.search(r"independently published", o["publishers"], re.I) else "no"
            if r["page_count"] == NS and str(o["number_of_pages"]).isdigit(): pages = int(o["number_of_pages"]); r["page_count"] = pages
            if r["publication_date"] == NS and o["publish_date"] != NS:
                r["publication_date"] = o["publish_date"] + " (openlibrary)"
                d, f = pdate(o["publish_date"])
                if d: r["listing_age_days_est" if f in ("%Y", "%B %Y", "%b %Y") else "listing_age_days"] = (TODAY - d).days
        classify(r, b["node_name"]); finish(r, pages, trim_large)
        master[key] = r
    # ---------- ASINsight ----------
    for b in rd("amazon_asinsight.csv"):
        key = ("amazon.com", b["asin"]); view = f"asinsight:{b['keyword']}"
        title = b["title"] if not b["title"].startswith(NS) else b.get("title_ld", NS)
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            v = fnum(b["monthly_sales_est_thirdparty"])
            if v is not None and (fnum(m["monthly_sales_est_thirdparty"]) or 0) < v:
                m["monthly_sales_est_thirdparty"] = int(v); m["notes"] = (m["notes"] if m["notes"] != NS else "") + f"[asinsight units {int(v)}/mo, {b['report_month']}]"
            continue
        r = blank(); r.update({"marketplace": "amazon.com", "product_id": b["asin"], "query_or_category": view, "appearances": 1, "rank_on_page": b["rank"],
                               "title": title, "author_or_brand": NS, "price": b["price"], "currency": "USD",
                               "price_usd_est": fnum(b["price"]) if fnum(b["price"]) else NS, "rating": b["rating"],
                               "review_count": b["review_count_exact"] if b.get("review_count_exact", NS) != NS else b["reviews"],
                               "monthly_sales_est_thirdparty": b["monthly_sales_est_thirdparty"], "is_book": b["is_book"],
                               "source_url": b["source_url"], "fetched_at": b["fetched_at"], "fetch_route": b["fetch_route"],
                               "notes": f"asinsight report month {b['report_month']}; products tracked {b['products_tracked']}"})
        o = ol.get(b["asin"]); pages = None
        if o:
            r["publisher"] = o["publishers"]; r["independently_published"] = "yes" if re.search(r"independently published", o["publishers"], re.I) else "no"
            if str(o["number_of_pages"]).isdigit(): pages = int(o["number_of_pages"]); r["page_count"] = pages
            r["publication_date"] = o["publish_date"] + " (openlibrary)"
            d, f = pdate(o["publish_date"])
            if d: r["listing_age_days_est" if f in ("%Y", "%B %Y", "%b %Y") else "listing_age_days"] = (TODAY - d).days
        r["format"] = "paperback?" if b["asin"][0].isdigit() else NS
        classify(r, b["keyword"])
        if b["is_book"] == "no": r["segment"] = "non-book-supply"; r["niche"] = "supply-for:" + b["keyword"]
        fmt_for_roy = "paperback" if b["asin"][0].isdigit() else NS
        r2 = dict(r); r2["format"] = fmt_for_roy; finish(r2, pages, None); r.update({k: r2[k] for k in ("royalty_per_sale_est", "royalty_assumptions", "monthly_royalty_est", "velocity_metric", "velocity_value")})
        master[key] = r
    # ---------- Gumroad ----------
    for b in rd("gumroad.csv"):
        key = ("gumroad", b["url"] or b["product_id"]); view = f"{b['query']}[{b['sort']}]"
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            continue
        r = blank(); cur = (b["currency"] or "usd").upper(); pc = fnum(b["price_cents"])
        r.update({"marketplace": "gumroad", "product_id": b["product_id"], "query_or_category": view, "appearances": 1, "rank_on_page": b["rank_on_page"],
                  "title": b["title"], "author_or_brand": b["creator"], "format": "digital (" + (b["native_type"] or "") + ")",
                  "price": f"{pc/100:.2f}" if pc is not None else NS, "currency": cur,
                  "price_usd_est": round(pc / 100 * FX.get(cur, float('nan')), 2) if pc is not None and cur in FX else NS,
                  "rating": b["rating"], "review_count": b["rating_count"], "is_book": "digital",
                  "source_url": b["url"] or b["source_url"], "fetched_at": b["fetched_at"], "fetch_route": "curl", "notes": f"pwyw={b['pay_what_you_want']}"})
        classify(r, b["query"]); r["royalty_assumptions"] = "not KDP"; master[key] = r
    # ---------- TpT ----------
    for b in rd("teacherspayteachers.csv"):
        key = ("teacherspayteachers", b["url"] or b["title"]); view = b["query"]
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            continue
        r = blank(); p = fnum(b["price"].replace("$", "")) if b["price"] not in (NS, "Free") else (0.0 if b["price"] == "Free" else None)
        r.update({"marketplace": "teacherspayteachers", "product_id": b["url"].split("-")[-1] if b["url"] else NS, "query_or_category": view, "appearances": 1,
                  "rank_on_page": b["rank"], "title": b["title"], "author_or_brand": b["seller"], "format": "digital", "price": b["price"], "currency": "USD",
                  "price_usd_est": p if p is not None else NS, "rating": b["rating"], "review_count": b["reviews"], "is_book": "digital",
                  "source_url": b["url"] or b["source_url"], "fetched_at": b["fetched_at"], "fetch_route": "curl", "notes": "grades " + b["grades"]})
        classify(r, b["query"]); r["royalty_assumptions"] = "not KDP"; master[key] = r
    # ---------- Etsy via RankHero ----------
    for b in rd("etsy_rankhero_listings.csv"):
        key = ("etsy", b["listing_id"]); view = "rankhero:" + b["keyword"]
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            continue
        r = blank(); pm = re.match(r"([$£€])\s*([0-9.,]+)", b["price"]); cur = {"$": "USD", "£": "GBP", "€": "EUR"}.get(pm.group(1)) if pm else NS
        if not pm:
            pm2 = re.match(r"([A-Z]{3})\s*([0-9.,]+)", b["price"]); cur = pm2.group(1) if pm2 else NS; pm = pm2
        val = fnum(pm.group(2)) if pm else None
        r.update({"marketplace": "etsy", "product_id": b["listing_id"], "query_or_category": view, "appearances": 1, "rank_on_page": b["rank"],
                  "title": b["title"], "author_or_brand": b["shop"], "format": "digital/physical (etsy)", "price": b["price"], "currency": cur,
                  "price_usd_est": round(val * FX[cur], 2) if val is not None and cur in FX else NS, "is_book": "digital",
                  "source_url": b["url"], "fetched_at": b["fetched_at"], "fetch_route": "third_party:rankhero",
                  "notes": f"favorites {b['favorites']}; views {b['views']}"})
        classify(r, b["keyword"]); r["royalty_assumptions"] = "not KDP"; master[key] = r
    # ---------- Goodreads shelves ----------
    for b in rd("goodreads_shelves.csv"):
        if b["title"] == NS: notes["goodreads blank cards"] += 1
        key = ("goodreads", b["title"] + "|" + b["author"]); view = "shelf:" + b["shelf"]
        if key in master:
            m = master[key]; m["appearances"] += 1
            if view not in m["query_or_category"]: m["query_or_category"] += " | " + view
            continue
        r = blank(); r.update({"marketplace": "goodreads", "product_id": NS, "query_or_category": view, "appearances": 1, "rank_on_page": b["rank"],
                               "title": b["title"], "author_or_brand": b["author"], "rating": b["avg_rating"], "review_count": b["ratings"],
                               "publication_date": b["published_year"], "is_book": "yes", "source_url": b["source_url"], "fetched_at": b["fetched_at"],
                               "fetch_route": "curl", "notes": "Goodreads ratings count (not Amazon reviews); demand/popularity signal"})
        if b["published_year"].isdigit(): r["listing_age_days_est"] = (TODAY - datetime.date(int(b["published_year"]), 7, 1)).days
        classify(r, b["shelf"].replace("-", " ")); r["royalty_assumptions"] = "not a listing"
        finish(r, None, None); r["royalty_per_sale_est"] = NS; r["monthly_royalty_est"] = NS
        if r["velocity_metric"] != NS: r["velocity_metric"] = "goodreads_ratings_per_month_since_pub_year_est"
        master[key] = r
    rows = list(master.values())
    with open(os.path.join(REPO, "master.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)
    print("master rows", len(rows), collections.Counter(r["marketplace"] for r in rows), notes)


if __name__ == "__main__":
    main()
