from bson import json_util
from flask import Flask, Blueprint, request, jsonify
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime
from pymongo.server_api import ServerApi
import json
import requests
import openai
from datetime import datetime, timedelta, time
import pandas as pd
import os
import certifi
from datetime import datetime
import schedule
import time as tm
import pytz


news_api_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
secret = "xxxxxxxxxxxxxxxxxxxxxxx"

'''
Function to calculate a given number of days in unix
'''
def getUnix(days):
    return days * 86400

import requests
import json
import pandas as pd

def assembleDF(ticker):
    accessKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    paginationLimit = 1000
    url = f"http://api.marketstack.com/v1/eod?access_key={accessKey}&symbols={ticker}&date_from=2020-01-13&date_to=2024-01-01&limit={paginationLimit}"
    r = requests.get(url)
    data = json.loads(r.text)
    data = data.get('data')
    dfData = {}
    for row in data:
        index = row.get('date').split('T')[0]
        dfData[index] = row.get('adj_close')
    df = pd.DataFrame.from_dict(dfData, orient="index", columns=['c'])
    df.index = pd.to_datetime(df.index)
    df = df.asfreq(freq='d')
    df['c'] = df['c'].ffill()
    df.index.freq = 'D'
    return df

'''
Function to combine multiple dataframes representing consecutive time series data
'''
def combineDF(frames):
    dfList = []
    for frame in frames:
        df = pd.read_csv(frame)
        dfList.append(df)
    result = pd.concat(dfList)
    return result

from pycaret.time_series import *
'''
Setup Pycaret framework and determine which model best suits the data
'''
def assembleModel(df):
    df = df.asfreq(freq='d')
    df.index.freq = 'D'
    df['c'] = df['c'].ffill()
    setup(df, fh=5, session_id=123, verbose = False)
    #best = compare_models()
    best = create_model('arima', verbose = False)
    result = best
    return result

'''
Generate predictions based on the best model
'''
def predictModel(days, model):
    model = finalize_model(model)
    prediction = predict_model(model, fh=days)
    return prediction

def get_percent_change(old_value, new_value):
    """
    Calculate the percent change between two values.

    Args:
        old_value (float): The initial value.
        new_value (float): The final value.

    Returns:
        float: The percent change, as a decimal.
    """
    if old_value == 0:
        return None  # Avoid division by zero
    percent_change = ((new_value - old_value) / abs(old_value)) * 100.0
    return percent_change

import json
import requests
#import pkg_resources
#pkg_resources.require("Openai==0.28")
import openai
from datetime import datetime, timedelta, time
import pandas as pd
import os

rest_client = REST(news_api_key, secret)
openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
openai.api_base = "https://expertsys1.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future
deployment_name='expertsys1' #This will correspond to the custom name you chose for your deployment when you deployed a model.

"""
Function to handle the GPT model.
Args:
    ticker: the ticker to analyze 
    d1: datetime argument --> IE: datetime(yyyy, mm, dd)
    d1: datetime argument --> IE: datetime(yyyy, mm, dd)
"""
def runGPT(priceData, ticker, prev_day, prev2_day):
    today = datetime.now()
    desired_time = datetime.now().time()
    pull_day = datetime.combine(today, desired_time)
    headlines=[]
    day0 = today
    price_open = [0,0,0,0,0]
    prev_price = priceData.iloc[-1].get('c')
    prev2_price = priceData.iloc[-1].get('c')
    articles = rest_client.get_news(ticker, prev2_day.strftime('%Y-%m-%d'), prev_day.strftime("%Y-%m-%d"))
    headlines = [x.headline for x in articles]
    summaries = [x.summary for x in articles]
    open_trend = get_percent_change(prev_price, prev2_price)
    user_message = f"""Forget all your previous instructions. Pretend you are a financial expert. You are
        a financial expert with stock recommendation experience. Provide a prediction for the direction of the stock,
        using only 1 word, 'bullish' for a positive trend, 'bearish' for a negative trend, or 'n/a' 
        if there is no headline provided or any other exception. Do not respond with anything other than
        one of these words. 
        Are these headlines good or bad for the stock price of {ticker} 
        in the next five days?
        Headline: ${headlines}"""
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[{"role": "system", "content": user_message}],
        max_tokens=500
    )
    assistant_response = response['choices'][0]['message']['content']
    if (assistant_response == None):
        return 'n/a'
    return assistant_response

def gptModel(data, ticker, d1, d2):
    rest_client = REST(news_api_key, secret)
    openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
    openai.api_base = "https://expertsys1.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15' # this may change in the future
    deployment_name='expertsys1' #This will correspond to the custom name you chose for your deployment when you deployed a model.
    result = runGPT(data, ticker, d1, d2)
    return result

from datetime import datetime, timedelta

def parseDate(date, timePeriod):
    y = int(date[0])
    m = int(date[1])
    d = int(date[2])
    # Check if timePeriod is within the specified range
    if not (0 < timePeriod < 31):
        raise ValueError("Invalid timePeriod. It must be > 0 and < 31.")
    month_days = {
        '1': 31,
        '2': 28,
        '3': 31,
        '4': 30,
        '5': 31,
        '6': 30,
        '7': 31,
        '8': 31,
        '9': 30,
        '10': 31,
        '11': 30,
        '12': 31
    }
    if d - timePeriod > 0:
        return datetime(y, m, d - timePeriod)
    elif d - timePeriod <= 0:
        remaining_days = timePeriod - d
        if m - 1 > 0:
            return datetime(y, m - 1, month_days[str(m - 1)] - remaining_days)
        else:
            # If the current month is January, go back to December of the previous year
            return datetime(y - 1, 12, month_days['12'] - remaining_days)

"""
Returns:
    1: Bullish
    -1: Bearish
    0: Uncertain
"""
def integratedModelLogic(gptDecision, arimaDecision):
    if gptDecision is None:
        return 0  # Return 0 for uncertain if GPT model output is None
    gptDecision = gptDecision.lower()
    gptDecision = gptDecision.replace(".", "")
    gptDecisions = {'bearish': -1, 'bullish': 1, 'uncertain': 0}
    gptDecision = gptDecisions.get(gptDecision)
    if gptDecision is None:
        return 0  # Return 0 for uncertain if GPT model output is None
    check = arimaDecision * gptDecision
    if check > 0:
        # Models agree
        if gptDecision == -1:
            return -1
        else:
            return 1
    elif check < 0:
        # Differing opinions and neither suggests HOLD
        return 0
    else:
        # gpt model produces uncertain output // or ARIMA predicts no change
        return 0


import json

def formatArimaData(historicalData, arimaOutput):
    arimaOutput.index = arimaOutput.index.to_timestamp()
    arimaOutput = arimaOutput.rename(columns = {'y_pred' : 'c'})
    df = historicalData.append(arimaOutput)
    result = {"c" : {}}
    for time, value in df.itertuples():
        result['c'][time.timestamp()] = value
    return json.dumps(result)

import GPTModel
import yfinance as yf
def generateJSON(currentDate, ticker, historicalData, arimaOutput, gptOutput, integratedOutput, timePeriod):
    ticker_symbol = yf.Ticker(ticker)
    historical_data = ticker_symbol.history(period="1d")
    closePrice = historical_data['Close'][0]
    closePrice = round(closePrice, 2)
    currentTime = currentDate.astimezone(pytz.utc).strftime("%I:%M")
    currDate = currentDate.strftime("%Y-%m-%d")
    #closePrice = historicalData.iloc[-1]['c']
    result = {"closing_price": closePrice,
              "date": currDate,
              "integrated_output": integratedOutput, "quantitative_output": None,
              "ticker": ticker, "time": currentTime
             }
    result['integrated_output'] = {"detailed_prediction": GPTModel.process_ticker_input(ticker), "general_prediction": gptOutput}
    result['quantitative_output'] = [{currDate: arimaOutput.iloc[timePeriod - 1]['y_pred']},
                                                 formatArimaData(historicalData, arimaOutput)]
    return result


from datetime import datetime
def integratedModelDriver(ticker, timePeriod=2):
    data = pd.DataFrame(assembleDF(ticker))
    arimaModel = assembleModel(data)
    prediction = predictModel(timePeriod, arimaModel)
    predictedPrice = prediction.iloc[timePeriod - 1]['y_pred']
    currentPrice = data.iloc[-1]['c']
    arimaDirection = predictedPrice - currentPrice
    #d1 = parseDate(currDate, 1)
    #d2 = parseDate(currDate, 2)
    d = datetime.now()
    d1 = d - timedelta(days=1)
    d2 = d1 - timedelta(days=1)
    gpt_model = gptModel(data, ticker, d1, d2)
    predictedDirection = integratedModelLogic(gpt_model, arimaDirection)
    result = generateJSON(d, ticker, data, prediction, gpt_model, predictedDirection, timePeriod)
    return result
#-------Connecting to MongoDB---------------

uri = "xxxxxxxx"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#function that returns database
def get_database():
   return client['user_stock_data']
#getting database
db = get_database()

#----------------------------Route--------------------------------------
app = Flask(__name__)
@app.route('/predictions', methods=['POST'])
def is_valid_ticker(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def get_tickers(user_stocks_collection):
    try:
        tickers_set = set()  # Use a set to store unique tickers
        documents = user_stocks_collection.find()
        for document in documents:
            ticker = document.get('ticker')
            if is_valid_ticker(ticker):
                tickers_set.add(ticker)

        tickers_list = list(tickers_set)  # Convert set to list
        print(tickers_list) #delete later
        return tickers_list

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_ticker_document(db, ticker, result_json):
    try:
        tickers_collection = db["tickers"]
        result_json["ticker"] = ticker  # Add the ticker information to the JSON document
        tickers_collection.insert_one(result_json)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def process_tickers_collection(db, user_stocks_collection):
    try:
        tickers_list = get_tickers(user_stocks_collection)
        for ticker in tickers_list:
            result_json = integratedModelDriver(ticker, timePeriod=2)  # Define timePeriod accordingly
            add_ticker_document(db, ticker, result_json)

        return {"success": "Ticker collection updated successfully"}
    except Exception as e:
        print("Error:", e)

def convert_est_time_to_utc(hour, minute):
    """
    est_hour = 9  # 9:00 AM EST
    est_minute = 0
    utc_hour, utc_minute = convert_est_time_to_utc(est_hour, est_minute)
    """
    # Define time zones
    est_tz = pytz.timezone('America/New_York')
    utc_tz = pytz.utc

    # Get current date and time in EST
    est_now = datetime.now(est_tz)

    # Create a datetime object for the specified time today in EST
    est_time_today = est_now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Convert the EST time to UTC
    utc_time = est_time_today.astimezone(utc_tz)

    # Extract hour and minute from the converted UTC time
    utc_hour = utc_time.hour
    utc_minute = utc_time.minute

    return utc_hour, utc_minute

def job():
    try:
        current_hour, current_minute = datetime.now().hour, datetime.now().minute
        current_hour_utc, current_minute_utc = convert_est_time_to_utc(current_hour, current_minute)
        utc_hour1, utc_minute1 = convert_est_time_to_utc(9, 0)
        utc_hour2, utc_minute2 = convert_est_time_to_utc(17, 0)
        # Check if the current hour is between 9 am and 5 pm in UTC
        if utc_hour1 <= current_hour_utc <= utc_hour2:
            print("Job started")
            user_stocks_collection = db['user_stocks']
            with app.app_context():
                result = process_tickers_collection(db, user_stocks_collection)
                print(result)  # Print the result for debugging purposes
        else:
            print("Job skipped: Current time is outside of 9 am - 5 pm range")
    except Exception as e:
        print(f"Error in job: {str(e)}")

    print("Job completed")


def schedule_and_run():
    # Schedule the job to run every hour at :08
    schedule.every().hour.at(":52").do(job)

    # Run the scheduler continuously
    while True:
        schedule.run_pending()
        tm.sleep(1)  # Use the renamed time module to avoid conflict

# Run the scheduling and execution function


if __name__ == '__main__':
    schedule_and_run()

    # This line is now outside the loop
    app.run(host='0.0.0.0', port=9780, debug=True)

