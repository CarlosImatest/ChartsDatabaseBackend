import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(credentials)
# sheet_names = client.open("AllDensities").worksheets()
# sheet_tile = [name.title for name in sheet_names]

sheet_titles = ['WDR (All)', 'LDR (All)', 'UHDR (All)', 'CRC (All)', 'VISNIR Size C', 'VISNIR', 'Sheet13', 'CRC - All, ’HDR-NIR']

for title in sheet_titles:
    sheet = client.open("AllDensities").worksheet(title)

    data = sheet.get_all_values()

    raw_headers = data[0]
    rows = data[1:]

    seen = defaultdict(int)
    clean_headers = []
    counter = 0
    print(title)
    print(f"before: {counter}")
    for counter, h in enumerate(raw_headers):
        seen[h] += 1

        has_data = (
            len(rows) > 10 and
            counter < len(rows[10]) and
            rows[10][counter]
        )

        if not h and not has_data:
            clean_headers.append(f"space_{seen[h]}")
        else:
            clean_headers.append(
                h if seen[h] == 1 else f"{h}_{seen[h]}"
            )
    print(f"after: {counter}")

    df = pd.DataFrame(rows, columns=clean_headers)
    seen.clear()

    df.to_excel(f"{title}.xlsx", index=False)