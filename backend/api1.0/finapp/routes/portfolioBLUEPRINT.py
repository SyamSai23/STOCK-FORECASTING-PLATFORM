from flask import Blueprint, jsonify, request
import models.database as db

portfolio_bp = Blueprint('portfolio_bp', __name__)

@portfolio_bp.route('/portfolio', methods=['POST'])
def portfolio(): #returns all the documents in a user's collection
    try:
        data = request.json
        action = data.get("action")
        username = data.get("username")
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