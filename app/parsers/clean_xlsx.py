import pandas as pd

class CleanXlsx:
    def __init__(self, xlsx_name):
        self.xlsx_name = xlsx_name

    def clean(self):
        # Load the Excel file
        df = pd.read_excel(self.xlsx_name)
        #drops all rows with NaN
        df.dropna(how='all', inplace=True)
        #fills all cells with NaN with empty space
        df = df.fillna("")
        # # Select all columns that contain 'space_' and drop them
        # df = df.drop(columns=df.filter(like='space_').columns)
        
        return df