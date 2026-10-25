"""Analysis tables from master.csv + keyword/trend data. Writes CSVs + report fragments (JSON)."""
import csv, datetime as dt, glob, json, math, os, re, statistics as st, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import classify as C

BASE = "/tmp/claude-0/-home-user-test5/f1949923-2992-520a-80c3-c501569412ac/scratchpad"
RAW = os.path.join(BASE, "raw")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "out")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def f(x):
    try:
        return float(str(x).replace(",", ""))
    except Exception:
        return None


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 2) if xs else None


def pct_rank(vals):
    """percentile rank 0..1 for dict name->value (None -> 0.5 neutral)."""
    real = sorted(v for v in vals.values() if v is not None)
    out = {}
    for k, v in vals.items():
        if v is None or not real:
            out[k] = 0.5
        else:
            out[k] = (sum(1 for x in real if x < v) + 0.5 * sum(1 for x in real if x == v)) / len(real)
    return out


def wcsv(name, rows, cols=None):
    if not rows: return
    cols = cols or list(rows[0].keys())
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def trends_tables():
    """Google Trends (pytrends) series -> monthly profile, peaks, YoY."""
    res = []
    for p in sorted(glob.glob(os.path.join(RAW, "trends", "*.csv"))):
        name = os.path.basename(p)[:-4]
        term, geo = name.rsplit("_", 1)
        term = term.replace("_", " ")
        pts = []
        for r in rd(p):
            d = r.get("date") or r.get("") or list(r.values())[0]
            v = f(r.get(term))
            if v is not None and re.match(r"\d{4}-\d\d-\d\d", d or ""):
                pts.append((dt.date.fromisoformat(d[:10]), v))
        if len(pts) < 60: continue
        bym = defaultdict(list)
        for d, v in pts:
            bym[d.month].append(v)
        prof = {m: round(st.mean(bym[m]), 1) for m in range(1, 13) if bym[m]}
        last = [v for d, v in pts[-52:]]; prev = [v for d, v in pts[-104:-52]]
        yoy = round((st.mean(last) / st.mean(prev) - 1) * 100, 1) if prev and st.mean(prev) else None
        first = [v for d, v in pts[:52]]
        g5 = round((st.mean(last) / st.mean(first) - 1) * 100, 1) if first and st.mean(first) else None
        ranked = sorted(prof, key=lambda m: -prof[m])
        peak = ranked[0]
        res.append({"term": term, "geo": geo, "route": "pytrends (Google Trends widget API), weekly 5y",
                    "weeks": len(pts), "peak_month": MONTHS[peak - 1], "second_peak": MONTHS[ranked[1] - 1],
                    "trough_month": MONTHS[ranked[-1] - 1], "yoy_pct_last52_vs_prev52": yoy, "change_5y_pct": g5,
                    "list_by": list_by(peak), **{MONTHS[m - 1]: prof.get(m) for m in range(1, 13)}})
    return res


def list_by(peak_month):
    """Peak month start minus 6 weeks (middle of the 4-8 week indexing window)."""
    y = 2026 if peak_month > 10 else 2027
    d = dt.date(y, peak_month, 1) - dt.timedelta(weeks=6)
    return d.strftime("%Y-%m-%d")


def rankhero_seasonality(kw):
    out = []
    for r in kw:
        ser = json.loads(r["monthly_series"] or "[]")
        if len(ser) < 12: continue
        vals = {m.split()[0][:3]: v for m, v in ser}
        mx = max(vals.values()); mn = min(vals.values())
        peaks = [m for m in MONTHS if vals.get(m) == mx]
        troughs = [m for m in MONTHS if vals.get(m) == mn]
        out.append({"term": r["keyword"], "geo": "Etsy (all countries)",
                    "route": "third_party:rankhero monthly Etsy searches (bucketed)",
                    "weeks": "", "peak_month": "/".join(peaks) if mx != mn else "flat",
                    "second_peak": "", "trough_month": "/".join(troughs) if mx != mn else "flat",
                    "yoy_pct_last52_vs_prev52": trend_pct(r["trend_sentence"]), "change_5y_pct": "",
                    "list_by": list_by(MONTHS.index(peaks[0]) + 1) if mx != mn and len(peaks) <= 4 else "evergreen",
                    **{m: vals.get(m) for m in MONTHS}})
    return out


def trend_pct(s):
    m = re.search(r"(dropped|fell|decreased|rose|grew|increased) (\d+)%", s or "")
    if not m: return None
    return (-1 if m.group(1) in ("dropped", "fell", "decreased") else 1) * int(m.group(2))


def main():
    rows = rd(os.path.join(OUT, "master.csv"))
    kw = rd(os.path.join(RAW, "thirdparty", "rankhero_keywords.csv"))
    kk = rd(os.path.join(RAW, "thirdparty", "kupkaike_niches.csv"))
    res = {}

    # ---------- seasonality ----------
    gt = trends_tables()
    rs = rankhero_seasonality(kw)
    wcsv("seasonality.csv", gt + rs, ["term", "geo", "route", "weeks", "peak_month", "second_peak", "trough_month",
                                      "yoy_pct_last52_vs_prev52", "change_5y_pct", "list_by"] + MONTHS)
    res["gt"] = gt; res["rs"] = rs

    # ---------- keyword -> niche aggregation ----------
    kn = defaultdict(list)
    for r in kw:
        n = C.niche(r["keyword"])
        sr = f(r["monthly_searches"]); el = f(r["etsy_listings"])
        kn[n].append({"kw": r["keyword"], "searches": sr, "listings": el,
                      "sd": (sr / el) if sr and el else None, "trend": trend_pct(r["trend_sentence"]),
                      "median_price": f((r["median_price"] or "").strip("$.")), "difficulty": f(r["difficulty"])})
    gt_by_niche = defaultdict(list)
    for g in gt:
        gt_by_niche[C.niche(g["term"])].append(g["yoy_pct_last52_vs_prev52"])

    # ---------- niche table ----------
    by = defaultdict(list)
    for r in rows:
        if r["niche"] == "supplies-not-a-book": continue
        by[r["niche"]].append(r)
    etsy_rh = defaultdict(list)
    for r in rows:
        if r["marketplace"] == "etsy" and "rankhero" in r["fetch_route"]:
            etsy_rh[r["niche"]].append(r)
    table = []
    for n, rs_ in by.items():
        mk = Counter(r["marketplace"] for r in rs_)
        prices = [f(r["price_usd_est"]) for r in rs_ if f(r["price_usd_est"]) is not None and f(r["price_usd_est"]) > 0]
        revs = [f(r["review_count"]) for r in rs_ if r["marketplace"] in ("gumroad", "teacherspayteachers", "amazon") and f(r["review_count"]) is not None]
        gr = [f(r["review_count"]) for r in rs_ if r["marketplace"] == "gumroad" and f(r["review_count"]) is not None]
        vel = [f(r["velocity_value"]) for r in rs_ if r["marketplace"] == "etsy" and r["velocity_metric"].startswith("favorites") and "LOWER BOUND" not in r["fetch_route"]]
        favs = [f(r["favorites"]) for r in rs_ if r["marketplace"] == "etsy" and f(r["favorites"]) is not None]
        bs = [r["bestseller_badge"] for r in rs_ if r["bestseller_badge"] in ("yes", "no")]
        shops = Counter(r["seller"] for r in etsy_rh.get(n, []) if r["seller"])
        top3 = sum(c for _, c in shops.most_common(3)) / sum(shops.values()) if shops else None
        k = kn.get(n, [])
        sd = med([x["sd"] for x in k]); srch = max([x["searches"] for x in k if x["searches"]] or [0]) or None
        lst = max([x["listings"] for x in k if x["listings"]] or [0]) or None
        tr = med([x["trend"] for x in k] + [x for x in gt_by_niche.get(n, []) if x is not None])
        amz = [f(r["monthly_sales_est_thirdparty"]) for r in rs_ if r["marketplace"] == "amazon"]
        young_hits = [r for r in rs_ if (f(r["listing_age_days"]) or f(r["listing_age_days_est"]) or 1e9) < 365]
        table.append({
            "niche": n, "rows_collected": len(rs_), "marketplaces": len(mk),
            "by_marketplace": "; ".join(f"{a}:{b}" for a, b in mk.most_common()),
            "etsy_monthly_searches_max_kw": srch, "etsy_competing_listings_max_kw": lst,
            "search_per_listing_median": round(sd, 4) if sd else None,
            "trend_pct_median": tr, "median_price_usd": med(prices),
            "median_reviews_gumroad_tpt_amazon": med(revs), "median_gumroad_ratings": med(gr),
            "etsy_median_favorites": med(favs), "etsy_median_fav_per_month_est": med(vel),
            "bestseller_share": round(bs.count("yes") / len(bs), 2) if bs else None, "bestseller_n": len(bs),
            "etsy_top3_shop_share": round(top3, 2) if top3 is not None else None,
            "amazon_monthly_sales_est_median": med(amz),
            "listings_lt12m_age": len(young_hits),
            "listings_lt12m_50plus_reviews": sum(1 for r in young_hits if (f(r["review_count"]) or 0) >= 50),
            "listings_lt12m_100plus_favorites": sum(1 for r in young_hits if (f(r["favorites"]) or 0) >= 100),
            "japan_fit_share": round(sum(1 for r in rs_ if r["anime_japan_kawaii_fit"] == "yes") / len(rs_), 2),
            "women_lean_share": round(sum(1 for r in rs_ if r["women_lean"] == "yes") / len(rs_), 2),
            "keywords_used": "|".join(x["kw"] for x in k)[:200]})
    # opportunity score
    P_sd = pct_rank({t["niche"]: t["search_per_listing_median"] for t in table})
    P_vel = pct_rank({t["niche"]: t["etsy_median_fav_per_month_est"] for t in table})
    P_eng = pct_rank({t["niche"]: (t["median_reviews_gumroad_tpt_amazon"]) for t in table})
    P_tr = pct_rank({t["niche"]: t["trend_pct_median"] for t in table})
    P_mk = pct_rank({t["niche"]: t["marketplaces"] for t in table})
    for t in table:
        n = t["niche"]
        dom = t["etsy_top3_shop_share"] if t["etsy_top3_shop_share"] is not None else 0.3
        demand = 0.35 * P_sd[n] + 0.25 * P_vel[n] + 0.15 * P_eng[n] + 0.15 * P_tr[n] + 0.10 * P_mk[n]
        t["opportunity_score"] = round(100 * demand * (1 - 0.5 * dom), 1)
        t["evidence_n"] = sum(x is not None for x in (t["search_per_listing_median"], t["etsy_median_fav_per_month_est"],
                                                        t["median_reviews_gumroad_tpt_amazon"], t["trend_pct_median"]))
    table.sort(key=lambda t: -t["opportunity_score"])
    for i, t in enumerate(table, 1):
        t["rank"] = i
    wcsv("niche_opportunity.csv", table, ["rank", "niche", "opportunity_score", "evidence_n"] + [k for k in table[0] if k not in ("rank", "niche", "opportunity_score", "evidence_n")])
    res["niches"] = table

    # ---------- velocity top 50 ----------
    vel = [r for r in rows if r["velocity_value"] and r["niche"] != "supplies-not-a-book"]
    etsy_v = sorted([r for r in vel if r["marketplace"] == "etsy" and "LOWER BOUND" not in r["fetch_route"]],
                    key=lambda r: -f(r["velocity_value"]))
    wcsv("velocity_top50_etsy.csv", etsy_v[:50])
    amz_v = sorted([r for r in vel if r["marketplace"] == "amazon"], key=lambda r: -f(r["velocity_value"]))
    res["vel_etsy"] = etsy_v[:50]; res["vel_amz"] = amz_v[:15]
    gum_top = sorted([r for r in rows if r["marketplace"] == "gumroad" and f(r["review_count"])], key=lambda r: -f(r["review_count"]))[:25]
    res["gum_top"] = gum_top
    gs = [r for r in rows if r["marketplace"] == "gumroad" and f(r["sales_shown"])]
    res["gum_sales"] = sorted(gs, key=lambda r: -f(r["sales_shown"]))[:25]
    tpt_top = sorted([r for r in rows if r["marketplace"] == "teacherspayteachers" and f(r["review_count"])], key=lambda r: -f(r["review_count"]))[:15]
    res["tpt_top"] = tpt_top

    # ---------- title words among top velocity ----------
    stop = set("a an and the for of with to in on by or pdf printable coloring colouring page pages book books digital download instant adult adults kids sheet sheets 1 2 3 & - | , set pack".split())
    words = Counter()
    for r in etsy_v[:100] + gum_top + res["gum_sales"]:
        for w in re.findall(r"[a-z][a-z'-]+", r["title"].lower()):
            if w not in stop and len(w) > 2:
                words[w] += 1
    res["words"] = words.most_common(40)

    # ---------- price ladder ----------
    def tier(r):
        t = r["title"].lower(); pc = f(r["page_count"])
        if re.search(r"procreate", t + r["format"].lower()): return "procreate"
        if re.search(r"goodnotes", t + r["format"].lower()): return "goodnotes"
        if r["niche"] == "mega-bundle-plr": return "PLR/resell mega bundle"
        if pc is None:
            return "single sheet" if re.search(r"coloring page\b|colouring page\b|coloring sheet\b", t) and not re.search(r"pages|sheets|set|pack|bundle|book", t) else "unknown size"
        if pc <= 1: return "single sheet"
        if pc < 10: return "2-9 pages"
        if pc <= 30: return "10-30 pages"
        if pc < 50: return "31-49 pages"
        return "50+ pages"
    ladder = defaultdict(list)
    for r in rows:
        p = f(r["price_usd_est"])
        if p is None or r["niche"] == "supplies-not-a-book": continue
        ladder[(r["marketplace"], tier(r))].append(p)
    lad = []
    for (m, t), ps in sorted(ladder.items()):
        if len(ps) < 3: continue
        ps.sort()
        q = lambda a: ps[min(len(ps) - 1, int(a * len(ps)))]
        lad.append({"marketplace": m, "tier": t, "n": len(ps), "p25": round(q(0.25), 2), "median": round(st.median(ps), 2),
                    "p75": round(q(0.75), 2), "share_free": round(sum(1 for x in ps if x == 0) / len(ps), 2)})
    wcsv("price_ladder.csv", lad); res["ladder"] = lad

    # ---------- format / bundle ----------
    fm = defaultdict(lambda: Counter())
    for r in rows:
        for x in (r["format"] or "NOT SHOWN").split("|"):
            fm[r["marketplace"]][x] += 1
    res["formats"] = {m: c.most_common(8) for m, c in fm.items()}
    bund = defaultdict(lambda: [[], []])
    for r in rows:
        if r["marketplace"] in ("etsy", "gumroad"):
            k = 1 if r["is_bundle"] == "True" else 0
            v = f(r["favorites"]) if r["marketplace"] == "etsy" else f(r["review_count"])
            if v is not None: bund[r["marketplace"]][k].append(v)
    res["bundle"] = {m: {"non_bundle_median": med(a), "bundle_median": med(b), "n": (len(a), len(b))} for m, (a, b) in bund.items()}

    # ---------- cross-marketplace overlap ----------
    res["overlap"] = [t for t in table if t["marketplaces"] >= 3]

    # ---------- anime/Japan section ----------
    jp = [r for r in rows if r["anime_japan_kawaii_fit"] == "yes"]
    sub = defaultdict(list)
    for r in jp:
        t = r["title"].lower() + " " + r["query"].lower()
        s = ("retro-gaming/pixel" if re.search(r"pixel|game|gamer|arcade", t) else
             "anime/manga" if re.search(r"anime|manga|shoujo", t) else
             "cozy-japan" if re.search(r"cozy|cosy|hygge", t) and re.search(r"japan|kawaii|bento|sakura|tea", t) else
             "japan-culture/retro" if re.search(r"japan|kyoto|tokyo|geisha|kimono|yokai|showa|city pop|bento|sushi|ramen|sakura|samurai", t) else
             "kawaii/chibi")
        r["_sub"] = s
        sub[s].append(r)
    jtab = []
    for s, rs_ in sub.items():
        jtab.append({"segment": s, "rows": len(rs_), "marketplaces": len({r["marketplace"] for r in rs_}),
                     "median_price_usd": med([f(r["price_usd_est"]) for r in rs_ if f(r["price_usd_est"])]),
                     "median_gumroad_ratings": med([f(r["review_count"]) for r in rs_ if r["marketplace"] == "gumroad" and f(r["review_count"]) is not None]),
                     "etsy_median_favorites": med([f(r["favorites"]) for r in rs_ if r["marketplace"] == "etsy" and f(r["favorites"]) is not None]),
                     "etsy_median_fav_per_month_est": med([f(r["velocity_value"]) for r in rs_ if r["marketplace"] == "etsy" and r["velocity_metric"].startswith("fav") and "LOWER" not in r["fetch_route"]]),
                     "ip_fanart_rows": sum(1 for r in rs_ if r["ip_risk"].startswith("fan-art")),
                     "women_lean_share": round(sum(1 for r in rs_ if r["women_lean"] == "yes") / len(rs_), 2)})
    jtab.sort(key=lambda x: -x["rows"])
    wcsv("anime_japan_segments.csv", jtab); res["jtab"] = jtab
    jlist = sorted(jp, key=lambda r: -(f(r["velocity_value"]) or f(r["review_count"]) or f(r["favorites"]) or 0))
    wcsv("anime_japan_listings.csv", jlist, ["_sub", "marketplace", "title", "seller", "price_usd_est", "review_count", "favorites",
                                             "velocity_metric", "velocity_value", "ip_risk", "source_url", "fetch_route"])
    res["jlist"] = jlist[:30]
    jkw = [r for r in kw if C.japan_fit(r["keyword"]) == "yes"]
    res["jkw"] = jkw
    res["kk"] = kk
    res["counts"] = Counter(r["marketplace"] for r in rows)
    json.dump(res, open(os.path.join(OUT, "_analysis.json"), "w"), default=str, indent=0)
    print("niches", len(table), "velocity etsy", len(etsy_v), "jp rows", len(jp), "ladder", len(lad))


if __name__ == "__main__":
    main()
