"""Fetch FindNiche pages for (listing_id, released) anchors to estimate Etsy listing age from ID."""
import csv, os, re, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, utcnow, BASE
RAW = os.path.join(BASE, "raw", "thirdparty")
paths = [l.strip() for l in open(os.path.join(RAW, "fn_anchor_paths.txt")) if l.strip()]
# spread across the ID range: sort by id and take every k-th
paths = sorted(set(paths), key=lambda p: int(re.search(r"-(\d+)$", p).group(1)))
step = max(1, len(paths) // 30)
sel = paths[::step][:32]
rows = []
for p in sel:
    out = os.path.join(RAW, "fn", "anchor_" + p.split("/")[-1][-40:] + ".html")
    try:
        st, b = fetch("findniche.com", "https://findniche.com" + p, out, 6, 9)
    except SiteBlocked as e:
        print("BLOCKED", e); break
    b = open(out, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Released\s*(?:<[^>]+>\s*)*(\d{4}-\d\d-\d\d)", b)
    rows.append({"listing_id": re.search(r"-(\d+)$", p).group(1), "released": m.group(1) if m else "",
                 "source_url": "https://findniche.com" + p, "fetched_at": utcnow()})
    print(rows[-1], flush=True)
    with open(os.path.join(RAW, "etsy_id_date_anchors.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)
