

from bson import json_util
from flask import Flask, Blueprint, request, jsonify, current_app  # Import current_app
import yfinance as yf
from datetime import datetime
import json
import requests
import openai
from datetime import datetime, timedelta, time
import pandas as pd
import os
import logging
import certifi
from datetime import datetime
import schedule
import time as tm
import pytz
from models import database as db
from models.IntegratedModel.IntegratedModel import IntegratedModel
import config
logging.basicConfig(level=logging.INFO)

news_api_key = config.NEWS_API_KEY
endpoint = config.NEWS_API_ENDPOINT

#----------------------------Route--------------------------------------
predictions_bp = Blueprint('predictionsBLUEPRINT', __name__)
@predictions_bp.route('/predictionsBLUEPRINT', methods=['POST'])
def is_valid_ticker(ticker):
    if not ticker:
        return jsonify({"error": "Ticker not provided"}), 400
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify({"valid_ticker": True})
    else:
        return jsonify({"valid_ticker": False})

def get_tickers(user_stocks_collection):
    """
    Problem accessing the tickers list
    PROBLEM ACCESSING THE DATABASE AS A WHOLE
    """
    try:
        tickers_set = set()  # Use a set to store unique tickers
        documents = user_stocks_collection.find()
        for document in documents:
            ticker = document.get('ticker')
            if is_valid_ticker(ticker):
                tickers_set.add(ticker)
        tickers_list = list(tickers_set)  # Convert set to list
        return tickers_list
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_ticker_document(db, ticker, result_json):
    try:
        tickers_collection = db.db["tickers_stephen"]
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
            intModel = IntegratedModel()
            output = intModel.runModel(ticker, 2)  # Define timePeriod accordingly
            result_json = intModel.generateJSON()
            print(result_json)
            add_ticker_document(db, ticker, result_json)
        return {"success": "Ticker collection updated successfully"}
    except Exception as e:
        return ({"failure": "Problem encountered when updating ticker collection"})

def convert_est_time_to_utc(hour, minute):
    """
    est_hour = 9  # 9:00 AM EST
    est_minute = 0
    utc_hour, utc_minute = convert_est_time_to_utc(est_hour, est_minute)
    """
    # Define time zones
    est_tz = pytz.timezone('America/New_York')
    utc_tz = pytz.utc
    est_now = datetime.now(est_tz)     # Get current date and time in EST
    est_time_today = est_now.replace(hour=hour, minute=minute, second=0, microsecond=0)     # Create a datetime object for the specified time today in EST
    utc_time = est_time_today.astimezone(utc_tz)     # Convert the EST time to UTC
    # Extract hour and minute from the converted UTC time
    utc_hour = utc_time.hour
    utc_minute = utc_time.minute
    return utc_hour, utc_minute

def job():
    try:
        print("entered")
        current_hour, current_minute = datetime.now().hour, datetime.now().minute
        current_hour_utc, current_minute_utc = convert_est_time_to_utc(current_hour, current_minute)
        print("Job started")
        user_stocks_collection = db.db['user_stocks']
        app = Flask(__name__)  # Create a new Flask app instance
        app.app_context().push()  # Push an application context
        with app.app_context():  # Use the app context
            result = process_tickers_collection(db.db, user_stocks_collection)
            print(result)  # Print the result for debugging purposes
    except Exception as e:
        print(f"Error in job: {str(e)}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(sys.stderr)
    print("Job completed")

def schedule_and_run():
    ### Need to start clearig the tickers database at some point.
    ### Check tickers database for duplicates
    # Schedule the job to run every hour at :08
    schedule.every().hour.at(":03").do(job)
    # Run the scheduler continuously
    while True:
        schedule.run_pending()
        tm.sleep(1)  # Use the renamed time module to avoid conflict
# Run the scheduling and execution function
schedule_and_run()