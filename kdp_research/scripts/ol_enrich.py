"""Open Library enrichment by ISBN-10 (= Amazon print ASIN). Keyless, 5-8 s pacing.
For each ISBN: /isbn/<isbn>.json (edition: publish_date, publishers, number_of_pages, physical_dimensions,
physical_format). Writes raw/enrich_openlibrary.csv incrementally; resumable."""
import csv, json, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
D = os.path.join(BASE, "pages", "openlibrary"); os.makedirs(D, exist_ok=True)
OUT = os.path.join(REPO, "raw", "enrich_openlibrary.csv")
F = ["isbn10", "http", "ol_key", "title", "publish_date", "publishers", "number_of_pages", "physical_dimensions",
     "physical_format", "subjects", "fetched_at", "source_url", "fetch_route"]


def candidates():
    c = {}
    p = os.path.join(REPO, "raw", "amazon_asinsight.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if r["asin"][0].isdigit():
                v = int(r["monthly_sales_est_thirdparty"]) if r["monthly_sales_est_thirdparty"].isdigit() else 0
                c[r["asin"]] = max(c.get(r["asin"], 0), v)
    p = os.path.join(REPO, "raw", "amazon_direct_lists.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if r["asin"][:1].isdigit(): c[r["asin"]] = max(c.get(r["asin"], 0), 10 ** 6)  # direct-list books first
    return [a for a, _ in sorted(c.items(), key=lambda x: -x[1])]


def main():
    done = set()
    if os.path.exists(OUT): done = {r["isbn10"] for r in csv.DictReader(open(OUT))}
    todo = [a for a in candidates() if a not in done]
    print("todo", len(todo), flush=True)
    for a in todo[: int(os.environ.get("OL_LIMIT", "2500"))]:
        url = f"https://openlibrary.org/isbn/{a}.json"
        fp = os.path.join(D, a + ".json")
        st, _ = fetch("openlibrary.org", url, fp, 5, 8, accept="application/json")
        row = {k: "NOT SHOWN" for k in F}
        row.update({"isbn10": a, "http": st, "fetched_at": utcnow(), "source_url": url, "fetch_route": "curl"})
        try:
            d = json.load(open(fp))
            row.update({"ol_key": d.get("key", "NOT SHOWN"), "title": d.get("title", "NOT SHOWN"),
                        "publish_date": d.get("publish_date", "NOT SHOWN"),
                        "publishers": "|".join(d.get("publishers", [])) or "NOT SHOWN",
                        "number_of_pages": d.get("number_of_pages", "NOT SHOWN"),
                        "physical_dimensions": d.get("physical_dimensions", "NOT SHOWN"),
                        "physical_format": d.get("physical_format", "NOT SHOWN"),
                        "subjects": "|".join(d.get("subjects", [])[:8]) or "NOT SHOWN"})
        except Exception:
            pass
        new = not os.path.exists(OUT)
        with open(OUT, "a", newline="") as f:
            w = csv.DictWriter(f, F)
            if new: w.writeheader()
            w.writerow(row)
        print(a, st, row["publish_date"], row["publishers"][:30], flush=True)


if __name__ == "__main__":
    try:
        main()
    except SiteBlocked as e:
        print("BLOCKED", e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE ol", flush=True)
