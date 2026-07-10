from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import certifi

class DbConnect:
    #looks for .env file in current dir
    load_dotenv("/Users/imatest_carlos/Desktop/Imatest/ChartDatabaseProject/backend/pymongo-quickstart/.env")
    def __init__(self, db_name, collection_name):
        # variable names from Atlas-generated .env
        self.uri     = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB_NAME", db_name)
        self.collection_name = collection_name

    def start_connection(self):

        if not self.uri:
            raise ValueError("MONGODB_URI not found in .env")

        print(f"Loaded URI: {self.uri[:10]}...")
        print(f"Database  : {self.db_name}")

        client = MongoClient(self.uri, tlsCAFile=certifi.where())

        try:
            database = client.get_database(self.db_name)
            collection   = database.get_collection(self.collection_name)

        except Exception as e:
            raise Exception(f"Unable to find document: {e}")
        
        return collection, database, client