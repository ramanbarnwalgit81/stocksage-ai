"""
Test script to verify Alpha Vantage API connectivity.
Tests both TIME_SERIES_DAILY and RSI endpoints.

Usage:
    pip install requests
    python test_alpha_vantage.py
"""

import requests
import json

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"
TEST_SYMBOL = "AAPL"


def test_daily_prices():
    print(f"\n{'='*50}")
    print(f"TEST: Daily Price History for {TEST_SYMBOL}")
    print('='*50)

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": TEST_SYMBOL,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        dates = list(data["Time Series (Daily)"].keys())
        latest = dates[0]
        latest_data = data["Time Series (Daily)"][latest]
        print(f"✅ SUCCESS — Latest trading day: {latest}")
        print(f"   Open:  ${latest_data['1. open']}")
        print(f"   High:  ${latest_data['2. high']}")
        print(f"   Low:   ${latest_data['3. low']}")
        print(f"   Close: ${latest_data['4. close']}")
        print(f"   Volume: {latest_data['5. volume']}")
        print(f"   Total days returned: {len(dates)}")
    elif "Note" in data:
        print("⚠️  RATE LIMIT HIT — Alpha Vantage free tier: 25 calls/day")
        print(f"   Message: {data['Note']}")
    elif "Error Message" in data:
        print(f"❌ ERROR: {data['Error Message']}")
        print("   → Check your API key and symbol")
    else:
        print("❌ UNEXPECTED RESPONSE:")
        print(json.dumps(data, indent=2)[:500])


def test_rsi():
    print(f"\n{'='*50}")
    print(f"TEST: RSI Indicator for {TEST_SYMBOL}")
    print('='*50)

    params = {
        "function": "RSI",
        "symbol": TEST_SYMBOL,
        "interval": "daily",
        "time_period": "14",
        "series_type": "close",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Technical Analysis: RSI" in data:
        dates = list(data["Technical Analysis: RSI"].keys())
        latest = dates[0]
        rsi_value = data["Technical Analysis: RSI"][latest]["RSI"]
        rsi_float = float(rsi_value)
        print(f"✅ SUCCESS — Latest RSI ({latest}): {rsi_value}")

        if rsi_float > 70:
            print(f"   📊 Signal: OVERBOUGHT (RSI > 70) — potential sell signal")
        elif rsi_float < 30:
            print(f"   📊 Signal: OVERSOLD (RSI < 30) — potential buy signal")
        else:
            print(f"   📊 Signal: NEUTRAL (30 < RSI < 70)")
    elif "Note" in data:
        print("⚠️  RATE LIMIT HIT")
        print(f"   Message: {data['Note']}")
    else:
        print("❌ UNEXPECTED RESPONSE:")
        print(json.dumps(data, indent=2)[:500])


if __name__ == "__main__":
    print("StockSage AI — Alpha Vantage API Connectivity Test")
    print(f"Symbol: {TEST_SYMBOL}")
    print(f"API Key: {API_KEY[:6]}{'*' * (len(API_KEY)-6)}")

    test_daily_prices()
    test_rsi()

    print(f"\n{'='*50}")
    print("Done. If both tests passed, your Alpha Vantage tools are ready.")
    print("Note: Free tier allows 25 requests/day (500/day after email verify)")
