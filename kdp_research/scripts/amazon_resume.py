"""The ONE allowed Amazon resume per marketplace, after a 30+ min cooldown, at slower pacing (45-75 s).
Stops for good at the first CAPTCHA/403/429. Fetch order is by information value."""
import csv, html, os, re, sys, time, datetime
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE
MK = sys.argv[1]; NOT_BEFORE = sys.argv[2]  # e.g. 2026-11-05T03:15:00
HOST = "https://www." + MK
D = os.path.join(BASE, "pages", MK.replace(".", "_")); os.makedirs(D, exist_ok=True)
IDX = os.path.join(D, "index.csv")
L1 = {"amazon.com": [("86", "Humor & Entertainment"), ("4", "Children's Books"), ("48", "Crafts, Hobbies & Home"),
                     ("23", "Romance"), ("4736", "Self-Help"), ("6", "Cookbooks, Food & Wine"), ("28", "Teens"),
                     ("12290", "Christian Books & Bibles"), ("21", "Reference"), ("1", "Arts & Photography"),
                     ("4366", "Comics & Graphic Novels"), ("8975347011", "Education & Teaching"),
                     ("25", "Science Fiction & Fantasy"), ("18", "Mystery, Thriller & Suspense"),
                     ("3248857011", "Calendars"), ("20", "Parenting & Relationships"), ("22", "Religion & Spirituality"),
                     ("10", "Health, Fitness & Dieting"), ("17", "Literature & Fiction")],
      "amazon.co.uk": [("", "Books root")], "amazon.de": [("", "Books root")], "amazon.ca": [("", "Books root")]}
WANT = re.compile(r"puzzle|word|sudoku|crossword|activit|colou?ring|journal|writing|diar|planner|notebook|"
                  r"romance|fantasy|paranormal|romantic|self-help|happiness|motivation|cook|baking|manga|comic|"
                  r"drawing|craft|picture|workbook|handwriting|early learning|cozy|prayer|devotion|games", re.I)


def wait_until():
    t = datetime.datetime.fromisoformat(NOT_BEFORE).replace(tzinfo=datetime.timezone.utc)
    while datetime.datetime.now(datetime.timezone.utc) < t: time.sleep(20)


def get(lst, node, name, page=1):
    path = f"/gp/{lst}/books" + (f"/{node}" if node else "")
    fn = re.sub(r"\W+", "_", f"{lst}_books_{node}_p{page}") + ".html"
    fp = os.path.join(D, fn)
    if os.path.exists(fp) and os.path.getsize(fp) > 50000:
        return open(fp, encoding="utf-8", errors="ignore").read()
    url = HOST + path + (f"?pg={page}" if page > 1 else "")
    st, _ = fetch(MK, url, fp, 45, 75)
    new = not os.path.exists(IDX)
    with open(IDX, "a", newline="") as f:
        w = csv.DictWriter(f, ["fetched_at", "list", "node_path", "node_name", "depth", "page", "file", "url", "http"])
        if new: w.writeheader()
        w.writerow({"fetched_at": utcnow(), "list": lst, "node_path": "books/" + node, "node_name": name, "depth": "resume",
                    "page": page, "file": fn, "url": url, "http": st})
    print(MK, lst, node, name, page, st, flush=True)
    return open(fp, encoding="utf-8", errors="ignore").read()


def kids(b, node):
    out = []
    for h, t in re.findall(r'<a[^>]*href="(/[^"]*zgbs/books/\d+)[^"]*"[^>]*>(.*?)</a>', b, re.S):
        nid = h.split("/")[-1]; t = html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        if nid != node and t and not t.isdigit(): out.append((nid, t))
    return out


def main():
    wait_until()
    plan = list(L1[MK]); sub = []
    for node, name in plan:
        b = get("bestsellers", node, name)
        for nid, t in kids(b, node):
            if WANT.search(t) and nid not in [p[0] for p in plan + sub]: sub.append((nid, t))
    for node, name in sub:
        b = get("bestsellers", node, name)
        for nid, t in kids(b, node):
            if WANT.search(t) and nid not in [p[0] for p in plan + sub]: sub.append((nid, t))
        if len(sub) > 80: break
    for node, name in [("11357541011", "Coloring Books for Grown-Ups")] + sub[:40]:
        for lst in ("movers-and-shakers", "new-releases", "most-wished-for"):
            get(lst, node, name)
    for node, name in sub[:40]:
        get("bestsellers", node, name, 2)


if __name__ == "__main__":
    try:
        main()
    except SiteBlocked as e:
        print("BLOCKED (second block) - Amazon stopped for good:", MK, e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE", MK, flush=True)
