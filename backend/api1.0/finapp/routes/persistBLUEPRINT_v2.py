from flask import Blueprint, jsonify, request
import models.database as db

persist_bp = Blueprint('persist_bp', __name__)

@persist_bp.route('/persist', methods=['POST'])
def persist_data():
    try:
        data = request.json
        action = data.get("action")
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
            document["_id"] = str(document["_id"])
            return jsonify(document)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

