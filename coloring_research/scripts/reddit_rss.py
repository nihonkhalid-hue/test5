"""Reddit search RSS (top of year) for demand signals. 25-30 s between requests."""
import csv, html, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE

RAW = os.path.join(BASE, "raw", "reddit")
os.makedirs(RAW, exist_ok=True)
PLAN = [(s, t) for s in ["adultcoloring", "ColoringBooks", "coloring"]
        for t in ["anime", "kawaii", "cozy", "bold easy", "mandala", "halloween", "christmas",
                  "japanese", "manga", "grayscale", "favorite book", "cute"]]
PLAN += [(s, "coloring") for s in ["AnimeSketch", "Kawaii", "manga", "animeart", "Procreate"]]


def main():
    rows = list(csv.DictReader(open(os.path.join(RAW, "reddit_signals.csv")))) if os.path.exists(os.path.join(RAW, "reddit_signals.csv")) else []
    done = {(r["subreddit"], r["term"]) for r in rows}
    for sub, term in PLAN:
        if (sub, term) in done: continue
        url = (f"https://www.reddit.com/r/{sub}/search.rss?q={urllib.parse.quote(term)}"
               "&restrict_sr=on&sort=top&t=year")
        out = os.path.join(RAW, re.sub(r"\W+", "_", f"{sub}_{term}") + ".xml")
        try:
            status, body = fetch("reddit.com", url, out, 90, 120, accept="application/atom+xml")
        except SiteBlocked as e:
            print("BLOCKED", e, flush=True); break
        entries = re.findall(r"<entry>(.*?)</entry>", body, re.S)
        ts = utcnow()
        for i, e in enumerate(entries, 1):
            g = lambda tag: html.unescape((re.search(f"<{tag}[^>]*>(.*?)</{tag}>", e, re.S) or [None, ""])[1])
            link = re.search(r'<link href="([^"]+)"', e)
            rows.append({"subreddit": sub, "term": term, "rank": i, "title": g("title"),
                         "author": re.sub(r"<[^>]+>", "", g("author")).strip(),
                         "published": g("published") or g("updated"),
                         "link": link.group(1) if link else "", "fetched_at": ts, "source_url": url})
        print(sub, term, status, len(entries), flush=True)
        with open(os.path.join(RAW, "reddit_signals.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, ["subreddit", "term", "rank", "title", "author", "published", "link",
                                   "fetched_at", "source_url"])
            w.writeheader(); w.writerows(rows)
    print("DONE reddit", len(rows))


if __name__ == "__main__":
    try:
        main()
    except StopMorocco as e:
        print("STOP MOROCCO", e)
