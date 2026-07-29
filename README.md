Daily News Digest AI Agent

An automated AI-powered news digest pipeline that collects news from multiple sources, extracts and processes article content, categorizes and summarizes stories using an LLM, filters and ranks relevant articles, and delivers a personalized daily digest via Email and WhatsApp.

The entire pipeline runs automatically using GitHub Actions, eliminating the need for a dedicated server or hosting infrastructure.

🚀 Features
📰 Multi-source news ingestion
NewsAPI integration
RSS feeds from major Indian and international news outlets
15+ RSS sources
🧹 Article extraction
Extracts article body content using newspaper3k
Handles inaccessible or restricted articles gracefully
🤖 AI-powered processing
LLM-based article categorization
Automated article summarization
Generates concise 2–3 sentence summaries
🔍 Intelligent filtering
URL-based duplicate removal
Domain reputation scoring
Cross-source validation
Confidence-based filtering
🏆 Sports importance filtering
Filters out low-importance sports stories
Retains major sporting events based on LLM evaluation
📧 Email delivery
Generates an HTML-formatted digest
Sends daily digest using SendGrid
Includes "Read More" links to original sources
📱 WhatsApp delivery
Sends the daily digest through Twilio WhatsApp API
⏰ Automated scheduling
Runs daily through GitHub Actions cron
Currently scheduled for approximately 9:00 AM IST
🔐 Secure configuration
API keys and credentials stored using GitHub Actions Secrets
No credentials hardcoded in the source code
💰 Serverless and cost-efficient
No dedicated backend server required
Runs entirely through GitHub Actions
🏗️ Architecture
                    GitHub Actions
                  Daily Cron Schedule
                         │
                         ▼
                  ┌──────────────┐
                  │   main.py    │
                  │ Orchestrator │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   fetch.py   │
                  │ NewsAPI + RSS│
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  extract.py  │
                  │ Article Text │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ classify.py  │
                  │ LLM Category │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ summarize.py │
                  │ LLM Summary  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   filter.py  │
                  │ Dedup + Rank │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  assemble.py │
                  │ Digest Build │
                  └──────┬───────┘
                         │
                    ┌────┴────┐
                    ▼         ▼
               SendGrid    Twilio
                Email     WhatsApp
🛠️ Tech Stack
Component	Technology
Language	Python
News Ingestion	NewsAPI + RSS Feeds
Article Extraction	newspaper3k
AI / LLM	OpenCode API
LLM Model	DeepSeek V4 Flash Free
LLM SDK	OpenAI Python SDK
Email Delivery	SendGrid
WhatsApp Delivery	Twilio WhatsApp API
HTML Rendering	Jinja2
Automation	GitHub Actions
Data Storage	Local JSON
Configuration	Environment Variables
Secret Management	GitHub Actions Secrets
📁 Project Structure
daily-news-digest/
│
├── .github/
│   └── workflows/
│       └── daily-digest.yml       # GitHub Actions scheduled workflow
│
├── src/
│   ├── config.py                  # Environment variables and configuration
│   ├── fetch.py                   # NewsAPI + RSS ingestion
│   ├── extract.py                 # Article body extraction
│   ├── classify.py                # LLM-based categorization
│   ├── summarize.py               # LLM-based summarization
│   ├── filter.py                  # Deduplication and filtering
│   ├── assemble.py                # Digest assembly and HTML rendering
│   ├── email.py                   # SendGrid email delivery
│   ├── whatsapp.py                # Twilio WhatsApp delivery
│   └── main.py                    # Pipeline orchestrator
│
├── data/
│   ├── sources.json               # RSS sources and domain reputation data
│   └── articles.json              # Generated article data
│
├── templates/
│   └── digest.html                # HTML digest template
│
├── .env.example                   # Environment variable template
├── requirements.txt               # Python dependencies
└── README.md
⚙️ Pipeline Workflow

The pipeline executes the following steps:

1. News Ingestion

News is collected from:

NewsAPI
RSS feeds from major news organizations
Indian and international news sources

Articles are deduplicated and the most relevant stories are selected for processing.

2. Article Extraction

The pipeline attempts to extract the full article body using newspaper3k.

If an article cannot be accessed due to restrictions such as 403 Forbidden, the pipeline handles the failure gracefully and continues processing other sources.

3. AI Categorization

Each article is passed to an LLM to determine its category, such as:

Politics
Technology
Business
Science
World
India
Entertainment
Sports
4. AI Summarization

The LLM generates concise summaries of selected articles, allowing users to quickly understand the key information without reading the full article.

5. Filtering and Ranking

Articles are processed using:

URL deduplication
Domain reputation scores
Category filtering
Confidence-based filtering
Sports importance filtering

This reduces noise and prioritizes more relevant stories.

6. Digest Generation

The selected articles are assembled into a structured HTML digest using Jinja2 templates.

Each article includes a link to the original source.

7. Delivery

The final digest is delivered through:

📧 Email using SendGrid
📱 WhatsApp using Twilio
8. Automated Execution

GitHub Actions runs the entire pipeline automatically on a daily cron schedule.

The workflow securely injects API credentials through GitHub Repository Secrets.

🔐 Environment Variables

The following environment variables are required:

OPENCODE_API_KEY=
OPENCODE_BASE_URL=
OPENCODE_MODEL=

NEWSAPI_KEY=

SENDGRID_API_KEY=
EMAIL_TO=
EMAIL_FROM=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=
WHATSAPP_TO=

For local development, create a .env file based on .env.example.

For production execution through GitHub Actions, all credentials are stored securely as GitHub Repository Secrets.

⚠️ Never commit .env or real API keys to GitHub.

⏰ GitHub Actions Automation

The pipeline runs automatically using a scheduled GitHub Actions workflow.

Example:

on:
  schedule:
    - cron: "30 3 * * *"
  workflow_dispatch:

GitHub Actions uses UTC for cron schedules.

30 3 * * * corresponds to approximately 9:00 AM IST.

The workflow_dispatch trigger also allows the pipeline to be manually executed for testing.

📊 Example Pipeline Output
Daily News Digest - Starting pipeline

[1/6] Fetching articles...
[fetch] RSS returned 96 articles
[fetch] Dedup: 96 -> 85
       -> 30 articles fetched

[2/6] Extracting article bodies...
[extract] Enriched 30 articles

[3/6] Classifying articles...
[classify] Classified 30 articles

[4/6] Summarizing articles...
[summarize] Summarized 30 articles

[5/6] Filtering & ranking...
[filter] 30 -> 30 after filtering
[filter] 4 after category capping

       -> Saved 4 articles to data/articles.json

[6/6] Sending WhatsApp digest...
[whatsapp] Message sent successfully

[6/6] Sending Email digest...
[email] Email sent successfully

Pipeline complete!
🔒 Security

The project follows secure credential management practices:

API keys are never hardcoded
.env is excluded using .gitignore
Production credentials are stored in GitHub Repository Secrets
GitHub Actions injects credentials only during workflow execution
.env.example contains only placeholder values
