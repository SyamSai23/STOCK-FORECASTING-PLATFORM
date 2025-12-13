from bson import json_util
from flask import Flask, Blueprint, request, jsonify
import yfinance as yf
from datetime import datetime
from pymongo.server_api import ServerApi
import json
import requests
import openai
from datetime import datetime, timedelta, time
import pandas as pd
import os
import logging
from config import MONGO_URI, NEWS_API_KEY, SECRET, ENDPOINT,OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_API_TYPE, OPENAI_API_VERSION, OPENAI_DEPLOYMENT_NAME
from alpaca_trade_api import REST, Stream
import certifi
from datetime import datetime
import schedule
import time as tm


nlogging.basicConfig(level=logging.INFO)

news_api_key = NEWS_API_KEY
secret = SECRET
endpoint = ENDPOINT

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE
openai.api_type = OPENAI_API_TYPE
openai.api_version = OPENAI_API_VERSION
deployment_name = OPENAI_DEPLOYMENT_NAME
rest_client = REST(news_api_key, secret)

#function that takes in old and new value and returns percentage change
def get_percent_change(old_value, new_value):
    if old_value == 0:
        return None  # Avoid division by zero
    percent_change = ((new_value - old_value) / abs(old_value)) * 100.0
    return percent_change

#function that takes in ticker and returns the current stock price
def get_current_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    return stock_data.history(period='1d')['Close'].iloc[-1]


def process_ticker_input(ticker):
    try:
        today = datetime.now()
        desired_time = datetime.now().time()
        prev_day = today - timedelta(days=1)
        prev2_day = today - timedelta(days=2)

        prev_price = yf.download(ticker, prev_day)
        prev2_price = yf.download(ticker, prev2_day)

        price_close = [prev_price['Close'].iloc[0], prev2_price['Close'].iloc[0]]
        price_open = [prev_price['Open'].iloc[0], prev2_price['Open'].iloc[0]]

        articles = rest_client.get_news(ticker, prev2_day.strftime('%Y-%m-%d'), prev_day.strftime("%Y-%m-%d"))
        headlines = [x.headline for x in articles]

        open_trend = get_percent_change(price_open[0], price_open[1])

        user_message = f"""Forget all your previous instructions. Pretend you are a financial expert with stock recommendation experience. 
    Provide a prediction for the direction of the stock,
    using 'bullish' for a positive trend and 'bearish' for a negative trend, or 'not enough information' 
    if there is no headline provided or any other exception. Then, explain the reasoning for your prediction,
    and cite the most influential articles headlines and source. Break your prediction up into 3 sections,
    'Prediction:', 'Explanation:', 'Sources:'. For sources, please format them in this manner:  'Tech Titans Tumble: 'Magnificent Seven' Shed $250 Billion in Market Cap On 2024 Day One'  (Benzinga)\n- 'Opportunities Ahead – Avoid Classic New Year Mistake, China And Iran Threats, Bitcoin Rumor' (Sentieo)\n- 'This Analyst With 82% Accuracy Rate Sees Around 19% Upside In Meta Platforms - Here Are 5 Stock Picks For Last Week From Wall Street's Most Accurate Analysts' (Forbes)
    Are these headlines good or bad for the stock price of {ticker} 
    in the next two days?
    Headline: ${headlines}"""

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "system", "content": user_message}],
            max_tokens=500
        )
        assistant_response = response['choices'][0]['message']['content']
        return assistant_response

    except Exception as e:
        print(f"Error processing input for {ticker}: {str(e)}")
