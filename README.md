![Airdrop Radar](assets/banner.png)

# 📡 Airdrop Radar

Find free and low-cost Binance campaigns before everyone else.

Airdrop Radar scans Binance's official announcements (Latest Activities, Airdrop, New Listings) and tags every campaign:

| Tag | Meaning |
| --- | --- |
| 🟢 FREE | Post on Square, quizzes, check-ins, challenges, votes |
| 🟡 CHEAP | Hold a tiny balance or claim with points |
| ⚪ OTHER | Needs a closer look |
| 🔴 PAID | Needs trading volume, deposits, or subscriptions |

👉 **Latest finds:** see [LATEST.md](LATEST.md), refreshed daily by GitHub Actions.

## Run it yourself

Needs only Python 3. No API keys, no installs.

```bash
python3 radar.py                       # last 2 days
python3 radar.py --days 7              # last 7 days
python3 radar.py --only free,cheap     # just the good stuff
python3 radar.py --new                 # only what you haven't seen yet
python3 radar.py --draft               # plus a ready-to-post Binance Square draft
python3 radar.py --md LATEST.md        # save a Markdown report
python3 radar.py --json                # for other tools
```

## Safety

Read-only. It never connects to a wallet, signs anything, or places a trade.
Tags come from title keywords, so always open the announcement to confirm requirements, deadlines, and region rules.

Not financial advice. DYOR.

Built by [@aviehub](https://x.com/aviehub).
