from flask import Flask, request, jsonify, Blueprint
import yfinance as yf
from datetime import datetime, timedelta, time
import models.database as db
import certifi
import json
from bson import json_util
from models.database import get_database


bp_route = Blueprint('bp_route', __name__)

@bp_route.route('/search', methods=['POST'])
def search_engine():
    return handle_json()

def handle_json():
    try:
        data = request.json
        ticker = data.get('ticker')

        if not ticker:
            return jsonify({"error": "Ticker not provided"}), 400

        # Use yfinance to get information for the provided ticker using method
        stock_info = get_stock_info(ticker)

        return jsonify(stock_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        about_info = stock.info.get("longBusinessSummary")

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
            "about": {
                "About": about_info
            },
            "graph_info": {
                "historical_prices": historical_prices,
                "hourly_prices": hourly_prices
            }
        }

        return info

    except Exception as e:
        raise Exception(f"Error fetching stock information: {str(e)}")


@bp_route.route('/persist', methods=['POST'])
def persist_data():
    try:
        data = request.json
        action = data.get("action")
        db = get_database() 
        collection = db["user_stocks"] #The collection that stores all user's stocks


        if action == 'insert':
            collection.insert_one(data.get('document'))
            data.get('document')["_id"] = str(data.get('document')["_id"])
            return jsonify(data.get('document'))

        elif action == 'update':
            query1 = data.get("query1") #username
            query2 = data.get("query2")
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
                collection.update_one(query, {"$set": data.get('update_values')})
                updated_document = collection.find_one(query)
            updated_document["_id"] = str(updated_document["_id"])
            return jsonify(updated_document)

        elif action == 'delete':
            query1 = data.get("query1") #username
            query2 = data.get("query2")
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
                collection.delete_one(query)
            return jsonify(f"Document deleted.")

        elif action == 'upsert':
            query1 = data.get("query1") #username
            query2 = data.get("query2")
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
                collection.update_one(query, {"$set": data.get('update_values')}, upsert=True)
                updated_document = collection.find_one(query)
            updated_document["_id"] = str(updated_document["_id"])
            return jsonify(updated_document)

        elif action == 'find':
            query1 = data.get("query1") #username
            query2 = data.get("query2")
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
            document = collection.find_one(query)
            print(document)
            document["_id"] = str(document["_id"])
            return jsonify(document)

        elif action == 'findall':
            query1 = data.get("query1")  # username
            query2 = data.get("query2")
            query = {}
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
            elif query1 is not None:
                query = query1
            elif query2 is not None:
                query = query2

            try:
                documents = collection.find(query)
                results = []
                for doc in documents:
                    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
                    results.append(doc)
                return jsonify(results)
            except Exception as e:
                # Handle exceptions (e.g., connection error, query error)
                return jsonify({"error": str(e)})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_route.route('/portfolio', methods=['POST'])
def portfolio(): #returns all the documents in a user's collection
    try:
        data = request.json
        action = data.get("action")
        username = data.get("username")
        db = get_database() 
        collection = db['user_stocks']

        if action == 'get_documents':
            return get_user_documents(collection, username)
        elif action == "get_tickers":
            return get_user_tickers(collection, username)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_documents(collection, username):
    try:
        documents = collection.find({"username": username})
        user_documents = list(documents)
        for document in user_documents:
            document['_id'] = str(document['_id'])
            # Use json_util.dumps to serialize the documents to JSON
            response_data = json.loads(json_util.dumps(user_documents))
            return jsonify(response_data)
    except:
        return jsonify({"error": str(e)}), 500

def get_user_tickers(collection, username):
    try:
        documents = collection.find({"username": username})
        user_documents = list(documents)
        tickers_list = []
        for document in user_documents:
            ticker = document.get('ticker')
            if ticker:
                tickers_list.append(ticker)
        return jsonify(tickers_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_route.route('/tickers_add', methods=['POST'])
def tickers_add():
    try:
        data = request.json
        action = data.get("action")
        db = get_database() 
        collection = db["tickers"] #The collection that stores all user's stocks


        if action == 'insert':
            collection.insert_one(data.get('document'))
            data.get('document')["_id"] = str(data.get('document')["_id"])
            return jsonify(data.get('document'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
@bp_route.route('/history_persist', methods=['POST'])
def history_persist():
    try:
        data = request.json
        action = data.get("action")
        db = get_database() 
        collection = db['tickers'] #we'll change this once we get official data

        if action == "find_by_three_queries":
            query1 = data.get("query1")  # ticker
            query2 = data.get("query2") # date (ex: 2023-12-14")
            query3 = data.get("query3") #time (military, ex: 9:00)
            if query1 is not None and query2 is not None and query3 is not None:
                query = {"$and": [query1, query2, query3]}
            document = collection.find_one(query)
            document["_id"] = str(document["_id"])
            return jsonify(document)

        if action == "find_by_two_queries":
            query1 = data.get("query1") #ticker
            query2 = data.get("query2") #date or time
            if query1 is not None and query2 is not None:
                query = {"$and": [query1, query2]}
                document = collection.find_one(query)
                document["_id"] = str(document["_id"])
                return jsonify(document)

        if action == "find_by_one_query":
            query = data.get("query") #ticker
            document = collection.find_one(query)
            document["_id"] = str(document["_id"])
            return jsonify(document)
        
        if action == "findall_by_three_queries":
            query1 = data.get("query1")  # ticker (e.g., {"ticker": "AAPL"})
            query2 = data.get("query2")  # date (e.g., {"date": "2023-12-14"})
            query3 = data.get("query3")  # time (e.g., {"time": "9:00"})

            query = {}
            if query1 is not None and query2 is not None and query3 is not None:
                query = {"$and": [query1, query2, query3]}

            documents = collection.find(query)

            # Convert the results to a list of dictionaries
            results = []
            for document in documents:
                document["_id"] = str(document["_id"])  # Convert ObjectId to string
                results.append(document)
            return jsonify(results)

        if action == "findall":
            query1 = data.get("query1")  # ticker (e.g., {"ticker": "AAPL"})
            query2 = data.get("query2")  # date (e.g., {"date": "2023-12-14"})
            query3 = data.get("query3")  # time (e.g., {"time": "9:00"})

            query = {}
            if query1 is not None and query2 is not None and query3 is not None:
                query = {"$and": [query1, query2, query3]}

            documents = collection.find(query)

            # Convert the results to a list of dictionaries
            results = []
            for document in documents:
                document["_id"] = str(document["_id"])  # Convert ObjectId to string
                results.append(document)

            total_predictions = len(results)
            correct_predictions = 0
            total_up = 0
            correct_up = 0
            total_down = 0
            total_hold = 0
            correct_down = 0
            correct_hold = 0

            for doc in results:
                # Assuming 'actual_result' field indicates the actual outcome
                # Replace 'actual_result' and 'prediction' with actual field names
                doc['actual_result'] = doc['integrated_output']['general_prediction']
                if doc['integrated_output']['general_prediction'] == doc['actual_result']:
                    correct_predictions += 1
                    if doc['actual_result'] == 'bullish':
                        correct_up += 1
                    elif doc['actual_result'] == 'bearish':
                        correct_down += 1
                    elif doc['actual_result'] == 'hold':
                        correct_hold += 1   

                if doc['integrated_output']['general_prediction'] == 'bullish':
                    total_up += 1
                elif doc['integrated_output']['general_prediction'] == 'bearish':
                    total_down += 1
                elif doc['integrated_output']['general_prediction'] == 'hold':
                    total_hold += 1

            correct_predictions_percentage = (correct_predictions / total_predictions) * 100 if total_predictions else 0
            stats = {
                "Correct Predictions (%)": f"{correct_predictions_percentage:.2f}%",
                "Correct Bullish/Total Bullish": f"{correct_up}/{total_up}",
                "Correct Bearish/Total Bearish": f"{correct_down}/{total_down}",
                "Correct Hold/Total Hold": f"{correct_hold}/{total_hold}"
            }

            return jsonify({"results": results, "statistics": stats})



        if action == "find_dashboard_data":
            query1 = data.get("query1")
            query2 = data.get("query2")
            query3 = data.get("query3")

            # Combine the queries
            query = {"$and": [query1, query2]} if query3 == {} else {"$and": [query1, query2, query3]}

            # Aggregation pipeline
            aggregation_pipeline = [
                {"$match": query},
                {"$sort": {"date": -1, "time": -1}},
                {"$group": {
                    "_id": "$ticker",
                    "latestDocument": {"$first": "$$ROOT"}
                }},
                {"$replaceRoot": {"newRoot": "$latestDocument"}},
                {"$project": {
                    "_id": {"$toString": "$_id"},  # Convert ObjectId to string
                    "date": 1,
                    "ticker": 1,
                    "integrated_output": 1,
                    "quantitative_output": 1
                }}
            ]

            documents = collection.aggregate(aggregation_pipeline)

            # Convert the results to a list of dictionaries
            results = list(documents)

            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@bp_route.route('/closingPrice', methods=['POST'])
def closing_price_info():
    return index()

def get_closing_price(date, ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    # Calculate previous day
    next_day = date_obj + timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    historical_data = ticker.history(start=next_day_str, period='1d')
    if not historical_data.empty:
        closing_price = historical_data['Close'][0]
        return closing_price
    else:
        return None

def index():
    data = request.json
    ticker = data.get('ticker')
    date = data.get('date') #date should be in format "YYYY-MM-DD"
    if not ticker:
        return jsonify({"error": "Ticker not provided"}), 400
    if not date:
        return jsonify({"error": "Date not provided"}), 400
    closing_price = get_closing_price(date, ticker)
    if closing_price is not None:
        info = {
            "Ticker": ticker,
            "Date": date,
            "Closing Price": closing_price
        }
        return info
    else:
        return jsonify({"error": "Cannot find closing price"}), 400