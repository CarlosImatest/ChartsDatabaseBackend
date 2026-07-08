import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2])) # go up 3 levels: parsers -> app -> backend
from app.db.mDB_connect_to_db import DbConnect
from app.parsers.clean_xlsx import CleanXlsx
from app.models.chart import Chart, Layer



class Parser_test:
    def __init__(self,db_name, collection_name, file_name):
        self.file_name = file_name
        #starting connection to DB
        connect = DbConnect(db_name, collection_name)
        self.collection, self.client = connect.start_connection()

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

                keys = list(dict_data.keys())


                # create final layer
                final_layer = Layer(
                    name=keys[-1],
                    values=dict_data[keys[-1]]
                )


                # remove final layer from normal layers
                keys.pop()


                # create all other layers
                layers = []

                for key in keys:
                    layer = Layer(
                        name=key,
                        values=dict_data[key]
                    )

                    layers.append(layer)


                # create complete chart object
                chart = Chart(
                    name=final_layer.name,
                    film_type=film_type,
                    layers=layers,
                    final_layer=final_layer
                )
                #inserting to database
                self.collection.insert_one(chart.model_dump())
                #clearing the variables
                film_type = ""
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