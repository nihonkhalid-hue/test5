"""Google Trends via pytrends: 5-year weekly, WW then US. 90-120 s sleeps; stop at first 429/error."""
import os, random, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from netlib import ip_check, utcnow, REPO, StopMorocco, LOG
from pytrends.request import TrendReq
RAW = os.path.join(REPO, "raw", "google_trends"); os.makedirs(RAW, exist_ok=True)
TERMS = ["word search", "sudoku book", "coloring book", "gratitude journal", "planner", "puzzle book",
         "activity book", "journal", "romantasy", "dark romance", "cozy mystery", "self help books",
         "cookbook", "how to draw anime", "kawaii", "sketchbook", "password book", "handwriting practice",
         "bold and easy coloring", "low content books"]


def log(term, geo, st, n, note=""):
    with open(LOG, "a") as f:
        f.write(f"{utcnow()},trends.google.com,pytrends {term} {geo},{st},{n},{note}\n")


def main():
    ip_check("new site trends.google.com")
    py = TrendReq(hl="en-US", tz=0, retries=0, backoff_factor=0)
    for geo in ("", "US"):
        for t in TERMS:
            out = os.path.join(RAW, f"{t.replace(' ', '_')}_{geo or 'WW'}.csv")
            if os.path.exists(out): continue
            try:
                py.build_payload([t], timeframe="today 5-y", geo=geo)
                df = py.interest_over_time()
            except Exception as e:
                log(t, geo, "ERR", 0, "BLOCKED " + str(e)[:80].replace(",", ";")); print("BLOCKED", t, geo, e, flush=True); return
            df.to_csv(out); log(t, geo, 200, len(df)); print("ok", t, geo, len(df), flush=True)
            time.sleep(random.uniform(90, 120))


if __name__ == "__main__":
    try:
        main()
    except StopMorocco as e:
        print("STOP MOROCCO", e)
    print("DONE trends")
