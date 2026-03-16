"""
Test script to verify Finnhub API connectivity.
Tests both real-time quote and company news endpoints.

Usage:
    pip install requests
    python test_finnhub.py
"""

import requests
import json
from datetime import datetime, timedelta

API_KEY = "YOUR_FINNHUB_API_KEY"
BASE_URL = "https://finnhub.io/api/v1"
TEST_SYMBOL = "AAPL"


def test_quote():
    print(f"\n{'='*50}")
    print(f"TEST: Real-Time Quote for {TEST_SYMBOL}")
    print('='*50)

    response = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": TEST_SYMBOL, "token": API_KEY}
    )
    data = response.json()

    if "c" in data and data["c"] > 0:
        print(f"✅ SUCCESS")
        print(f"   Current Price:  ${data['c']}")
        print(f"   Open:           ${data['o']}")
        print(f"   High:           ${data['h']}")
        print(f"   Low:            ${data['l']}")
        print(f"   Previous Close: ${data['pc']}")
        change = data['c'] - data['pc']
        change_pct = (change / data['pc']) * 100
        direction = "📈" if change >= 0 else "📉"
        print(f"   Change:         {direction} {change:+.2f} ({change_pct:+.2f}%)")
    elif data.get("c") == 0:
        print("⚠️  Market closed or symbol not found — returned 0 values")
        print("   Try during US market hours (9:30am–4:00pm ET, Mon–Fri)")
    else:
        print("❌ UNEXPECTED RESPONSE:")
        print(json.dumps(data, indent=2))


def test_company_news():
    print(f"\n{'='*50}")
    print(f"TEST: Company News for {TEST_SYMBOL} (last 7 days)")
    print('='*50)

    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    response = requests.get(
        f"{BASE_URL}/company-news",
        params={
            "symbol": TEST_SYMBOL,
            "from": week_ago,
            "to": today,
            "token": API_KEY
        }
    )
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        print(f"✅ SUCCESS — {len(data)} articles found ({week_ago} to {today})")
        print(f"\n   Top 3 Headlines:")
        for i, article in enumerate(data[:3], 1):
            print(f"   {i}. {article.get('headline', 'No headline')[:80]}...")
            print(f"      Source: {article.get('source', 'Unknown')} | "
                  f"Date: {datetime.fromtimestamp(article.get('datetime', 0)).strftime('%Y-%m-%d')}")
    elif isinstance(data, list) and len(data) == 0:
        print("⚠️  No news returned — try extending the date range to 14 days")
        print(f"   Date range used: {week_ago} to {today}")
    else:
        print("❌ UNEXPECTED RESPONSE:")
        print(json.dumps(data, indent=2)[:500])


if __name__ == "__main__":
    print("StockSage AI — Finnhub API Connectivity Test")
    print(f"Symbol: {TEST_SYMBOL}")
    print(f"API Key: {API_KEY[:6]}{'*' * max(0, len(API_KEY)-6)}")

    test_quote()
    test_company_news()

    print(f"\n{'='*50}")
    print("Done. If both tests passed, your Finnhub tools are ready.")
    print("Note: Free tier allows 60 API calls/minute.")
