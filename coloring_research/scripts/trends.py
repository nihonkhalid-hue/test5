"""Google Trends via pytrends: one attempt, 60-90 s sleeps, stop at first 429/error."""
import csv, os, random, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from netlib import ip_check, utcnow, BASE, StopMorocco
from pytrends.request import TrendReq

RAW = os.path.join(BASE, "raw", "trends"); os.makedirs(RAW, exist_ok=True)
TERMS = ["coloring pages", "coloring book", "adult coloring", "bold and easy coloring", "cozy coloring",
         "kawaii coloring", "anime coloring", "mandala coloring", "christmas coloring pages",
         "halloween coloring pages", "printable coloring pages"] + sys.argv[1:]


def main():
    ip_check("new site trends.google.com")
    py = TrendReq(hl="en-US", tz=0, retries=0, backoff_factor=0)
    done = 0
    plan = [(t, "") for t in TERMS] + [(t, "US") for t in TERMS[:11]]
    for t, geo in plan:
        if True:
            out = os.path.join(RAW, f"{t.replace(' ', '_')}_{geo or 'WW'}.csv")
            if os.path.exists(out):
                continue
            try:
                py.build_payload([t], timeframe="today 5-y", geo=geo)
                df = py.interest_over_time()
            except Exception as e:
                with open(os.path.join(BASE, "raw", "fetch_log.csv"), "a") as f:
                    f.write(f"{utcnow()},trends.google.com,pytrends {t} {geo},ERR,0,BLOCKED {str(e)[:80]}\n")
                print("BLOCKED", t, geo, e, flush=True); return done
            df.to_csv(out); done += 1
            with open(os.path.join(BASE, "raw", "fetch_log.csv"), "a") as f:
                f.write(f"{utcnow()},trends.google.com,pytrends {t} {geo},200,{len(df)},\n")
            print("ok", t, geo, len(df), flush=True)
            time.sleep(random.uniform(120, 150))
    return done


if __name__ == "__main__":
    try:
        print("DONE trends", main())
    except StopMorocco as e:
        print("STOP MOROCCO", e)
