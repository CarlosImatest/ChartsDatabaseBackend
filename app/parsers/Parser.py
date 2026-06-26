#instruments: Barbieri, Densitometer, i1Pro

import gspread
from google.oauth2.service_account import Credentials

class Parser:

    def google_parser():
        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ]

        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )

        client = gspread.authorize(creds)

        sheet = client.open("Chart Reference Database")

        worksheet = sheet.sheet1

        rows = worksheet.get_all_records()

        for row in rows:
            print(row)





test1 = Parser
test1.google_parser()