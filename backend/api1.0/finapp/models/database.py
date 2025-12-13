from pymongo import MongoClient
import certifi
import logging
from config import MONGO_URI

logging.basicConfig(level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

def get_database():
    return client['user_stock_data']

def insert_document(collection, document):
    try:
        collection.insert_one(document)
        return {"status": "success", "message": "Document inserted"}
    except Exception as e:
        logging.error(f"Insert Error: {e}")
        return {"status": "error", "message": str(e)}

def update_document(collection, query, update_values):
    try:
        collection.update_one(query, {'$set': update_values})
        return {"status": "success", "message": "Document updated"}
    except Exception as e:
        logging.error(f"Update Error: {e}")
        return {"status": "error", "message": str(e)}

def delete_document(collection, query):
    try:
        collection.delete_one(query)
        return {"status": "success", "message": "Document deleted"}
    except Exception as e:
        logging.error(f"Delete Error: {e}")
        return {"status": "error", "message": str(e)}

def upsert_document(collection, query, update_values):
    try:
        collection.update_one(query, {'$set': update_values}, upsert=True)
        return {"status": "success", "message": "Document upserted"}
    except Exception as e:
        logging.error(f"Upsert Error: {e}")
        return {"status": "error", "message": str(e)}

def find_document(collection, query):
    try:
        document = collection.find(query)
        return {"status": "success", "message": "Document found", "document": document}
    except Exception as e:
        logging.error(f"Find Error: {e}")
        return {"status": "error", "message": str(e)}
