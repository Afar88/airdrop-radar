#!/usr/bin/env python3
"""Airdrop Radar: scans Binance announcements and sorts campaigns into
FREE (post, quiz, check-in, challenge), CHEAP (hold a tiny balance or claim),
PAID (needs trading volume or deposits) and OTHER.

Usage:
  python3 radar.py                 # last 2 days, all tags
  python3 radar.py --days 7        # look back 7 days
  python3 radar.py --only free,cheap
  python3 radar.py --new           # only campaigns not seen on a previous run
  python3 radar.py --draft         # also print a Binance Square post for each FREE/CHEAP find
  python3 radar.py --md LATEST.md  # write a Markdown report
  python3 radar.py --json          # machine-readable output
Read-only: it never touches a wallet or places a trade.
"""
import argparse, json, os, sys, time, urllib.request

CATALOGS = {93: "Latest Activities", 128: "Airdrop", 48: "New Listings"}
API = ("https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
       "?type=1&pageNo=1&pageSize=20&catalogId={}")
LINK = "https://www.binance.com/en/support/announcement/detail/{}"
SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen.json")

FREE = ["write", "post", "square", "quiz", "word of the day", "check-in",
        "story", "challenge", "vote", "red packet", "learn", "creator", "pick", "referral"]
CHEAP = ["hold", "holders", "airdrop", "alpha points", "claim"]
PAID = ["trade", "trading", "deposit", "subscribe", "futures", "tournament",
        "competition", "convert", "stake", "launchpool", "volume"]
ORDER = {"FREE": 0, "CHEAP": 1, "OTHER": 2, "PAID": 3}
EMOJI = {"FREE": "🟢", "CHEAP": "🟡", "OTHER": "⚪", "PAID": "🔴"}


def fetch(cid, retries=2):
    req = urllib.request.Request(API.format(cid), headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)["data"]["catalogs"][0]["articles"]
        except Exception:
            if attempt == retries:
                raise
            time.sleep(2)


def classify(title):
    t = title.lower()
    if any(k in t for k in PAID):
        return "PAID"
    if any(k in t for k in CHEAP):
        return "CHEAP"
    if any(k in t for k in FREE):
        return "FREE"
    return "OTHER"


def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except (OSError, ValueError):
        return set()


def save_seen(codes):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(codes)[-500:], f)


def draft_post(c):
    how = ("It's free to join" if c["tag"] == "FREE"
           else "It only needs a tiny balance or points")
    return (f"🚨 New on Binance: {c['title']}\n\n"
            f"{how}. Here's how:\n"
            f"• Open the Binance app and search the campaign name\n"
            f"• Tap Join and follow the tasks on the page\n"
            f"• Check the deadline and region rules in the announcement\n\n"
            f"Full details: {c['url']}\n\n"
            f"Found with my Airdrop Radar 📡 Not financial advice. DYOR.\n"
            f"#Binance #Airdrop #CryptoRewards")


def scan(days):
    cutoff = (time.time() - days * 86400) * 1000
    seen, rows = set(), []
    for cid, name in CATALOGS.items():
        try:
            for a in fetch(cid):
                if a["releaseDate"] < cutoff or a["code"] in seen:
                    continue
                seen.add(a["code"])
                rows.append({
                    "tag": classify(a["title"]), "catalog": name, "title": a["title"],
                    "date": time.strftime("%Y-%m-%d", time.gmtime(a["releaseDate"] / 1000)),
                    "code": a["code"], "url": LINK.format(a["code"]),
                })
        except Exception as e:
            print(f"! {name}: {e}", file=sys.stderr)
    return sorted(rows, key=lambda r: (ORDER[r["tag"]], r["date"]), reverse=False)


def to_markdown(rows):
    out = [f"# Airdrop Radar\n\nUpdated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}\n",
           "| Tag | Date | Campaign |", "| --- | --- | --- |"]
    for r in rows:
        out.append(f"| {EMOJI[r['tag']]} {r['tag']} | {r['date']} | [{r['title']}]({r['url']}) |")
    if not rows:
        out.append("| — | — | Nothing new |")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description="Scan Binance for free and low-cost campaigns.")
    p.add_argument("days_pos", nargs="?", type=int, help=argparse.SUPPRESS)
    p.add_argument("--days", type=int, default=2)
    p.add_argument("--only", default="", help="comma list: free,cheap,other,paid")
    p.add_argument("--new", action="store_true", help="hide campaigns seen on earlier runs")
    p.add_argument("--draft", action="store_true", help="print a Square post per FREE/CHEAP find")
    p.add_argument("--md", metavar="FILE", help="write a Markdown report to FILE")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    days = a.days_pos or a.days

    rows = scan(days)
    if a.only:
        keep = {t.strip().upper() for t in a.only.split(",")}
        rows = [r for r in rows if r["tag"] in keep]
    if a.new:
        seen = load_seen()
        rows = [r for r in rows if r["code"] not in seen]
        save_seen(seen | {r["code"] for r in rows})

    if a.md:
        with open(a.md, "w") as f:
            f.write(to_markdown(rows))
    if a.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    if not rows:
        print("Nothing new on the radar.")
    for r in rows:
        print(f"{EMOJI[r['tag']]} [{r['tag']}] {r['date']} | {r['title']}\n        {r['url']}")
        if a.draft and r["tag"] in ("FREE", "CHEAP"):
            print("\n--- Square post draft ---\n" + draft_post(r) + "\n-------------------------\n")


if __name__ == "__main__":
    main()
