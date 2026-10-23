#!/usr/bin/env python3
"""Airdrop Radar: scans Binance announcements and sorts campaigns into
FREE (post, quiz, check-in, share), CHEAP (hold a tiny balance), and PAID
(needs trading volume or deposits). Prints only campaigns from the last N days."""
import json, sys, time, urllib.request

CATALOGS = {93: "Latest Activities", 128: "Airdrop", 48: "New Listings"}
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
API = ("https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
       "?type=1&pageNo=1&pageSize=20&catalogId={}")
LINK = "https://www.binance.com/en/support/announcement/detail/{}"

FREE = ["write", "post", "square", "quiz", "word of the day", "check-in",
        "story", "challenge", "vote", "red packet", "learn", "creator", "pick", "referral"]
CHEAP = ["hold", "holders", "airdrop", "alpha points", "claim"]
PAID = ["trade", "trading", "deposit", "subscribe", "futures", "tournament",
        "competition", "convert", "stake", "launchpool", "volume"]

def fetch(cid):
    req = urllib.request.Request(API.format(cid), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]["catalogs"][0]["articles"]

def classify(title):
    t = title.lower()
    if any(k in t for k in PAID):
        return "PAID"
    if any(k in t for k in CHEAP):
        return "CHEAP"
    if any(k in t for k in FREE):
        return "FREE"
    return "OTHER"

def main():
    cutoff = (time.time() - DAYS * 86400) * 1000
    seen, rows = set(), []
    for cid, name in CATALOGS.items():
        try:
            for a in fetch(cid):
                if a["releaseDate"] < cutoff or a["code"] in seen:
                    continue
                seen.add(a["code"])
                rows.append((classify(a["title"]), name, a["title"],
                             time.strftime("%Y-%m-%d", time.gmtime(a["releaseDate"] / 1000)),
                             LINK.format(a["code"])))
        except Exception as e:
            print(f"! {name}: {e}", file=sys.stderr)
    order = {"FREE": 0, "CHEAP": 1, "OTHER": 2, "PAID": 3}
    for tag, cat, title, date, url in sorted(rows, key=lambda r: order[r[0]]):
        print(f"[{tag}] {date} | {title}\n        {url}")

if __name__ == "__main__":
    main()
