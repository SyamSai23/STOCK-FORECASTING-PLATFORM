import json
import requests
import openai 
from datetime import datetime, timedelta, time
import pandas as pd
import os
#from alpaca_trade_api.rest import REST#, Stream
#from newsapi import 
from alpaca.common.rest import RESTClient
from config import NEWS_API_ENDPOINT, NEWS_API_KEY, NEWS_API_SECRET

class GPTModelSimplified:

    def __init__(self):
        """
        Relevant GPT Model keys below
        """
        openai.api_key = "1606201e15864372b4207a3f9c85f406"
        openai.api_base = "https://expertsys1.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15' # this may change in the future
        self.deployment_name='expertsys1' #This will correspond to the custom name you chose for your deployment when you deployed a model.
        self.headlines = []
        self.news_api_key = NEWS_API_KEY
        self.secret = NEWS_API_SECRET
        self.endpoint = NEWS_API_ENDPOINT
        #self.rest_client = REST(self.news_api_key, self.secret, self.endpoint)
        self.rest_client = RESTClient(base_url=self.endpoint, api_version='v1beta1',
                                api_key=self.news_api_key, secret_key=self.secret)

    """
    Calculate the percent change between two values.
    Args:
        old_value (float): The initial value.
        new_value (float): The final value.
    Returns:
        float: The percent change, as a decimal.
    """
    def __get_percent_change(self, old_value, new_value):
        if old_value == 0:
            return None  # Avoid division by zero
        percent_change = ((new_value - old_value) / abs(old_value)) * 100.0
        return percent_change

    def populateHeadlines(self, ticker, prevDay, prev2Day):
        news_endpoint = '/news'
        parameters = {
        'start': prev2Day.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),  # Format datetime to RFC3339
        'end': prevDay.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),  # Format datetime to RFC3339
        'symbols': ticker
        }
        news = self.rest_client.get(news_endpoint, parameters)
        self.headlines = [x.get('headline') for x in news.get('news')]

    """
    Function to handle the GPT model.
    Args:
        ticker: the ticker to analyze 
        d1: datetime argument --> IE: datetime(yyyy, mm, dd)
        d1: datetime argument --> IE: datetime(yyyy, mm, dd)
    """
    def runGPT(self, priceData, ticker, prev_day, prev2_day):
        # populate the headlinees for news api
        self.populateHeadlines(ticker, prev_day, prev2_day)
        user_message = f"""Forget all your previous instructions. Pretend you are a financial expert. You are
            a financial expert with stock recommendation experience. Provide a prediction for the direction of the stock,
            using only 1 word, 'bullish' for a positive trend, 'bearish' for a negative trend, or 'n/a' 
            if there is no headline provided or any other exception. Do not respond with anything other than
            one of these words. 
            Are these headlines good or bad for the stock price of {ticker} 
            in the next five days?
            Headline: ${self.headlines}"""
        response = openai.ChatCompletion.create(
            engine=self.deployment_name,
            messages=[{"role": "system", "content": user_message}],
            max_tokens=500
        )
        assistant_response = response['choices'][0]['message']['content']
        if (assistant_response == None):
            return 'n/a'
        return assistant_response

    """
    Function to handle the GPT model's detailed response.
    Args:
        ticker: the ticker to analyze 
        d1: datetime argument --> IE: datetime(yyyy, mm, dd)
        d1: datetime argument --> IE: datetime(yyyy, mm, dd)
    """
    def runGPT_Detailed(self, priceData, ticker, prev_day, prev2_day, arimaPrediction):
        ### Incorporate percent change of stock price into the model
        user_message = f"""Forget all your previous instructions. Pretend you are a financial expert with stock recommendation experience. 
            Provide a prediction for the direction of the stock,
            using 'bullish' for a positive trend and 'bearish' for a negative trend, or 'not enough information' 
            if there is no headline provided or any other exception. Then, explain the reasoning for your prediction,
            and cite the most influential articles headlines and source. Break your prediction up into 3 sections,
            'Prediction:', 'Explanation:', 'Sources:'. For sources, please format them in this manner:  'Tech Titans Tumble: 'Magnificent Seven' Shed $250 Billion in Market Cap On 2024 Day One'  (Benzinga)\n- 'Opportunities Ahead – Avoid Classic New Year Mistake, China And Iran Threats, Bitcoin Rumor' (Sentieo)\n- 'This Analyst With 82% Accuracy Rate Sees Around 19% Upside In Meta Platforms - Here Are 5 Stock Picks For Last Week From Wall Street's Most Accurate Analysts' (Forbes)
            Are these headlines good or bad for the stock price of {ticker} 
            in the next two days?
            Headline: ${self.headlines}"""
        response = openai.ChatCompletion.create(
            engine=self.deployment_name,
            messages=[{"role": "system", "content": user_message}],
            max_tokens=500
        )
        assistant_response = response['choices'][0]['message']['content']
        if (assistant_response == None):
            return 'n/a'
        return assistant_response