from pymongo import MongoClient
import certifi
from config import MONGO_URI

#-------Connecting to MongoDB---------------

#uri = "mongodb+srv://annavalente:1234@cluster0.q7jsu2y.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
#client = MongoClient(uri, tlsCAFile=certifi.where())
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#function that returns database
def get_database():
   return client['user_stock_data']

db = get_database()
