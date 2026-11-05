"""Writes COVERAGE.md from raw files, fetch log, ip checks, verification."""
import csv, collections, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from netlib import REPO
csv.field_size_limit(10 ** 9)
R = os.path.join(REPO, "raw"); NS = "NOT SHOWN"


def rd(p):
    p = os.path.join(REPO, p)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


M = rd("master.csv"); FL = rd("raw/fetch_log.csv"); IP = rd("raw/ip_checks.csv"); PI = rd("raw/pilot.csv"); V = rd("verification.csv")
L = []
L.append("# COVERAGE — KDP market research\n")
L.append(f"_Collection 2026-11-05 UTC from a cloud container. IP checks: {len(IP)} (countries {dict(collections.Counter(r['country'] for r in IP))}; orgs {dict(collections.Counter(r['org'] for r in IP))}). Never MA, never a Moroccan ISP, never 197.146.42.124._\n")
L.append("## Pilot (one request per source, 2026-11-05 02:40 UTC)\n\n| Group | Site | URL | Result | Bytes |\n|---|---|---|---|---|")
for r in PI: L.append(f"| {r['group']} | {r['site']} | {r['url']} | {r['http_or_block']} | {r['bytes']} |")
L.append("\nPilot notes: amazon.com and amazon.co.uk returned real pages on the first request; amazon.de and amazon.ca returned the small CAPTCHA page; Google Books API returned 429 `RESOURCE_EXHAUSTED` with `quota_limit_value: 0` for the shared keyless project (not retried); camelcamelcamel, BookBub and Book Bolt returned Cloudflare/403; the ASINsight 404 was a non-existent slug, not a block.\n")
L.append("## Rows per source (master.csv, one row per product per marketplace)\n\n| Marketplace | Master rows | Route(s) |\n|---|---|---|")
by = collections.defaultdict(collections.Counter)
for r in M: by[r["marketplace"]][r["fetch_route"]] += 1
for mk, c in sorted(by.items(), key=lambda x: -sum(x[1].values())):
    L.append(f"| {mk} | {sum(c.values())} | " + "; ".join(f"{k} ({v})" for k, v in c.items()) + " |")
L.append(f"\n**Total master rows: {len(M)}**\n")
L.append("## Raw collection counts (before de-duplication; every collected row kept in raw/)\n")
for f in sorted(os.listdir(R)):
    if f.endswith(".csv"):
        n = len(rd("raw/" + f)); L.append(f"- raw/{f}: {n} rows")
gt = os.listdir(os.path.join(R, "google_trends")) if os.path.exists(os.path.join(R, "google_trends")) else []
L.append(f"- raw/google_trends/: {len(gt)} series ({', '.join(sorted(gt))})")
L.append("\n## Requests per site\n")
c = collections.Counter(r["site"] for r in FL)
L.append(", ".join(f"{k} {v}" for k, v in c.most_common()) + f". Total logged requests: {len(FL)}.\n")
L.append("## Blocked / failed URLs (every BLOCKED or HTTP>=400 line of fetch_log.csv)\n\n| Time (UTC) | Site | URL | HTTP | Note |\n|---|---|---|---|---|")
nb = 0
for r in FL:
    if "BLOCKED" in r["note"] or (r["http"].isdigit() and int(r["http"]) >= 400 and r["site"] not in ("asinsight.com", "openlibrary.org")):
        L.append(f"| {r['fetched_at']} | {r['site']} | {r['url'][:110]} | {r['http']} | {r['note'][:70]} |"); nb += 1
a404 = sum(1 for r in FL if r["site"] == "asinsight.com" and r["http"] == "404")
o404 = sum(1 for r in FL if r["site"] == "openlibrary.org" and r["http"] == "404")
L.append(f"\nNot listed above: {a404} ASINsight 404s (sitemap slugs with no live report) and {o404} Open Library 404s (ISBN not in Open Library). These are missing pages, not blocks.\n")
L.append("## Fields missing per source (share of master rows NOT SHOWN / blank)\n")
F = ["price", "rating", "review_count", "bsr", "publisher", "publication_date", "page_count", "trim_size", "monthly_sales_est_bsr", "monthly_sales_est_thirdparty"]
L.append("| Marketplace / route | n | " + " | ".join(F) + " |\n|---|---|" + "---|" * len(F))
g = collections.defaultdict(list)
for r in M: g[(r["marketplace"], r["fetch_route"])].append(r)
for (mk, rt), rs in sorted(g.items(), key=lambda x: -len(x[1])):
    L.append(f"| {mk} / {rt} | {len(rs)} | " + " | ".join(f"{round(100*sum(1 for r in rs if r[k] in (NS, '', 'None'))/len(rs))}%" for k in F) + " |")
L.append("\n## Verification (random 5% of master rows, seed 42)\n")
if V:
    c1 = collections.Counter(x["reparse_status"].split(" ")[0] for x in V); c2 = collections.Counter(x["live_status"].split(" ")[0] for x in V)
    rp = [x for x in V if x["reparse_status"] in ("match",) or x["reparse_status"].startswith("MISMATCH")]
    lv = [x for x in V if x["live_status"] == "match" or x["live_status"].startswith("DRIFT")]
    L.append(f"Sample: {len(V)} rows. Step 1 (re-parse the saved page, tests the pipeline): {dict(c1)}; mismatch rate {round(100*sum(1 for x in rp if x['reparse_status'].startswith('MISMATCH'))/max(1,len(rp)),1)}% of {len(rp)} checkable rows.")
    L.append(f"Step 2 (live re-fetch now, tests real drift): {dict(c2)}; value drift {round(100*sum(1 for x in lv if x['live_status'].startswith('DRIFT'))/max(1,len(lv)),1)}% of {len(lv)} rows still on the page; rows that left the page = rank drift.")
    L.append("Per-row results: verification.csv.\n")
open(os.path.join(REPO, "COVERAGE_auto.md"), "w").write("\n".join(L))
print("coverage written", nb, "blocked lines")
