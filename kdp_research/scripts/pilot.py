"""Pilot: one request per source; records status in raw/pilot.csv."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from netlib import fetch, SiteBlocked, StopMorocco, utcnow, BASE, REPO
P = os.path.join(BASE, "pages", "pilot"); os.makedirs(P, exist_ok=True)
SRC = [
 ("amazon.com", "https://www.amazon.com/gp/bestsellers/books/11357541011", "A amazon direct"),
 ("amazon.co.uk", "https://www.amazon.co.uk/gp/bestsellers/books/", "A amazon direct"),
 ("amazon.de", "https://www.amazon.de/gp/bestsellers/books/", "A amazon direct"),
 ("amazon.ca", "https://www.amazon.ca/gp/bestsellers/books/", "A amazon direct"),
 ("asinsight.com", "https://www.asinsight.com/report/US/word-search-books-for-adults", "B asinsight"),
 ("openlibrary.org", "https://openlibrary.org/search.json?q=word+search+large+print&limit=5", "C enrichment"),
 ("googleapis.com", "https://www.googleapis.com/books/v1/volumes?q=intitle:gratitude+journal", "C enrichment"),
 ("kindlepreneur.com", "https://kindlepreneur.com/amazon-kdp-sales-rank-calculator/", "D third party"),
 ("tckpublishing.com", "https://www.tckpublishing.com/amazon-book-sales-calculator/", "D third party"),
 ("camelcamelcamel.com", "https://camelcamelcamel.com/product/B09VCYS41G", "D third party"),
 ("keepa.com", "https://keepa.com/", "D third party"),
 ("goodreads.com", "https://www.goodreads.com/list/show/1.Best_Books_Ever", "D third party"),
 ("bookbub.com", "https://www.bookbub.com/blog", "D third party"),
 ("bookbolt.io", "https://bookbolt.io/", "D third party"),
 ("kdspy.com", "https://www.kdspy.com/", "D third party"),
 ("reddit.com", "https://www.reddit.com/r/selfpublish/search.rss?q=low+content&restrict_sr=on&sort=top&t=year", "E demand"),
 ("gumroad.com", "https://gumroad.com/products/search?query=journal&from=0", "F comparison"),
 ("teacherspayteachers.com", "https://www.teacherspayteachers.com/browse?search=handwriting%20practice", "F comparison"),
 ("rankhero.com", "https://www.rankhero.com/keywords/printable-planner", "F comparison"),
 ("kdp.amazon.com", "https://kdp.amazon.com/en_US/help/topic/G201834340", "royalty constants"),
]
rows = []
for site, url, grp in SRC:
    out = os.path.join(P, site.replace(".", "_") + ".html")
    try:
        gap = (1, 2)
        st, b = fetch(site, url, out, *gap)
        note = "OK"
    except SiteBlocked as e:
        st, b, note = "BLOCKED", "", str(e)[:150]
    except StopMorocco as e:
        print("STOP MOROCCO", e); break
    size = os.path.getsize(out) if os.path.exists(out) else 0
    rows.append({"tested_at": utcnow(), "group": grp, "site": site, "url": url, "http_or_block": st, "bytes": size, "note": note})
    print(rows[-1], flush=True)
with open(os.path.join(REPO, "raw", "pilot.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)
