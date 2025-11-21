import time
from modules.google_sheets_api.google_sheets import GoogleSheet
from modules.utils.utils import *
from CONFIG import *

g = GoogleSheet(CREDENTIALS_DIR)

#Перевіряємо чи існує вихідна таблиця, якщо ні — створюємо
if not OUTPUT_SPREADSHEET_ID:
    OUTPUT_SPREADSHEET_ID = g.create_spreadsheets("Test_task")

# Перевіряємо чи існують потрібні листи, якщо ні — копіюємо з шаблону і перейменовуємо
if not g.is_sheet_exist(OUTPUT_SPREADSHEET_ID, INPUT_SHEET_NAME) \
   and not g.is_sheet_exist(OUTPUT_SPREADSHEET_ID, OUTPUT_SHEET_NAME):

    for name in [INPUT_SHEET_NAME, OUTPUT_SHEET_NAME]:
        copied = g.copy_sheeet(
            spreadsheetId=INPUT_SPREADSHEET_ID,
            destinationSpreadsheetId=OUTPUT_SPREADSHEET_ID
        )
        g.rename_sheet(OUTPUT_SPREADSHEET_ID, name, copied.get("sheetId"))

# Отримуємо всі листи в таблиці
all_sheets = g.get_all_sheets(OUTPUT_SPREADSHEET_ID)

# Отримуємо об’єкти потрібних листів
ws_work = g.get_sheet_info_by_name(OUTPUT_SPREADSHEET_ID, OUTPUT_SHEET_NAME)
ws_input = g.get_sheet_info_by_name(OUTPUT_SPREADSHEET_ID, INPUT_SHEET_NAME)

# Видаляємо зайві листи
del_list = [s for s in all_sheets if s not in [ws_work, ws_input]]
for s in del_list:
    g.delete_sheet(OUTPUT_SPREADSHEET_ID, s.get("sheetId"))

# Отримуємо кількість рядків та стовпців вхідного листа
rows_count = int(ws_input.get("gridProperties").get("rowCount"))
cols_count = int(ws_input.get("gridProperties").get("columnCount"))

# Очищуємо вихідний лист перед записом нових даних
g.clear_range(
    OUTPUT_SPREADSHEET_ID,
    OUTPUT_SHEET_NAME,
    f"A2:O{ws_work.get('gridProperties').get('rowCount')}"
)

# Зчитуємо заголовки стовпців для подальшої обробки
row_headers = g.read_row(OUTPUT_SPREADSHEET_ID, 1, OUTPUT_SHEET_NAME)
check_cells = get_cells_to_update(COLUMN_ARGUMENT, row_headers)

# Проходимо по кожному рядку вхідного листа і обробляємо
for row in range(2, rows_count + 1):
    attempt = 0
    while attempt < 3:
        try:
            time.sleep(1.2)  # невелика затримка для уникнення обмежень API
            read_row = g.read_row(OUTPUT_SPREADSHEET_ID, row, INPUT_SHEET_NAME)
            if "values" not in read_row or not read_row["values"]:
                break  # якщо рядок пустий, пропускаємо
            original = read_row["values"][0]
            fields = [original[i] for i in check_cells]
            r = make_new_range(fields).astype(str)
            rows_to_insert = expand_row_with_range(original, check_cells, r)
            g.update_rows(
                OUTPUT_SPREADSHEET_ID,
                rows_to_insert,
                ws_work.get("sheetId")
            )
            break
        except (TypeError, IndexError):
            attempt += 1
            time.sleep(1)  # чекаємо перед повторною спробою

# Завантажуємо оброблені дані у CSV
g.download_sheet_as_csv(
    OUTPUT_SPREADSHEET_ID,
    OUTPUT_SHEET_NAME,
    save_path=EXPORTS_DIR,
    filename=CSV_FILENAME
)

