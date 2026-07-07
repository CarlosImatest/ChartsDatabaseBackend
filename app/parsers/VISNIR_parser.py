import sys
from pathlib import Path

# go up 3 levels: parsers -> app -> backend
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.mDB_connect_to_db import DbConnect
from app.parsers.clean_xlsx import CleanXlsx

#starting connection to DB
connect = DbConnect("Charts","VISNIR")
db, client = connect.start_connection()

df = CleanXlsx("VISNIR_clean.xlsx")
df = df.clean()
# layer_1 = []
# layer_2 = []
# final_layer = []
# layer_name = []
# film_type = ""
# raw_columns = df.columns
# counter = 0

dict_data = {}
film_type = ""
counter = 0

for column in df.columns:

    if "space_" in column:
        # if counter == 1:
        #     db.insert_one({
        #         "name": layer_name[1],
        #         "layer_1": layer_1,
        #         "film_type":film_type,
        #         "layer1": layer_1
        #     })
        print(len(dict_data))
        document = {}
        first_key = next(iter(my_dict))
        for i in range(len(dict_data)):
            counter += 1
            layer_name, layer_value = dict_data.popitem()
            print(layer_name)
            if "name" not in document:
                document = {
                    "name": layer_name,
                    "film_type": film_type,
                    "L1+L2":layer_value}
                continue
            
            document[f"layer{i-}_name"] = layer_name
            document[f"layer{i-1}_value"] = layer_value
        # for i in range(len(layer_value)):
        #     document[f"layer{i+1}"] = layer_value[i]
        #     if i == len(layer_value)-1:
        #         document["L1_L2"] = layer_value[i]

        # else:
        #     db.insert_one({
        #         "name": layer_name[-1], 
        #         "layer1": layer_name[0], 
        #         "layer2": layer_name[1],
        #         "film_type": film_type,
        #         "layer1_values": layer_1,
        #         "layer2_values": layer_2,
        #         "L1_L2": final_layer
        #     })
            
        # layer_1.clear()
        # layer_2.clear()
        # final_layer.clear()
        film_type = ""
        counter = 0
        db.insert_one(document)
        continue

    # counter += 1
    # layer_name.append(column)
    values = df[column]

    dict_data[column] = []
    # print(column)

    

    for value in values:
        if value in ("Kodak", "Fujifilm"):
            film_type = value
            continue
        if value:
            dict_data[column].append(value)

        # if counter == 1:
        #     if value:
        #         layer_1.append(value)
        # elif counter == 2:
        #     if value:
        #         layer_2.append(value)
        # elif counter == 3:
        #     if value:
        #         final_layer.append(value)

        # if value:
        #     dict_data[column].appen(value)

    

client.close()