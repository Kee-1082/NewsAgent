# Daily News Digest AI Agent — Project Plan

## Goal
Build an automated AI agent that scrapes news from major media channels and social media, categorizes and summarizes them, and emails a daily digest to the user with "Read more" links to original sources.

## Requirements

### Functional
- Ingest articles from NewsAPI.org + RSS feeds of major Indian and international outlets
- Scrape article body text using `newspaper3k`
- Categorize each article into: `trending`, `financial`, `indian`, `international`, `social_media`, `technological`, `political`, `sports`
- Summarize each article into 2–3 sentences using an LLM
- Filter out low-confidence/unverified articles and unimportant sports
- Deduplicate articles by URL
- Assemble a formatted HTML email digest with category headers
- Include `[Read more]` hyperlinks back to original source for every article
- Send via email daily at 8:30 AM IST
- Sports section: only major events (World Cup finals, major tournament wins, record-breaking moments)

### Non-Functional
- Free to run (no server cost)
- Run on GitHub Actions cron schedule (2000 free min/month)
- Modular code for easy maintenance
- Secure: all secrets stored in GitHub Actions secrets, never hardcoded
- Authenticity checking via domain reputation scoring + cross-referencing

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Actions (cron)                      │
│  7:00 AM UTC (6:30 AM IST) — runs < 10 min                    │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                     main.py (orchestrator)               │  │
│  │                                                         │  │
│  │  fetch.py → extract.py → classify.py → summarize.py    │  │
│  │       → filter.py → assemble.py → email.py             │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Language | Python 3.11 | Rich ecosystem for scraping + LLM |
| News sources | NewsAPI.org + RSS feeds | Free tiers: 100 req/day + unlimited RSS |
| Article extraction | `newspaper3k` | Auto-extracts title, body, date, author |
| LLM API | OpenCode Go / Zen | Uses `deepseek-v4-flash-free` (free) or `kimi-k2.5` (Go sub, $10/mo) via OpenAI-compatible endpoint at `https://opencode.ai/zen/v1` |
| LLM SDK | `openai` Python SDK | OpenAI-compatible with custom `base_url` |
| Email | SendGrid via `sendgrid` SDK | 100 emails/day free tier |
| HTML templates | Jinja2 | Dynamic email rendering |
| Scheduling/Hosting | GitHub Actions | Free, cron trigger, secrets management |
| Data store | Local JSON files | Simple, zero-infrastructure, ephemeral per run |

## Key Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Delivery channel | Email (MVP) | Simpler than WhatsApp — no business approval needed |
| Hosting | GitHub Actions | Free, no server management, fits daily 10-min job within 2000 min/mo quota |
| LLM provider | OpenCode Go/Zen | User already uses OpenCode; free tier available; OpenAI-compatible API |
| Code structure | Modular (multi-file) | Easier to debug, modify categories, and test individual steps |
| Article storage | JSON files (no DB) | No persistent server needed; ephemeral per-run is simpler |
| Sports filtering | LLM-based + threshold | Only include if LLM deems it "major" with confidence > 5/10 |

## File Structure

```
daily-news-digest/
├── .github/workflows/daily-digest.yml   # 7 AM UTC cron
├── src/
│   ├── config.py          # Env vars, API keys, constants
│   ├── fetch.py           # NewsAPI + RSS ingestion
│   ├── extract.py         # newspaper3k → clean text
│   ├── classify.py        # LLM → category label
│   ├── summarize.py       # LLM → 2-3 sentence summary
│   ├── filter.py          # Dedup + domain reputation + confidence
│   ├── assemble.py        # Group, sort, render HTML via Jinja2
│   ├── email.py           # SendGrid email delivery
│   └── main.py            # Pipeline orchestrator
├── data/
│   ├── sources.json       # RSS URLs + domain trust scores
│   └── articles.json      # (auto-generated) cache
├── templates/
│   └── digest.html         # Jinja2 email template
├── .env.example            # Template for secrets
├── requirements.txt
└── README.md
```

## Build Timeline (3-Day Weekend)

### Day 1 — Friday Eve (3 hrs)
- [x] Scaffold project: virtualenv, `requirements.txt`, directory structure
- [ ] `config.py` — environment variable loading
- [ ] `fetch.py` — NewsAPI + RSS feed ingestion
- [ ] `extract.py` — article body extraction with `newspaper3k`
- **Milestone**: `python src/fetch.py` fetches and prints 30-40 raw articles

### Day 2 — Saturday Full Day (5 hrs)
- [ ] `classify.py` — LLM categorization via OpenCode API
- [ ] `summarize.py` — LLM summarization via OpenCode API
- [ ] `filter.py` — domain reputation scoring, dedup, low-confidence rejection
- [ ] `assemble.py` — Jinja2 HTML template with category headers + Read more links
- [ ] `digest.html` — Jinja2 template design (responsive, dark-mode friendly)
- **Milestone**: `python src/main.py` produces `digest.html` viewable in browser

### Day 3 — Sunday (4 hrs)
- [ ] `email.py` — SendGrid integration
- [ ] Local end-to-end test: full pipeline → email received on phone
- [ ] `.github/workflows/daily-digest.yml` — GitHub Actions workflow
- [ ] Store secrets in GitHub repo (OPENCODE_API_KEY, NEWSAPI_KEY, SENDGRID_API_KEY, EMAIL_TO, EMAIL_FROM)
- [ ] Push and trigger manual workflow
- [ ] Verify email arrives at 6:30 AM IST next day
- **Milestone**: `git push` → daily digest automated

## Secrets Required (GitHub Actions)

| Secret | Source |
|--------|--------|
| `OPENCODE_API_KEY` | opencode.ai → Account → API Keys |
| `NEWSAPI_KEY` | newsapi.org → Free signup (100 req/day) |
| `SENDGRID_API_KEY` | sendgrid.com → Free account → API Keys |
| `EMAIL_TO` | Your personal email address |
| `EMAIL_FROM` | Verified sender email in SendGrid |

## Planned Features (MVP Scope)

- [x] News ingestion from NewsAPI.org + 15+ RSS feeds
- [x] LLM-based categorization (8 categories)
- [x] LLM-based summarization (2-3 sentences)
- [x] Domain reputation scoring for authenticity
- [x] Deduplication by URL
- [x] Sports importance gate (only major events)
- [x] HTML email digest with Read more links
- [x] Daily cron automation via GitHub Actions

## Future Enhancements (Post-MVP)

- [ ] Twitter/X API integration for social media trends
- [ ] Reddit trends via PRAW
- [ ] WhatsApp delivery via Twilio
- [ ] Personalization — select/deselect categories
- [ ] Web dashboard to browse past digests
- [ ] Multi-user support

## Current Progress

- Planning complete ✅
- Architecture finalized ✅
- Tech stack chosen ✅
- **Build ready to start** — waiting for implementation go-ahead
