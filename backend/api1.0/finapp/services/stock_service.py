import yfinance as yf
import openai
from datetime import datetime, timedelta
from config import OPENAI_API_KEY, OPENAI_DEPLOYMENT_NAME
# Include other necessary imports, like for your REST client



def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)

        # Fetch historical prices
        historical_prices = stock.history(period='1y')['Close'].reset_index()
        historical_prices = historical_prices.rename(columns={'Date': 'date', 'Close': 'price'})
        historical_prices = historical_prices.to_dict(orient='records')

        # Fetch hourly prices for the current day
        hourly_prices = stock.history(period='1d', interval='1h')['Close'].reset_index()
        hourly_prices = hourly_prices.rename(columns={'Datetime': 'datetime', 'Close': 'price'})
        hourly_prices['hour'] = hourly_prices['datetime'].dt.strftime('%H:%M')
        hourly_prices = hourly_prices[['hour', 'price']].groupby('hour').last().reset_index()
        hourly_prices = hourly_prices.to_dict(orient='records')

        info = {
            "ticker": ticker,
            "info": {
                "previous_close": stock.info.get("previousClose"),
                "day_range": {"low": stock.info.get("dayLow"), "high": stock.info.get("dayHigh")},
                "year_range": {"low": stock.info.get("52WeekLow"), "high": stock.info.get("52WeekHigh")},
                "market_cap": stock.info.get("marketCap"),
                "pe_ratio": stock.info.get("trailingPE"),
                "dividend_yield": stock.info.get("dividendYield"),
                "primary_exchange": stock.info.get("exchange"),
                "average_volume": stock.info.get("averageVolume"),
            },
            "graph_info": {
                "historical_prices": historical_prices,
                "hourly_prices": hourly_prices
            }
        }

        return info

    except Exception as e:
        raise Exception(f"Error fetching stock information: {str(e)}")

# You can add more stock-related functions here
