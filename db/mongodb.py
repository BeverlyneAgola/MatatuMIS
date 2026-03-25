from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi
from config import MONGO_URI



def get_db():
    try:
        client = MongoClient(
            MONGO_URI,
            tlsCAFile=certifi.where()
        )

        client.admin.command("ping")
        print("MongoDB connection successful!")
        return client["sacco_management"]

    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None