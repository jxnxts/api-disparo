import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

# MONGO_URI = "mongodb+srv://jonatas:88343806@whats.r7qrlcw.mongodb.net/?retryWrites=true&w=majority"

MONGO_URI = "mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}"

class NoSQLDatabase():
    def __init__(self) -> None:
        self.connection_is_active = False
        self.client = None

    def get_mongo_connection(self):
        if self.connection_is_active == False:
            try:
                self.client = MongoClient(MONGO_URI)
                self.connection_is_active = True
                return self.client
            except Exception as ex:
                print("Error connecting to MongoDB : ", ex)
        return self.client

    def get_mongo_db(self, client):
        try:
            db = client[MONGO_DB_NAME]
            return db
        except Exception as ex:
            print("Error getting MongoDB Database : ", ex)
            return None


if __name__ == "__main__":
    nosql_db = NoSQLDatabase()
    mongo_client = nosql_db.get_mongo_connection()
    mongo_db = nosql_db.get_mongo_db(mongo_client)
    print("MongoDB connected and database selected.")