# Airdrop Radar

Scans Binance announcements (Latest Activities, Airdrop, New Listings) and tags each campaign:

- **FREE**: posting on Square, quizzes, check-ins, challenges, votes
- **CHEAP**: hold a tiny balance or claim with points
- **PAID**: needs trading volume, deposits, or subscriptions
- **OTHER**: everything else

## Run

```bash
python3 radar.py      # last 2 days
python3 radar.py 7    # last 7 days
```

No API key and no dependencies: Python 3 standard library only. Read-only: it never touches a wallet or places a trade.

Tags come from title keywords, so always open the announcement to confirm the real requirements.
