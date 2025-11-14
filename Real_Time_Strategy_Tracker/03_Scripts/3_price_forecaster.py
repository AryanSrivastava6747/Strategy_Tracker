import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# 1. Configuration (Current Price and ASIN from raw_product_data.csv)
# We will hardcode the necessary data from raw_product_data.csv for simplicity
CURRENT_PRICE = 51990
ASIN = "B0CHX1W1XY"
# We assume the price was scraped today (Nov 14, 2025)
TODAY = datetime(2025, 11, 14) 

# --- Function to generate synthetic weekly price data ---
def generate_synthetic_price_history(start_date, current_price, num_weeks=10):
    """
    Generates a synthetic price time series assuming a slight random fluctuation
    around a base price that generally matches the current price.
    """
    dates = [start_date - timedelta(weeks=i) for i in range(num_weeks)][::-1]
    
    # Base price trend: Assume a slight decreasing trend (typical for electronics)
    # The initial price is slightly higher than the current price
    base_price = current_price * 1.05
    
    prices = []
    
    for i in range(num_weeks):
        # Apply a slight random fluctuation (e.g., +/- 1% of the base price)
        fluctuation = random.uniform(-0.01, 0.01) * base_price
        
        # Apply a mild downward trend over time
        trend = - (i * 0.005) * base_price
        
        price = base_price + fluctuation + trend
        
        # Round price to the nearest 10 (common for e-commerce pricing)
        prices.append(round(price / 10) * 10)
        
    df = pd.DataFrame({'date': dates, 'price': prices})
    df['date'] = df['date'].dt.normalize()
    return df

# Generate 10 weeks of synthetic data
synthetic_df = generate_synthetic_price_history(TODAY, CURRENT_PRICE, num_weeks=10)

# Ensure the last price is close to the current price
synthetic_df.iloc[-1, synthetic_df.columns.get_loc('price')] = CURRENT_PRICE

# Save the synthetic data to be used for forecasting
file_name = f"synthetic_price_history_{ASIN}.csv"
synthetic_df.to_csv(file_name, index=False)

print(f"✅ Synthetic Price Data (10 weeks) generated and saved to {file_name}")
print("\n--- Last 5 Weeks of Synthetic Price Data ---")
print(synthetic_df.tail().to_string(index=False))

# --- Next Step: Run Price Forecasting ---
# Now, we will directly proceed to the forecasting step using this generated data.

from statsmodels.tsa.arima.model import ARIMA

# Prepare Time Series Data
ts_data = synthetic_df.set_index('date')['price']

# 2. Fit ARIMA Model and Forecast
if len(ts_data) >= 7:
    # Use ARIMA order (1, 1, 0) as it's common for price data with trends
    order = (1, 1, 0) 
    model = ARIMA(ts_data, order=order)
    model_fit = model.fit()

    forecast_steps = 4
    forecast_result = model_fit.get_forecast(steps=forecast_steps)
    forecast = forecast_result.predicted_mean
    
    # Create an index for the next 4 weeks
    last_date = ts_data.index[-1]
    forecast_index = pd.date_range(start=last_date, periods=forecast_steps + 1, freq='W-FRI')[1:]
    forecast_series = pd.Series(forecast.values, index=forecast_index)
    
    print(f"\n✅ Price Forecasting for the next {forecast_steps} weeks complete.")
    
    # Final Output
    print("\n--- Next 4 Weeks Price Forecast (INR) ---")
    print(forecast_series.round(0).astype(int).to_string(header=False))

else:
    print("❌ Error: Not enough data points for robust ARIMA price forecasting.")