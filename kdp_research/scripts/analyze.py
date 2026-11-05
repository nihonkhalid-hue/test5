"""Analysis tables from master.csv + trend/seasonality raw files. Writes CSVs into kdp_research/."""
import csv, collections, datetime, glob, json, math, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import REPO
csv.field_size_limit(10 ** 9)
NS = "NOT SHOWN"


def f(x):
    try:
        v = float(str(x).replace(",", ""))
        return v if math.isfinite(v) else None
    except Exception:
        return None


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 2) if xs else None


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    k = (len(xs) - 1) * p; lo = math.floor(k); hi = math.ceil(k)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 2)


def pct_rank(vals):
    s = sorted(v for v in vals if v is not None)
    return lambda v: (sum(1 for x in s if x <= v) / len(s)) if (v is not None and s) else 0.0


def w(name, rows, cols=None):
    if not rows: return
    cols = cols or list(rows[0].keys())
    with open(os.path.join(REPO, name), "w", newline="") as fh:
        wr = csv.DictWriter(fh, cols, extrasaction="ignore"); wr.writeheader(); wr.writerows(rows)


M = list(csv.DictReader(open(os.path.join(REPO, "master.csv"))))
AMZ = [r for r in M if r["marketplace"].startswith("amazon") and r["is_book"] in ("yes",) and r["segment"] != "non-book-supply"]
for r in AMZ:
    r["_sales"] = f(r["monthly_sales_est_bsr"]) if f(r["monthly_sales_est_bsr"]) is not None else f(r["monthly_sales_est_thirdparty"])
    r["_rev"] = f(r["review_count"]); r["_price"] = f(r["price_usd_est"]); r["_pages"] = f(r["page_count"])
    r["_age"] = f(r["listing_age_days"]) if f(r["listing_age_days"]) is not None else f(r["listing_age_days_est"])
    r["_vel"] = f(r["velocity_value"]); r["_roy"] = f(r["royalty_per_sale_est"]); r["_mroy"] = f(r["monthly_royalty_est"])
    r["_indie"] = 1 if r["independently_published"].startswith(("yes", "likely")) else 0
    r["_who"] = (r["publisher"] if r["publisher"] not in (NS, "") and not r["_indie"] else r["author_or_brand"]) or NS

# ---------------- Google Trends direction ----------------
TREND_FILES = glob.glob(os.path.join(REPO, "raw", "google_trends", "*.csv"))


def trend_series(path):
    rows = list(csv.reader(open(path)))[1:]
    out = []
    for r in rows:
        try: out.append((r[0][:10], float(r[1])))
        except Exception: pass
    return out


TREND = {}
for p in TREND_FILES:
    term, geo = os.path.basename(p)[:-4].rsplit("_", 1)
    s = trend_series(p)
    if len(s) < 110: continue
    last = statistics.mean(v for _, v in s[-52:]); prev = statistics.mean(v for _, v in s[-104:-52])
    first = statistics.mean(v for _, v in s[:52])
    l13 = statistics.mean(v for _, v in s[-13:]); p13 = statistics.mean(v for _, v in s[-65:-52])
    TREND[(term.replace("_", " "), geo)] = {"yoy_pct": round(100 * (last - prev) / prev, 1) if prev else None,
                                            "last13w_vs_year_ago_pct": round(100 * (l13 - p13) / p13, 1) if p13 else None,
                                            "vs_5y_ago_pct": round(100 * (last - first) / first, 1) if first else None, "series": s}
SEG_TREND = {"coloring": "coloring book", "puzzle": "word search", "journal": "gratitude journal", "planner": "planner", "activity-kids": "activity book",
             "fiction-romance": "romantasy", "nonfiction-selfhelp": "self help books", "cookbook": "cookbook", "art-instruction": "how to draw anime",
             "logbook": "password book", "workbook-education": "handwriting practice", "notebook": "sketchbook"}
NICHE_TREND = {"puzzle-sudoku": "sudoku book", "puzzle-mixed": "puzzle book", "romance-dark-mafia": "dark romance", "fiction-cozy-mystery": "cozy mystery",
               "coloring-bold-easy": "bold and easy coloring", "art-sketchbook": "sketchbook", "journal-general": "journal", "logbook-password": "password book",
               "art-how-to-draw-anime-manga": "how to draw anime", "coloring-anime-manga-kawaii": "kawaii", "romance-romantasy-fae": "romantasy"}


def trend_for(seg, niche):
    t = NICHE_TREND.get(niche) or SEG_TREND.get(seg)
    d = TREND.get((t, "US")) or TREND.get((t, "WW"))
    if not d: return "no series", None, t
    y = d["yoy_pct"]
    return ("rising" if y > 10 else "declining" if y < -10 else "flat"), y, t


# ---------------- segment & niche tables ----------------
def table(key):
    g = collections.defaultdict(list)
    for r in AMZ: g[r[key]].append(r)
    out = []
    for k, rs in g.items():
        who = collections.Counter(r["_who"] for r in rs if r["_who"] != NS)
        sales_by_who = collections.Counter()
        for r in rs:
            if r["_sales"] is not None and r["_who"] != NS: sales_by_who[r["_who"]] += r["_sales"]
        tot_sales = sum(sales_by_who.values())
        dom = round(sum(v for _, v in sales_by_who.most_common(3)) / tot_sales, 3) if tot_sales else None
        young = [r for r in rs if r["_age"] is not None and 0 <= r["_age"] < 365]
        newc = [r for r in young if (r["_rev"] or 0) >= 50 or (r["_sales"] or 0) >= 300]
        seg = rs[0]["segment"]
        tdir, tyoy, tterm = trend_for(seg, k if key == "niche" else "")
        out.append({key: k, "segment": seg, "listings": len(rs), "median_price_usd": med(r["_price"] for r in rs),
                    "median_pages": med(r["_pages"] for r in rs), "median_reviews": med(r["_rev"] for r in rs),
                    "median_monthly_sales_est": med(r["_sales"] for r in rs), "p75_monthly_sales_est": q([r["_sales"] for r in rs], .75),
                    "median_royalty_per_sale_est": med(r["_roy"] for r in rs), "median_monthly_royalty_est": med(r["_mroy"] for r in rs),
                    "share_indie": round(sum(r["_indie"] for r in rs) / len(rs), 3), "median_velocity": med(r["_vel"] for r in rs),
                    "top3_sales_share_dominance": dom, "top3_names": "; ".join(n for n, _ in sales_by_who.most_common(3)),
                    "books_under_12mo": len(young), "newcomers_50rev_or_300sales": len(newc),
                    "newcomer_rate": round(len(newc) / len(young), 3) if young else None,
                    "share_kindle_unlimited": round(sum(1 for r in rs if r["kindle_unlimited"] == "True") / len(rs), 3),
                    "japan_fit_share": round(sum(1 for r in rs if r["anime_japan_kawaii_fit"] == "yes") / len(rs), 3),
                    "trend_term": tterm or "", "trend_direction_US_yoy": tdir, "trend_yoy_pct": tyoy})
    # opportunity score
    elig = [t for t in out if t["listings"] >= 5 and t["median_monthly_sales_est"] is not None]
    pd = pct_rank([t["median_monthly_sales_est"] for t in elig]); pr = pct_rank([t["median_reviews"] for t in elig])
    pv = pct_rank([t["median_velocity"] for t in elig])
    for t in out:
        if t not in elig:
            t["opportunity_score"] = None; continue
        demand = 0.6 * pd(t["median_monthly_sales_est"]) + 0.4 * pv(t["median_velocity"])
        barrier = pr(t["median_reviews"])
        dom = t["top3_sales_share_dominance"] or 0
        nr = t["newcomer_rate"] if t["newcomer_rate"] is not None else 0
        trend_adj = {"rising": 1.1, "declining": 0.9}.get(t["trend_direction_US_yoy"], 1.0)
        t["opportunity_score"] = round(100 * demand * (1 - 0.5 * barrier) * (0.6 + 0.4 * t["share_indie"]) * (1 - 0.3 * dom) * (0.85 + 0.3 * nr) * trend_adj, 1)
    out.sort(key=lambda t: -(t["opportunity_score"] or -1))
    for i, t in enumerate(out, 1): t["rank"] = i
    return out


SEG = table("segment"); NICHE = table("niche")
w("segment_table.csv", SEG, ["rank", "segment", "opportunity_score"] + [k for k in SEG[0] if k not in ("rank", "segment", "opportunity_score")])
w("niche_opportunity.csv", NICHE, ["rank", "niche", "segment", "opportunity_score"] + [k for k in NICHE[0] if k not in ("rank", "niche", "segment", "opportunity_score")])

# ---------------- velocity top 50 ----------------
V = [r for r in AMZ if r["_vel"] is not None and r["_age"] is not None and r["_age"] >= 14]
V.sort(key=lambda r: -r["_vel"])
VCOLS = ["product_id", "title", "author_or_brand", "publisher", "independently_published", "format", "segment", "niche", "price_usd_est", "review_count",
         "publication_date", "listing_age_days", "velocity_value", "bsr", "monthly_sales_est_bsr", "monthly_sales_est_thirdparty", "royalty_per_sale_est",
         "monthly_royalty_est", "anime_japan_kawaii_fit", "ip_risk", "link"]
for r in V: r["link"] = f"https://www.amazon.com/dp/{r['product_id']}" if r["marketplace"] == "amazon.com" else f"https://www.{r['marketplace']}/dp/{r['product_id']}"
w("velocity_top50.csv", V[:50], VCOLS)
VI = [r for r in V if r["_indie"]]
w("velocity_top50_indie.csv", VI[:50], VCOLS)
# low/medium-content KDP-type only (excludes fiction & trad nonfiction)
LC = {"coloring", "puzzle", "activity-kids", "journal", "planner", "logbook", "notebook", "workbook-education", "art-instruction"}
VL = [r for r in V if r["segment"] in LC]
w("velocity_top50_low_medium_content.csv", VL[:50], VCOLS)

# ---------------- price / page / trim ladder ----------------
lad = []
g = collections.defaultdict(list)
for r in AMZ: g[(r["segment"], r["format"])].append(r)
for (s, fm), rs in sorted(g.items()):
    if len(rs) < 3: continue
    lad.append({"segment": s, "format": fm, "n": len(rs), "price_p25": q([r["_price"] for r in rs], .25), "price_median": med(r["_price"] for r in rs),
                "price_p75": q([r["_price"] for r in rs], .75), "pages_p25": q([r["_pages"] for r in rs], .25), "pages_median": med(r["_pages"] for r in rs),
                "pages_p75": q([r["_pages"] for r in rs], .75), "royalty_per_sale_median_est": med(r["_roy"] for r in rs),
                "monthly_sales_median_est": med(r["_sales"] for r in rs), "monthly_royalty_median_est": med(r["_mroy"] for r in rs),
                "share_indie": round(sum(r["_indie"] for r in rs) / len(rs), 3)})
w("price_ladder.csv", lad)
# price bands: sales by price band within low/medium content paperbacks
pb = []
BANDS = [(0, 6.99), (7, 8.99), (9, 9.98), (9.99, 11.99), (12, 14.99), (15, 19.99), (20, 999)]
for s in sorted(set(r["segment"] for r in AMZ)):
    for lo, hi in BANDS:
        rs = [r for r in AMZ if r["segment"] == s and r["format"] in ("paperback", "spiral") and r["_price"] is not None and lo <= r["_price"] <= hi]
        if len(rs) >= 3:
            pb.append({"segment": s, "price_band": f"{lo}-{hi}", "n": len(rs), "median_monthly_sales_est": med(r["_sales"] for r in rs),
                       "median_royalty_per_sale_est": med(r["_roy"] for r in rs), "median_monthly_royalty_est": med(r["_mroy"] for r in rs)})
w("price_band_sales.csv", pb)
pgb = []
PB = [(1, 50), (51, 100), (101, 150), (151, 200), (201, 300), (301, 400), (401, 2000)]
for s in sorted(set(r["segment"] for r in AMZ)):
    for lo, hi in PB:
        rs = [r for r in AMZ if r["segment"] == s and r["_pages"] is not None and lo <= r["_pages"] <= hi and r["format"] != "kindle"]
        if len(rs) >= 3:
            pgb.append({"segment": s, "pages": f"{lo}-{hi}", "n": len(rs), "median_monthly_sales_est": med(r["_sales"] for r in rs),
                        "median_price": med(r["_price"] for r in rs), "median_royalty_per_sale_est": med(r["_roy"] for r in rs)})
w("page_count_sweetspots.csv", pgb)
tr = collections.defaultdict(list)
for r in AMZ:
    if r["trim_size"] != NS: tr[(r["segment"], r["trim_size"].split(" (")[0])].append(r)
w("trim_sizes.csv", [{"segment": s, "trim": t, "n": len(rs), "median_monthly_sales_est": med(r["_sales"] for r in rs)} for (s, t), rs in sorted(tr.items(), key=lambda x: -len(x[1]))])

# ---------------- indie vs trad by list ----------------
il = collections.defaultdict(list)
for r in AMZ:
    for v in r["query_or_category"].split(" | "):
        il[v].append(r)
w("indie_vs_trad_by_list.csv", sorted([{"list": k, "n": len(rs), "share_indie": round(sum(r["_indie"] for r in rs) / len(rs), 3),
                                         "share_independently_published_exact": round(sum(1 for r in rs if r["independently_published"] == "yes") / len(rs), 3)}
                                        for k, rs in il.items() if len(rs) >= 10], key=lambda x: -x["share_indie"]))

# ---------------- title words ----------------
STOP = set("the a an and of for to in with on by your my book books from at is it you this that are be as or vol volume edition series".split())
def words(rs, n=2):
    c = collections.Counter(); b = collections.Counter()
    for r in rs:
        toks = [t for t in re.findall(r"[a-z0-9']+", r["title"].lower()) if t not in STOP and len(t) > 1]
        c.update(set(toks)); b.update(set(" ".join(p) for p in zip(toks, toks[1:])))
    return c, b
c1, b1 = words(V[:300]); c2, b2 = words(VL[:300])
tw = [{"scope": "top300_velocity_all", "kind": "word", "term": k, "count": v} for k, v in c1.most_common(40)] + \
     [{"scope": "top300_velocity_all", "kind": "bigram", "term": k, "count": v} for k, v in b1.most_common(25)] + \
     [{"scope": "top300_velocity_low_medium_content", "kind": "word", "term": k, "count": v} for k, v in c2.most_common(40)] + \
     [{"scope": "top300_velocity_low_medium_content", "kind": "bigram", "term": k, "count": v} for k, v in b2.most_common(25)]
w("title_words.csv", tw)

# ---------------- cross-source overlap ----------------
src = collections.defaultdict(set)
for r in AMZ:
    for v in r["query_or_category"].split(" | "):
        src[r["product_id"]].add(v.split(":")[0].split("[")[0] if ":" in v else "amazon-direct")
ov = collections.Counter(tuple(sorted(s)) for s in src.values())
segm = collections.Counter((r["marketplace"], r["segment"]) for r in M)
w("cross_source_overlap.csv", [{"sources": "+".join(k), "products": v} for k, v in ov.most_common()] +
  [{"sources": f"segment_count:{m}:{s}", "products": v} for (m, s), v in sorted(segm.items())])

# ---------------- seasonality ----------------
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
seas = []
for (term, geo), d in sorted(TREND.items()):
    bym = collections.defaultdict(list)
    for dt, v in d["series"]:
        bym[int(dt[5:7])].append(v)
    avg = {m: statistics.mean(bym[m]) for m in bym}
    mean = statistics.mean(avg.values())
    idx = {m: round(100 * avg[m] / mean, 1) for m in avg}
    peak = max(idx, key=idx.get)
    row = {"term": term, "source": "google_trends_" + geo, "peak_month": MON[peak - 1], "peak_index": idx[peak],
           "publish_by": f"{MON[(peak - 3) % 12]} 15 (6-8 weeks before {MON[peak - 1]})", "yoy_pct": d["yoy_pct"], "last13w_vs_year_ago_pct": d["last13w_vs_year_ago_pct"], "vs_5y_ago_pct": d["vs_5y_ago_pct"]}
    row.update({MON[m - 1]: idx.get(m) for m in range(1, 13)}); seas.append(row)
for r in csv.DictReader(open(os.path.join(REPO, "raw", "etsy_rankhero_keywords_parsed.csv"))):
    s = json.loads(r["monthly_series"])
    if len(s) < 12: continue
    vals = {datetime.datetime.strptime(m, "%B %Y").month: v for m, v in s}
    if not vals or not any(vals.values()): continue
    mean = statistics.mean(vals.values())
    idx = {m: round(100 * v / mean, 1) for m, v in vals.items()}
    peak = max(idx, key=idx.get)
    row = {"term": r["keyword"], "source": "rankhero_etsy_monthly_searches(Oct2025-Sep2026)", "peak_month": MON[peak - 1], "peak_index": idx[peak],
           "publish_by": f"{MON[(peak - 3) % 12]} 15 (6-8 weeks before {MON[peak - 1]})", "yoy_pct": "", "vs_5y_ago_pct": ""}
    row.update({MON[m - 1]: idx.get(m) for m in range(1, 13)}); seas.append(row)
w("seasonality.csv", seas, ["term", "source", "peak_month", "peak_index", "publish_by", "yoy_pct", "last13w_vs_year_ago_pct", "vs_5y_ago_pct"] + MON)
# publication month of current bestsellers (when did today's sellers launch?)
pm = collections.defaultdict(collections.Counter)
for r in AMZ:
    m = re.match(r"([A-Z][a-z]+) \d{1,2}, (\d{4})", r["publication_date"])
    if m and r["_age"] is not None and r["_age"] < 3 * 365:
        pm[r["segment"]][m.group(1)[:3]] += 1
w("launch_month_of_current_bestsellers.csv", [{"segment": s, **{mo: c.get(mo, 0) for mo in MON}, "n": sum(c.values())} for s, c in sorted(pm.items())])

# ---------------- anime / Japan section ----------------
J = [r for r in M if r["anime_japan_kawaii_fit"] == "yes"]
jt = collections.defaultdict(list)
for r in J: jt[(r["marketplace"], r["segment"])].append(r)
w("anime_japan_segments.csv", sorted([{"marketplace": m, "segment": s, "n": len(rs), "median_price_usd": med(f(r["price_usd_est"]) for r in rs),
                                       "median_reviews": med(f(r["review_count"]) for r in rs), "median_monthly_sales_est": med((f(r["monthly_sales_est_bsr"]) or f(r["monthly_sales_est_thirdparty"])) for r in rs),
                                       "median_velocity": med(f(r["velocity_value"]) for r in rs),
                                       "share_ip_high": round(sum(1 for r in rs if r["ip_risk"].startswith("HIGH")) / len(rs), 3),
                                       "share_indie": round(sum(1 for r in rs if r["independently_published"].startswith(("yes", "likely"))) / len(rs), 3)}
                                      for (m, s), rs in jt.items()], key=lambda x: (-x["n"])))
J.sort(key=lambda r: -(f(r["velocity_value"]) or f(r["monthly_sales_est_bsr"]) or 0))
w("anime_japan_listings.csv", J, ["marketplace", "product_id", "title", "author_or_brand", "publisher", "independently_published", "format", "segment", "niche",
                                  "price_usd_est", "review_count", "rating", "bsr", "monthly_sales_est_bsr", "monthly_sales_est_thirdparty", "velocity_value",
                                  "publication_date", "ip_risk", "source_url"])

# ---------------- do-not-enter ----------------
dne = []
for t in NICHE:
    why = []
    if t["listings"] < 5: continue
    if (t["top3_sales_share_dominance"] or 0) >= 0.6: why.append(f"top-3 hold {int(100*t['top3_sales_share_dominance'])}% of est sales")
    if t["share_indie"] < 0.15: why.append(f"only {int(100*t['share_indie'])}% indie")
    if (t["median_reviews"] or 0) >= 5000: why.append(f"median {int(t['median_reviews'])} reviews (moat)")
    if t["newcomer_rate"] is not None and t["books_under_12mo"] >= 3 and t["newcomer_rate"] == 0: why.append("no newcomer under 12 months reached 50 reviews/300 sales")
    if t["trend_direction_US_yoy"] == "declining": why.append(f"Google Trends US {t['trend_yoy_pct']}% y/y")
    ipn = sum(1 for r in AMZ if r["niche"] == t["niche"] and r["ip_risk"].startswith("HIGH"))
    if ipn / t["listings"] >= 0.3: why.append(f"{ipn}/{t['listings']} titles use trademarked names")
    if len(why) >= 2 or any("trademarked" in x for x in why):
        dne.append({"niche": t["niche"], "segment": t["segment"], "listings": t["listings"], "reasons": "; ".join(why), "opportunity_score": t["opportunity_score"]})
w("do_not_enter.csv", dne)
print("segments", len(SEG), "niches", len(NICHE), "velocity", len(V), "anime", len(J), "dne", len(dne), "trend series", len(TREND))
