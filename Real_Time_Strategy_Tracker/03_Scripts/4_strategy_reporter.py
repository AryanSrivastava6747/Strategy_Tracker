# 4_strategy_reporter.py
import pandas as pd
from datetime import datetime

# --- 1. Fetching Forecast Data (Hardcoded based on your outputs) ---

# Sentiment Forecast from 03_Scripts/2_sentiment_analyzer.py
sentiment_forecast_data = {
    '2025-11-23': 99.94,
    '2025-11-30': 99.20,
    '2025-12-07': 99.29,
    '2025-12-14': 99.28
}
sentiment_series = pd.Series(sentiment_forecast_data)
average_sentiment_forecast = sentiment_series.mean()

# Price Forecast from 03_Scripts/3_price_forecaster.py
price_forecast_data = {
    '2025-11-21': 52031,
    '2025-11-28': 52029,
    '2025-12-05': 52029,
    '2025-12-12': 52029
}
price_series = pd.Series(price_forecast_data)
average_price_forecast = price_series.mean()

# --- 2. Generating Strategy Insights ---

# Product Context (from raw_product_data.csv)
PRODUCT_NAME = "Apple iPhone 15 (128 GB) - Black"
COMPETITOR = "Apple/Amazon"
REPORT_DATE = datetime.now().strftime("%d %B %Y")

# Sentiment Strategy Logic
if average_sentiment_forecast >= 95:
    sentiment_insight = f"Sentiment is EXTREMELY HIGH (avg. {average_sentiment_forecast:.2f}% Positive). This indicates a highly satisfied customer base and a strong market position. The competitor is performing exceptionally well on product quality and experience."
    sentiment_recommendation = "Recommendation: Do NOT try to compete on product quality in the short term. Focus on differentiation, accessories, or value-added services."
elif average_sentiment_forecast >= 80:
    sentiment_insight = f"Sentiment is High (avg. {average_sentiment_forecast:.2f}% Positive). The product is performing well."
    sentiment_recommendation = "Recommendation: Look for the few negative/neutral reviews for specific product weaknesses (e.g., battery/heating) where your product can gain an advantage."
else:
    sentiment_insight = "Sentiment is Moderate/Low. There are clear opportunities for a better product experience."
    sentiment_recommendation = "Recommendation: Launch a product that directly addresses the competitor's pain points."

# Price Strategy Logic
if price_series.max() - price_series.min() < 500: # Less than ₹500 fluctuation is stable
    price_insight = f"Price is STABLE (avg. ₹{average_price_forecast:.0f}). The competitor is maintaining a premium, non-promotional price point."
    price_recommendation = "Recommendation: The competitor is not planning a major price drop. You have a window to use a competitive pricing strategy (e.g., flash sales, exchange bonuses) to attract customers."
else:
    price_insight = f"Price is VOLATILE (max fluctuation: ₹{price_series.max() - price_series.min():.0f}). A pricing event is likely."
    price_recommendation = "Recommendation: Wait for the price drop before making a counter-offer, or offer a value bundle that justifies your price."

# --- 3. Final Report Output ---

report = f"""
=========================================================
      COMPETITOR STRATEGY TRACKER: FINAL REPORT
=========================================================
Date Generated: {REPORT_DATE}
Competitor Product: {PRODUCT_NAME}
Target Competitor: {COMPETITOR}

---------------------------------------------------------
1. SENTIMENT ANALYSIS & FORECASTING
---------------------------------------------------------
- Current Review Count: 94 Analyzed (Approx.)
- Observed Positive Sentiment: 93/94 (Approx. 98.9%)
- 4-Week Average Forecast: {average_sentiment_forecast:.2f}% Positive

INSIGHT:
{sentiment_insight}

STRATEGY RECOMMENDATION:
{sentiment_recommendation}

---------------------------------------------------------
2. PRICING ANALYSIS & FORECASTING
---------------------------------------------------------
- Current Price (Base): ₹51,990
- 4-Week Average Forecast: ₹{average_price_forecast:.0f}
- Price Fluctuation Forecast: Min ₹{price_series.min():.0f} to Max ₹{price_series.max():.0f}

INSIGHT:
{price_insight}

STRATEGY RECOMMENDATION:
{price_recommendation}

---------------------------------------------------------
3. OVERALL COMPETITIVE STRATEGY (Sentiment + Price)
---------------------------------------------------------
The competitor is executing a **Premium Quality, Stable Price** strategy.
They rely on a highly positive product experience to justify a consistent price point.
Your strategy should focus on **undercutting their stable price** with promotional offers OR **launching a product with superior features** that address niche complaints (like battery life or refresh rate, which were mentioned in the original reviews).

=========================================================
"""

print(report)
