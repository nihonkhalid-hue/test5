"""Writes REPORT.md tables from the analysis CSVs (narrative sections come from scripts/recs.md)."""
import csv, collections, os, sys, statistics
sys.path.insert(0, os.path.dirname(__file__))
from netlib import REPO
csv.field_size_limit(10 ** 9)


def rd(p):
    p = os.path.join(REPO, p)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def tbl(rows, cols, hdr=None, n=None):
    rows = rows[:n] if n else rows
    out = ["| " + " | ".join(hdr or cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")).replace("|", "/")[:90] for c in cols) + " |")
    return "\n".join(out)


M = rd("master.csv"); N = rd("niche_opportunity.csv"); SEG = rd("segment_table.csv")
L = []
L.append(open(os.path.join(REPO, "scripts", "recs.md")).read() if os.path.exists(os.path.join(REPO, "scripts", "recs.md")) else "# REPORT\n")
L.append("\n## A. Top 20 niches by opportunity score\n")
L.append("Opportunity = 100 x demand x (1 - 0.5 x review-barrier pct) x (0.6 + 0.4 x indie share) x (1 - 0.3 x top-3 dominance) x (0.85 + 0.3 x newcomer rate) x trend factor (1.1 rising / 0.9 declining / 1.0). Demand = 0.6 x percentile(median est. monthly sales) + 0.4 x percentile(median review velocity). Only niches with 5+ Amazon books. Formula and inputs: COVERAGE.md.\n")
L.append(tbl([r for r in N if r["opportunity_score"]], ["rank", "niche", "segment", "opportunity_score", "listings", "median_price_usd", "median_pages", "median_reviews", "median_monthly_sales_est", "median_monthly_royalty_est", "share_indie", "top3_sales_share_dominance", "newcomer_rate", "trend_direction_US_yoy"], n=20))
L.append("\n### Segment overview\n")
L.append(tbl(SEG, ["rank", "segment", "opportunity_score", "listings", "median_price_usd", "median_pages", "median_reviews", "median_monthly_sales_est", "median_royalty_per_sale_est", "median_monthly_royalty_est", "share_indie", "median_velocity", "top3_sales_share_dominance", "newcomers_50rev_or_300sales", "books_under_12mo", "trend_direction_US_yoy", "trend_yoy_pct"]))
L.append("\n## B. Top 50 books by velocity (reviews per month since publication)\n")
for name, f in (("All Amazon books", "velocity_top50.csv"), ("Indie / likely-KDP only", "velocity_top50_indie.csv"), ("Low- and medium-content KDP formats only (coloring, puzzle, activity, journal, planner, logbook, notebook, workbook, art)", "velocity_top50_low_medium_content.csv")):
    V = rd(f)
    for r in V: r["title_link"] = f"[{r['title'][:70]}]({r['link']})"
    L.append(f"\n### {name}\n")
    L.append(tbl(V, ["title_link", "author_or_brand", "segment", "format", "price_usd_est", "review_count", "publication_date", "velocity_value", "bsr", "monthly_sales_est_bsr", "independently_published"], ["title", "author/brand", "segment", "format", "price $", "reviews", "published", "reviews/mo", "BSR", "est sales/mo", "indie"], n=50))
L.append("\n## C. Seasonality calendar\n")
S = rd("seasonality.csv")
L.append(tbl(S, ["term", "source", "peak_month", "peak_index", "publish_by", "yoy_pct", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]))
L.append("\nIndex = month average / yearly average x 100. Publish-by = at least 6-8 weeks before the peak (KDP review and indexing take up to 72 h; reviews and ranking need several weeks).\n")
LM = rd("launch_month_of_current_bestsellers.csv")
if LM:
    L.append("\n### Launch month of today's bestsellers (published in the last 3 years)\n")
    L.append(tbl(LM, ["segment", "n", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]))
L.append("\n## D. Price, page count and trim ladder with royalty estimates\n")
L.append(tbl(rd("price_ladder.csv"), ["segment", "format", "n", "price_p25", "price_median", "price_p75", "pages_median", "royalty_per_sale_median_est", "monthly_sales_median_est", "monthly_royalty_median_est", "share_indie"]))
L.append("\n### Paperback price bands (median est. sales by band)\n")
L.append(tbl(rd("price_band_sales.csv"), ["segment", "price_band", "n", "median_monthly_sales_est", "median_royalty_per_sale_est", "median_monthly_royalty_est"]))
L.append("\n### Page-count bands (print)\n")
L.append(tbl(rd("page_count_sweetspots.csv"), ["segment", "pages", "n", "median_monthly_sales_est", "median_price", "median_royalty_per_sale_est"]))
TR = rd("trim_sizes.csv")
if TR:
    L.append("\n### Trim sizes seen (from Amazon product pages / Open Library dimensions)\n"); L.append(tbl(TR, ["segment", "trim", "n", "median_monthly_sales_est"], n=25))
L.append("\n## E. Indie vs traditional share by list\n")
L.append(tbl(rd("indie_vs_trad_by_list.csv"), ["list", "n", "share_indie", "share_independently_published_exact"], n=60))
L.append("\n## F. Title words among top-velocity books\n")
TW = rd("title_words.csv")
for sc in ("top300_velocity_all", "top300_velocity_low_medium_content"):
    L.append(f"\n**{sc}**: " + ", ".join(f"{r['term']} ({r['count']})" for r in TW if r["scope"] == sc and r["kind"] == "word"))
    L.append(f"\nBigrams: " + ", ".join(f"{r['term']} ({r['count']})" for r in TW if r["scope"] == sc and r["kind"] == "bigram"))
L.append("\n\n### Cross-source overlap (Amazon books seen in more than one source)\n")
L.append(tbl([r for r in rd("cross_source_overlap.csv") if not r["sources"].startswith("segment_count")], ["sources", "products"]))
L.append("\n## G. Anime / manga / kawaii / cozy Japan / retro gaming\n")
L.append(tbl(rd("anime_japan_segments.csv"), ["marketplace", "segment", "n", "median_price_usd", "median_reviews", "median_monthly_sales_est", "median_velocity", "share_indie", "share_ip_high"]))
AJ = [r for r in rd("anime_japan_listings.csv") if r["marketplace"].startswith("amazon")]
L.append("\n### Amazon anime/Japan titles (sorted by velocity, then est. sales)\n")
for r in AJ: r["t"] = f"[{r['title'][:70]}](https://www.amazon.com/dp/{r['product_id']})" if r["marketplace"] == "amazon.com" else r["title"][:70]
L.append(tbl(AJ, ["t", "author_or_brand", "segment", "price_usd_est", "review_count", "monthly_sales_est_bsr", "monthly_sales_est_thirdparty", "velocity_value", "independently_published", "ip_risk"], ["title", "author", "segment", "price", "reviews", "est sales (BSR)", "est sales (ASINsight)", "reviews/mo", "indie", "IP risk"], n=40))
L.append("\n## H. Do NOT enter\n")
L.append(tbl(rd("do_not_enter.csv"), ["niche", "segment", "listings", "reasons"]))
open(os.path.join(REPO, "REPORT.md"), "w").write("\n".join(L) + "\n")
print("report written")
