import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2])) # go up 3 levels: parsers -> app -> backend
from app.db.mDB_connect_to_db import DbConnect
import pandas as pd

# connect = DbConnect("Charts", "WDR") #establishing connection
# db, client = connect.start_connection() #instantiating db and client

#getting google sheet
file_name = ["originalSheet/CRC (All).xlsx", "originalSheet/LDR (All).xlsx", "originalSheet/UHDR (All).xlsx", "originalSheet/VISNIR.xlsx", "originalSheet/WDR (All).xlsx"]
google_sheet_df = [list(pd.read_excel(name).columns) for name in file_name]


#db collection names
collection_name = ["CRC", "LDR", "UHDR", "VISNIR", "WDR"]
database_name = "Charts"

no_match = {}
test_name = ["200-201-1", "202-201-2", "260-261-1"]

connect = DbConnect("Charts", "WDR") #establishing connection
db, client = connect.start_connection() #instantiating db and client

names = [chart["name"] for chart in db.find({}, {"name": 1})]

print(names)

# for i in test_name:
#     if i in list(google_sheet_df[-1].columns):
#         print(f"yes {i} is in WDR")
#     else:
#         print("no")

counter = 0
# for chart in db.find({}, {"name": 1, "_id": 0}):
#     counter += 1
#     print(chart["name"])
#     print(isinstance(chart["name"],str))

#     if counter == 5:
#         client.close()
#         break

# for collection in collection_name:
#     index += 1
#     connect = DbConnect("Charts", collection) #establishing connection
#     db, client = connect.start_connection() #instantiating db and client
#     for chart in db.find({}, {"name":1, "_id":0}):
#         if chart["name"] in




