import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
import json


# Load the Excel file
df = pd.read_excel('WDR_clean.xlsx')
layer_1 = []
layer_2 = []
final_layer = []
col_names = []
film_type = ""
#drops all rows with NaN
df.dropna(how='all', inplace=True)
#fills all cells with NaN with empty space
df = df.fillna("")
# Select all columns that contain 'space_' and drop them
df = df.drop(columns=df.filter(like='space_').columns)
raw_columns = df.columns


#looks for .env file in current dir
load_dotenv("/Users/imatest_carlos/Desktop/Imatest/ChartDatabaseProject/backend/pymongo-quickstart/.env")

# variable names from Atlas-generated .env
uri     = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB_NAME", "WDR")
client = MongoClient(uri, tlsCAFile=certifi.where())


database = client.get_database(db_name)
wdr   = database["test"]

# View the first 5 rows
counter = 0
for col_name in raw_columns:
    temp_col_value = df[col_name]
    col_names.append(col_name)
    print(col_names)
    counter +=1

    for value in temp_col_value:
        if value == "Fujifilm":
            film_type = value
            continue
        elif value == "Kodak":
            film_type = value
            continue

        
        if counter == 1:
            if value:
                layer_1.append(value)
        elif counter == 2:
            if value:
                layer_2.append(value)
        if counter == 3:
            if value:
                final_layer.append(value)

            
    if counter == 3:
        wdr.insert_one({"name": col_names[-1], 
                        "layer1": col_names[0], 
                        "layer2": col_names[1],
                        "film_type": film_type,
                        "layer1_values": layer_1,
                        "layer2_values": layer_2,
                        "L1+L2": final_layer})
        layer_1.clear()
        layer_2.clear()
        final_layer.clear()
        col_names.clear()
        counter = 0
        continue

client.close()