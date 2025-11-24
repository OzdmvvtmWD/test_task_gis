import os


BASE_DIR = os.path.abspath(os.getcwd())

CSV_FILENAME = "processed_data.csv"
CSV_PATH = os.path.join(BASE_DIR, "exports", CSV_FILENAME)

CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")

PORTAL_URL = "https://www.arcgis.com"

TEST_ITEM_ID = "61da4ed4a1b040929a705873b44166f6"

WORK_FOLDER_NAME = "Test"

INPUT_SPREADSHEET_ID = "12846JbH2PwR0wN8eLVnosg4xujw-04gKyyD6RuElc-4"
INPUT_SHEET_NAME = "Дані_Початкові"

OUTPUT_SPREADSHEET_ID = "1pigm2Hs6RIFfIKmCAixcGZ0Mslg-DwaL2AAN1--qP6A"
# OUTPUT_SPREADSHEET_ID = None
OUTPUT_SHEET_NAME = "Дані_Оброблені"

COLUMN_ARGUMENT = "Значення"
