import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2])) # go up 3 levels: parsers -> app -> backend
from app.db.mDB_connect_to_db import DbConnect
from app.parsers.clean_xlsx import CleanXlsx



class Parser_test:
    def __init__(self,db_name, collection_name, file_name):
        self.file_name = file_name
        #starting connection to DB
        connect = DbConnect(db_name, collection_name)
        self.db, self.client = connect.start_connection()

        self.df = CleanXlsx(self.file_name)
        self.df = self.df.clean()

    def parse(self):

        dict_data = {}
        film_type = ""

        for column in self.df.columns:

            if "space_" in column:
                if not dict_data:
                    print("dict_emtpy")
                    continue

                keys = list(dict_data.keys()) #getting the film's layer name

                document = {
                    "name": keys[-1],
                    "film_type": film_type,
                    "final_layer_value": dict_data[keys[-1]]
                }

                keys.pop() #removing the last entry from key

                #iterating the the rest of layers
                for i in range(len(keys)):
                    document[f"layer{i+1}_name"] = keys[i]
                    document[f"layer_{i+1}_value"] = dict_data[keys[i]]

                #inserting to database
                self.db.insert_one(document)

                #clearing the variables
                film_type = ""
                document.clear()
                dict_data.clear()

                continue

            #getting the values from the dataframe
            values = self.df[column]

            #making a dictionary and storing the values in an array
            dict_data[column] = []
            for value in values:
                if value in ("Kodak", "Fujifilm"):
                    film_type = value
                    continue
                if value:
                    dict_data[column].append(value)
        print(f"Done uploading file: {self.file_name}")

            

        self.client.close()