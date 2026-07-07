from parser_test import Parser_test

file_name = ["CRC_clean.xlsx", "LDR_clean.xlsx", "UHDR_clean.xlsx", "VISNIR_clean.xlsx", "WDR_clean.xlsx"]
collection_name = ["CRC", "LDR", "UHDR", "VISNIR", "WDR"]
database_name = "Charts"

for i in range(len(file_name)):
    insert_data = Parser_test(database_name, collection_name[i], file_name[i] )
    insert_data.parse()
