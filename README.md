# 📈 StockSage AI — AI-Powered Stock Analysis Chatbot

> Institutional-grade stock analysis for everyone — built on Dify.ai with real-time market data, technical indicators, and GenAI-powered investment reports. Free. Instant. No expertise needed.

![Dify](https://img.shields.io/badge/Built%20with-Dify.ai-blue)
![Alpha Vantage](https://img.shields.io/badge/API-Alpha%20Vantage-green)
![Finnhub](https://img.shields.io/badge/API-Finnhub-orange)
![LLM](https://img.shields.io/badge/LLM-GPT--4.1--mini-purple)
![Nodes](https://img.shields.io/badge/Workflow%20Nodes-10-darkblue)
![APIs](https://img.shields.io/badge/API%20Tools-4-teal)
![LLMs](https://img.shields.io/badge/LLM%20Nodes-5-violet)

---

## 🎯 Problem & Solution

**The Problem:** Retail investors, finance students, and beginner traders lack access to professional-grade stock analysis without expensive tools or deep financial expertise.

**The Solution:** StockSage AI — a Dify-powered chatbot that delivers real-time prices, RSI analysis, news sentiment, and a Buy/Hold/Sell recommendation in seconds.

**Target Users:**
- 📈 Retail Investors
- 🎓 Finance Students
- 📊 Beginner Traders

---

## 💬 What You Can Ask

```
"Give me a full analysis of Apple stock"
"Is Tesla a buy or sell right now?"
"What's Microsoft's RSI and what does it mean?"
"Analyze NVDA based on the latest news"
```

Each query returns a structured report covering:
- 📊 Real-time price and quote data (current, high, low, open, prev close)
- 📉 30-day price trend and RSI momentum indicator
- 📰 News sentiment analysis (Bullish / Bearish / Neutral + confidence %)
- 🎯 Short and medium-term price outlook
- ✅ Buy / Hold / Sell recommendation with reasoning
- ⚠️ Risk disclaimer

---

## 🏗️ Architecture

```
User Query
    ↓
[Node 01]  Extract Ticker — LLM maps "Apple" → AAPL
    ↓
[Node 02]  Calculate Date Range — Python code node (today & 7 days ago)
    ↓
┌──────────────────────────────────────────┐
│  [Node 03]  Parallel API Execution       │
│  ├── Fetch Live Quote      (Finnhub)     │
│  ├── Fetch Price History   (Alpha Vantage│
│  └── Fetch Company News    (Finnhub)     │
└──────────────────────────────────────────┘
    ↓
[Node 04]  Fetch RSI Indicator — Alpha Vantage (14-day)
    ↓
┌──────────────────────────────────────────┐
│  [Node 05-06]  Parallel LLM Analysis     │
│  ├── Sentiment Analysis LLM              │
│  └── Technical Analysis LLM             │
└──────────────────────────────────────────┘
    ↓
[Node 07]  Price Prediction & Investment Thesis — LLM
    ↓
[Node 08]  Final Report Generator — LLM (Markdown formatted)
    ↓
Structured Institutional-Grade Report
```

**Key Design Choices:**
- **Multi-node pipeline** — 10 specialized nodes, not one giant prompt
- **Parallel API execution** — quotes, history & news fetched simultaneously, cutting response time from ~6s to ~2s
- **Structured LLM output** — fixed format labels (SENTIMENT:, TREND:, RSI_SIGNAL:) ensure parseable, reliable data that chains into downstream nodes
- **Tool-augmented generation** — 4 custom API tools inject real-time market data into LLM context, grounding every claim in live data

---

## 🔧 Tech Stack

| Component | Tool |
|---|---|
| Workflow Orchestration | Dify.ai (no-code visual builder) |
| LLM | GPT-4.1-mini (OpenAI) |
| Real-time Quote & News | Finnhub API |
| Price History & RSI | Alpha Vantage API |
| Interface | Dify Chatbot |

---

## 🗂️ Workflow Nodes — Full Breakdown

| # | Node Name | Type | Input | Output |
|---|---|---|---|---|
| 1 | Start | Input | User message | `user_query` |
| 2 | Extract Ticker | LLM | `user_query` | `ticker` |
| 3 | Calculate Dates | Code (Python) | — | `today`, `week_ago` |
| 4 | Fetch Live Quote | Tool (Finnhub) | `ticker` | Quote JSON |
| 5 | Fetch Price History | Tool (Alpha Vantage) | `ticker` | 30-day OHLCV JSON |
| 6 | Fetch News | Tool (Finnhub) | `ticker`, dates | News articles JSON |
| 7 | Fetch RSI | Tool (Alpha Vantage) | `ticker` | RSI values JSON |
| 8 | Sentiment Analysis | LLM | News JSON | `sentiment_report` |
| 9 | Technical Analysis | LLM | RSI + Quote + History | `technical_report` |
| 10 | Price Prediction | LLM | Nodes 8 + 9 | `prediction_report` |
| 11 | Generate Final Report | LLM | All above | `final_report` |
| 12 | End | Output | `final_report` | Displayed to user |

---

## 🧠 GenAI Techniques Used

### 1. Structured Output Prompting
Every LLM node uses a fixed labeled format ensuring parseable outputs that chain reliably into downstream nodes:
```
SENTIMENT: [Bullish/Bearish/Neutral]
CONFIDENCE: [0-100%]
KEY_THEMES: [3 themes]
RISKS: [2 risks]
SUMMARY: [2-3 sentences]
```

### 2. Chained LLM Pipeline
5 LLM nodes feed sequentially — each specializes in exactly one task:
`Ticker Extraction → Sentiment → Technical → Prediction → Report`

### 3. Tool-Augmented Generation (RAG-like)
4 custom API tools inject live market data into LLM context, grounding every claim in real data rather than training knowledge.

### 4. Context Injection via Variables
Dify passes structured API outputs directly into downstream prompts using `{{node/output}}` variable syntax — zero manual parsing required.

---

## 🚀 How to Replicate

### Step 1 — Get Free API Keys

| API | Free Limit | Sign Up |
|---|---|---|
| Alpha Vantage | 25 calls/day (500/day after email verify) | https://alphavantage.co |
| Finnhub | 60 calls/minute | https://finnhub.io |
| OpenAI | Pay-as-you-go (~$0.001/run with gpt-4.1-mini) | https://platform.openai.com |

### Step 2 — Set Up Dify
1. Create a free account at https://dify.ai
2. Go to **Settings → Model Provider → OpenAI** → paste your API key
3. Set default model to `gpt-4.1-mini`

### Step 3 — Create the 4 Custom API Tools
Go to **Tools → Custom → Create Custom Tool** for each:

| Tool Name | API | Base URL | Auth Header |
|---|---|---|---|
| `get_stock_quote` | Finnhub | `https://finnhub.io/api/v1/quote` | `token` |
| `get_daily_prices` | Alpha Vantage | `https://www.alphavantage.co/query` | `apikey` |
| `get_rsi_indicator` | Alpha Vantage | `https://www.alphavantage.co/query` | `apikey` |
| `get_company_news` | Finnhub | `https://finnhub.io/api/v1/company-news` | `token` |

> See `config/tools_config.json` for exact parameter definitions for each tool.

### Step 4 — Import the Workflow
1. Go to **Dify Studio → Create App → Workflow**
2. Click **Import DSL** → upload `config/workflow_export.yml`
3. Re-link your API tools to the imported tool nodes

### Step 5 — Build the Chatbot
1. Create a new **Chatbot** app in Dify Studio
2. Paste the system prompt from `prompts/chatbot_system.md` into Instructions
3. Enable all 4 custom tools
4. Add opening message and suggested questions (see `config/chatbot_config.json`)
5. Click **Publish**

---

## ✅ What Worked / ⚠️ Challenges

### What Worked
- Dify's visual workflow made complex multi-step logic intuitive to build
- Parallel API execution cut response time from ~6s to ~2s
- Structured output prompts produced reliable, parseable LLM data
- Free API tiers fully sufficient for a functional prototype

### Challenges
- Alpha Vantage 25 req/day limit hit during rapid testing
- LLMs fabricated data when API calls returned empty responses
- Dify variable reference syntax is error-prone to configure
- Input validation gap — typos like `APPL` vs `AAPL` caused silent failures

### Future Work
- Error-handling guards to prevent LLM hallucination on empty API responses
- Portfolio mode — analyze multiple tickers in one query
- RAG layer integrating SEC filings for fundamental analysis
- Price alert notifications via Dify webhook integrations

---

## 📋 Sample Output

```markdown
# 📊 AAPL Stock Analysis — February 28, 2026

| Metric          | Value                  |
|-----------------|------------------------|
| Current Price   | $102.45 (+0.29%)       |
| Sentiment       | Bullish (78% confidence)|
| RSI (14-day)    | 58.3 — Neutral         |
| Recommendation  | BUY                    |

## 📰 Sentiment Analysis
SENTIMENT: Bullish
CONFIDENCE: 78%
KEY_THEMES: AI chip demand, Services revenue growth, iPhone upgrade cycle
...

## 📉 Technical Picture
TREND: Uptrend
RSI_SIGNAL: Neutral (58.3)
SUPPORT: $98.00 | RESISTANCE: $108.00
...

⚠️ This analysis is AI-generated for educational purposes only.
Not financial advice. Consult a licensed financial advisor.
```

See `sample_outputs/` for full AAPL and TSLA reports.

---

## 👥 Authors

**Raman Barnwal**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Raman%20Barnwal-blue)](https://linkedin.com/in/raman-barnwal-bhole81)
[![GitHub](https://img.shields.io/badge/GitHub-ramanbarnwalgit81-black)](https://github.com/ramanbarnwalgit81)
