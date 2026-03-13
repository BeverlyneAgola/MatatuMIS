from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi

connection_string = "mongodb+srv://agola:myfirstdatabase@trial.qwqpkuo.mongodb.net/?retryWrites=true&w=majority&appName=Trial"


def get_db():
    try:
        client = MongoClient(
            connection_string,
            tlsCAFile=certifi.where()
        )

        client.admin.command("ping")
        print("MongoDB connection successful!")
        return client["sacco_management"]

    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None