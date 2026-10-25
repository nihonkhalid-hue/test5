"""Polite read-only fetch helper: per-site pacing, IP safety check, block logging."""
import csv, json, os, random, subprocess, time, datetime, sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
BASE = "/tmp/claude-0/-home-user-test5/f1949923-2992-520a-80c3-c501569412ac/scratchpad"
LOG = os.path.join(BASE, "raw", "fetch_log.csv")
IPLOG = os.path.join(BASE, "raw", "ip_checks.csv")
BLOCK_MARKERS = ["captcha-delivery", "Enter the characters you see below", "opfcaptcha",
                 "Just a moment...", "cf-challenge", "challenge-platform",
                 "Pardon Our Interruption", "/errors/validateCaptcha"]


class SiteBlocked(Exception):
    pass


class StopMorocco(Exception):
    pass


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_last_ip = 0.0
_seen_sites = set()
_last_req = {}


def ip_check(reason):
    global _last_ip
    out = subprocess.run(["curl", "-s", "-m", "20", "https://ipinfo.io/json"],
                         capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
    except Exception:
        d = {"raw": out[:200]}
    new = not os.path.exists(IPLOG)
    with open(IPLOG, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["checked_at", "reason", "ip", "country", "org"])
        w.writerow([utcnow(), reason, d.get("ip"), d.get("country"), d.get("org")])
    _last_ip = time.time()
    org = (d.get("org") or "").lower()
    if (d.get("country") == "MA" or d.get("ip") == "197.146.42.124"
            or any(k in org for k in ["maroc", "morocco", "inwi", "wana", "itissalat"])):
        raise StopMorocco(json.dumps(d))
    return d


def _log(site, url, status, size, note):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["fetched_at", "site", "url", "http", "bytes", "note"])
        w.writerow([utcnow(), site, url, status, size, note])


def fetch(site, url, out_path, min_gap=6, max_gap=10, accept=None):
    """Fetch one URL with curl. Raises SiteBlocked on 403/429/challenge pages."""
    if site not in _seen_sites:
        ip_check("new site " + site)
        _seen_sites.add(site)
    elif time.time() - _last_ip > 1800:
        ip_check("30-min check")
    gap = random.uniform(min_gap, max_gap)
    wait = _last_req.get(site, 0) + gap - time.time()
    if wait > 0:
        time.sleep(wait)
    cmd = ["curl", "-sS", "--compressed", "-L", "-A", UA, "-m", "40",
           "-H", "Accept-Language: en-US,en;q=0.9",
           "-H", "Accept: " + (accept or "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
           "-o", out_path, "-w", "%{http_code}", url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    _last_req[site] = time.time()
    status = r.stdout.strip() or "000"
    size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    body = ""
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8", errors="ignore") as f:
            body = f.read(400000)
    marker = next((m for m in BLOCK_MARKERS if m in body), None)
    if status in ("403", "429") or (marker and size < 20000) or (marker == "opfcaptcha") or ("captcha" in body.lower() and size < 8000):
        _log(site, url, status, size, "BLOCKED " + (marker or ""))
        raise SiteBlocked(f"{site} {status} {marker} {url}")
    _log(site, url, status, size, r.stderr.strip()[:100])
    return status, body
