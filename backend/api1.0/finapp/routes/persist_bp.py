from flask import Blueprint, jsonify, request
import models.database as db
from flask_cors import CORS
from models.database import get_database


persist_bp = Blueprint('persist_bp', __name__)

@persist_bp.route('/persist', methods=['POST'])
def persist_data():
    try:
        data = request.json
        action = data.get("action")
        collection_name = str(data.get('collection')) #'collection' is the user's username
        db = get_database()  # Get the database instance
        collection = db[collection_name]
        

        if action == 'insert':
            collection.insert_one(data.get('document'))
            data.get('document')["_id"] = str(data.get('document')["_id"])
            return jsonify(data.get('document'))

        elif action == 'update':
            collection.update_one((data.get('query')), {"$set": data.get('update_values')})
            updated_document = collection.find_one(data.get('query'))
            updated_document["_id"] = str(updated_document["_id"])
            return jsonify(updated_document)

        elif action == 'delete':
            collection.delete_one(data.get('query'))
            return jsonify(f"Document of {data.get('query')} deleted.")

        elif action == 'upsert':
            collection.update_one((data.get('query')), {"$set": data.get('update_values')}, upsert=True)
            updated_document = collection.find_one(data.get('query'))
            updated_document["_id"] = str(updated_document["_id"])
            return jsonify(updated_document)

        elif action == 'find':
            document = collection.find_one(data.get("query"))
            document["_id"] = str(document["_id"])
            return jsonify(document)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

