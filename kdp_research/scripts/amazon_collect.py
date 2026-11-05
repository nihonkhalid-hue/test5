"""Amazon direct (read-only, 20-30 s/request, stop for good at first CAPTCHA/403/429).
Phase 1: walk Best Sellers category tree (keyword-filtered), fetch BS p1+p2, New Releases,
Movers & Shakers, Most Wished For per node. Phase 2: product (dp) pages for ASINs found.
Only saves raw HTML + a node index; parsing is done by amazon_parse.py from the saved files."""
import csv, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO

MK = sys.argv[1]  # amazon.com / amazon.co.uk
PHASE = sys.argv[2] if len(sys.argv) > 2 else "all"
CAP_LISTS = int(os.environ.get("CAP_LISTS", "260")); CAP_DP = int(os.environ.get("CAP_DP", "450"))
D = os.path.join(BASE, "pages", MK.replace(".", "_")); os.makedirs(D, exist_ok=True)
IDX = os.path.join(D, "index.csv")
HOST = "https://www." + MK
DESCEND = re.compile(r"puzzle|game|word|sudoku|crossword|logic|brain|activit|colou?ring|journal|writing|diar|"
                     r"planner|notebook|calendar|romance|fantasy|paranormal|romantic|self-help|personal|happiness|"
                     r"motivation|mindful|cook|baking|teen|young adult|manga|comic|graphic|drawing|art |arts|craft|hobb|"
                     r"children|picture|education|workbook|handwriting|early learning|mystery|cozy|thriller|"
                     r"religion|christian|prayer|devotion|spiritual|humor|entertainment|kindle ebooks|"
                     r"reference|fiction|literature|anime|japan|stickers?|journals", re.I)
SEEDS = {"amazon.com": [("books", "Books", 0), ("digital-text/154606011", "Kindle eBooks", 0),
                        ("books/11357541011", "Coloring Books for Grown-Ups", 2)],
         "amazon.co.uk": [("books", "Books", 0), ("digital-text/341689031", "Kindle eBooks", 0)]}
LISTS = ["bestsellers", "new-releases", "movers-and-shakers", "most-wished-for"]
n_req = 0


def idx_write(row):
    new = not os.path.exists(IDX)
    with open(IDX, "a", newline="") as f:
        w = csv.DictWriter(f, ["fetched_at", "list", "node_path", "node_name", "depth", "page", "file", "url", "http"])
        if new: w.writeheader()
        w.writerow(row)


def get(lst, node, name, depth, page=1):
    global n_req
    fn = re.sub(r"\W+", "_", f"{lst}_{node}_p{page}") + ".html"
    fp = os.path.join(D, fn)
    if os.path.exists(fp) and os.path.getsize(fp) > 50000:
        return open(fp, encoding="utf-8", errors="ignore").read()
    url = f"{HOST}/gp/{lst}/{node}" + (f"?pg={page}" if page > 1 else "")
    st, _ = fetch(MK, url, fp, 20, 30); n_req += 1
    idx_write({"fetched_at": utcnow(), "list": lst, "node_path": node, "node_name": name, "depth": depth,
               "page": page, "file": fn, "url": url, "http": st})
    return open(fp, encoding="utf-8", errors="ignore").read()


def children(body, node, store):
    out = []
    cur = node.split("/")[-1]
    for href, txt in re.findall(r'<a[^>]*href="(/[^"]*zgbs/(?:books|digital-text)/\d+)[^"]*"[^>]*>(.*?)</a>', body, re.S):
        nid = href.split("/")[-1]; t = html.unescape(re.sub(r"<[^>]+>", "", txt)).strip()
        if nid == cur or not t or t.isdigit() or "page" in t.lower(): continue
        out.append((store + "/" + nid, t))
    return out


def phase_lists():
    seen, queue = set(), []
    for node, name, depth in SEEDS[MK]:
        queue.append((node, name, depth))
    ancestors = set()
    while queue and n_req < CAP_LISTS:
        node, name, depth = queue.pop(0)
        if node in seen: continue
        seen.add(node)
        body = get("bestsellers", node, name, depth)
        store = node.split("/")[0]
        kids = children(body, node, store)
        # children are links after the current-node in nav; parents appear before. Drop known nodes.
        for k, t in kids:
            if k in seen or k in ancestors: continue
            if depth < 4 and (DESCEND.search(t) or depth == 0 and store == "books" and False):
                queue.append((k, t, depth + 1))
        if depth == 0:
            continue  # root pages: only use for navigation + list
        get("bestsellers", node, name, depth, 2)
        for lst in LISTS[1:]:
            get(lst, node, name, depth)
        print(MK, "node", node, name, depth, "req", n_req, "queue", len(queue), flush=True)


def phase_dp():
    asins = []
    for fn in sorted(os.listdir(D), key=lambda f: (0 if f.startswith(("movers", "new-releases")) else 1, f)):
        if not fn.endswith(".html") or fn.startswith("dp_"): continue
        b = open(os.path.join(D, fn), encoding="utf-8", errors="ignore").read()
        m = re.search(r'data-client-recs-list="([^"]+)"', b)
        if not m: continue
        for it in json.loads(html.unescape(m.group(1)))[:20]:
            if it["id"] not in asins: asins.append(it["id"])
    print("dp candidates", len(asins), flush=True)
    done = 0
    for a in asins:
        if done >= CAP_DP: break
        fp = os.path.join(D, f"dp_{a}.html")
        done += 1
        if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
        url = f"{HOST}/dp/{a}"
        st, _ = fetch(MK, url, fp, 20, 30)
        idx_write({"fetched_at": utcnow(), "list": "dp", "node_path": a, "node_name": "", "depth": "",
                   "page": 1, "file": f"dp_{a}.html", "url": url, "http": st})
        print(MK, "dp", done, a, st, flush=True)


if __name__ == "__main__":
    try:
        if PHASE in ("all", "lists"): phase_lists()
        if PHASE in ("all", "dp"): phase_dp()
    except SiteBlocked as e:
        print("BLOCKED - stopping", MK, e, flush=True)
    except StopMorocco as e:
        print("STOP MOROCCO", e, flush=True)
    print("DONE", MK, n_req, flush=True)
