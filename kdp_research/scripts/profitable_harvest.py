"""profitable.app public KDP dataset pages (free page 1 only = 25 books per category x lens).
Book records carry ASIN, format, publisher, publishedAt, printLength, all BSR category placements,
bsrTop, likelyKdp, KU flag, price, rating, ratingCount and the site's monthlyRevenue estimate.
Categories are discovered from the books' bestSubCategoryNodeId (BFS, KDP-relevant names first).
Never requests page 2+ (paywalled). 7-10 s pacing. Resumable."""
import csv, heapq, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
D = os.path.join(BASE, "pages", "profitable"); os.makedirs(D, exist_ok=True)
OUT = os.path.join(REPO, "raw", "profitable_books.csv"); COUT = os.path.join(REPO, "raw", "profitable_category_views.csv")
CAP = int(os.environ.get("PROF_CAP", "1500"))
INSIGHTS = ["", "new-trending", "top-kdp", "hidden-gems"]
HOT = re.compile(r"colou?ring|puzzle|word search|sudoku|crossword|activit|journal|diar|planner|notebook|writing|"
                 r"logic|brain|games|craft|hobb|drawing|manga|anime|comic|graphic novel|children|picture|early learning|"
                 r"workbook|handwriting|education|teen|young adult|romance|romantasy|fantasy|cozy|mystery|self-help|"
                 r"happiness|motivation|mindful|cook|baking|recipe|christian|prayer|devotion|bible|humor|stickers?|"
                 r"art|calendar|reference|parenting|horror|paranormal|dark|erotica|litrpg|kawaii|japan", re.I)
SEEDS = [("48", "Crafts, Hobbies & Home"), ("11357541011", "Coloring Books for Grown-Ups"), ("86", "Humor & Entertainment"),
         ("4", "Children's Books"), ("4736", "Self-Help"), ("23", "Romance"), ("6", "Cookbooks, Food & Wine"),
         ("28", "Teens"), ("12290", "Christian Books & Bibles"), ("21", "Reference"), ("1", "Arts & Photography"),
         ("4366", "Comics & Graphic Novels"), ("8975347011", "Education & Teaching"), ("25", "Science Fiction & Fantasy"),
         ("18", "Mystery, Thriller & Suspense"), ("3248857011", "Calendars"), ("20", "Parenting & Relationships"),
         ("22", "Religion & Spirituality"), ("10", "Health, Fitness & Dieting"), ("17", "Literature & Fiction"),
         ("158566011", "Romance (Kindle)"), ("668010011", "SF&F (Kindle)"), ("157028011", "Literature & Fiction (Kindle)"),
         ("158569011", "Romantasy (Kindle)")]


def payload(fp):
    b = open(fp, encoding="utf-8", errors="ignore").read()
    out = []
    for c in re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', b, re.S):
        try: out.append(json.loads('"' + c + '"'))
        except Exception: pass
    return "".join(out)


def parse(fp):
    s = payload(fp)
    m = re.search(r'"activeCategory":', s)
    cat = None
    if m:
        try: cat, _ = json.JSONDecoder().raw_decode(s[m.end():])
        except Exception: cat = None
    i = s.find('"currentPage":1,"data":[')
    if i < 0: return cat, [], None
    data, _ = json.JSONDecoder().raw_decode(s[i + len('"currentPage":1,"data":'):])
    tot = re.search(r'"pageSize":25,"total":(\d+)', s[i:])
    return cat, data, tot.group(1) if tot else "NOT SHOWN"


KEYS = ["asin", "tree", "url", "title", "subtitle", "author", "format", "publisher", "publishedAt", "printLength",
        "bestSubCategoryNodeId", "bestSubCategoryName", "bestSubCategoryRank", "allPlacementsText", "monthlyRevenue",
        "categoryRank", "categoryRankName", "language", "likelyKdp", "isKindleUnlimited", "priceUsd", "bsrTop",
        "bsrTopCategory", "rating", "ratingCount", "relatedEditions"]


def main():
    done = set()
    if os.path.exists(COUT):
        done = {(r["node_id"], r["insight"]) for r in csv.DictReader(open(COUT))}
    pq, seen, names = [], set(), {}
    def push(nid, name, base):
        if nid and nid not in seen:
            seen.add(nid); names[nid] = name
            heapq.heappush(pq, (base - (5 if HOT.search(name or "") else 0), len(seen), nid))
    for k, (nid, nm) in enumerate(SEEDS): push(nid, nm, -10 + k * 0.01)
    views = [("ROOT", ins) for ins in INSIGHTS + ["ku-goldmines"]]
    n = 0
    def do(nid, ins):
        nonlocal n
        q = ([f"category={nid}"] if nid != "ROOT" else []) + ([f"insight={ins}"] if ins else [])
        url = "https://profitable.app/kdp" + ("?" + "&".join(q) if q else "")
        fp = os.path.join(D, re.sub(r"\W+", "_", f"{nid}_{ins or 'all'}") + ".html")
        if (nid, ins) in done and os.path.exists(fp):
            cat, data, tot = parse(fp); return data
        st, _ = fetch("profitable.app", url, fp, 7, 10); n += 1
        cat, data, tot = parse(fp); ts = utcnow()
        rows = []
        for r_i, b in enumerate(data, 1):
            row = {"view_node_id": nid, "view_node_name": (cat or {}).get("name", "ROOT") if isinstance(cat, dict) else "ROOT",
                   "view_tree": (cat or {}).get("tree", "") if isinstance(cat, dict) else "", "insight": ins or "all",
                   "rank_on_page": r_i}
            for k in KEYS:
                v = b.get(k, "NOT SHOWN")
                row[k] = json.dumps(v) if isinstance(v, (dict, list)) else ("NOT SHOWN" if v in (None, "") and k not in ("subtitle",) else v)
            row.update({"fetched_at": ts, "source_url": url, "fetch_route": "third_party:profitable.app"})
            rows.append(row)
        if rows:
            new = not os.path.exists(OUT)
            with open(OUT, "a", newline="") as f:
                w = csv.DictWriter(f, list(rows[0].keys()))
                if new: w.writeheader()
                w.writerows(rows)
        c = cat if isinstance(cat, dict) else {}
        new = not os.path.exists(COUT)
        with open(COUT, "a", newline="") as f:
            w = csv.DictWriter(f, ["node_id", "insight", "http", "name", "tree", "parent_id", "level", "full_path",
                                   "books_in_view_total", "rows", "fetched_at", "source_url"])
            if new: w.writeheader()
            w.writerow({"node_id": nid, "insight": ins, "http": st, "name": c.get("name", "ROOT" if nid == "ROOT" else "NOT SHOWN"),
                        "tree": c.get("tree", ""), "parent_id": c.get("parent_id", ""), "level": c.get("level", ""),
                        "full_path": c.get("full_path", ""), "books_in_view_total": tot, "rows": len(rows),
                        "fetched_at": ts, "source_url": url})
        print(n, nid, names.get(nid, ""), ins or "all", st, len(rows), tot, flush=True)
        if c.get("parent_id"): push(c["parent_id"], "parent of " + c.get("name", ""), 5)
        return data
    for nid, ins in views:
        do(nid, ins)
    while pq and n < CAP:
        _, _, nid = heapq.heappop(pq)
        data = do(nid, "")
        if not data: continue
        for b in data:
            push(str(b.get("bestSubCategoryNodeId") or ""), b.get("bestSubCategoryName") or "", 0)
        hot = HOT.search(names.get(nid, "")) is not None
        for ins in (INSIGHTS[1:] if hot else INSIGHTS[1:2]):
            do(nid, ins)


if __name__ == "__main__":
    try:
        main()
    except SiteBlocked as e:
        print("BLOCKED", e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE profitable", flush=True)
