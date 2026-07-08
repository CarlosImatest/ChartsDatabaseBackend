from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import certifi

#looks for .env file in current dir
load_dotenv()

# variable names from Atlas-generated .env
uri     = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB_NAME", "sample_mflix")

if not uri:
    raise ValueError("MONGODB_URI not found in .env")

print(f"Loaded URI: {uri[:40]}...")
print(f"Database  : {db_name}")

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    database = client.get_database(db_name)
    movies   = database.get_collection("movies")

    query = {"title": "Back to the Future"}
    movie = movies.find_one(query)

    print(json.dumps(movie, indent=4, default=str))
    client.close()

except Exception as e:
    raise Exception(f"Unable to find document: {e}")