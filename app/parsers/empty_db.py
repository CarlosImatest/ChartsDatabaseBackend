import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2])) # go up 3 levels: parsers -> app -> backend
from app.db.mDB_connect_to_db import DbConnect

user_input = input("enter collection name")

connect = DbConnect("Charts", user_input)


collection, database, client = connect.start_connection()

# delete_many directly on the collection object and returns deleted count
result = collection.delete_many({})

print(f"Successfully emptied the collection. Deleted {result.deleted_count} documents.")

client.close()