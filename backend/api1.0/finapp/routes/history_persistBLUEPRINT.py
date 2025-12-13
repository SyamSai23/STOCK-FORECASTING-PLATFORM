from flask import Blueprint, jsonify, request
import models.database as db

history_persist_bp = Blueprint('history_persist_bp', __name__)

@portfolio_bp.route('/history_persist', methods=['POST'])
def persist():
    try:
        data = request.json
        action = data.get("action")
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500