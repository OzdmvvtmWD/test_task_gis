Налаштування

1. Google Sheets API
- Створіть client secret file для роботи з Google Sheets API.
- Інструкція: https://developers.google.com/workspace/drive/api/quickstart/python
- Завантажте файл у форматі .json і помістіть його в папку credentials.
- Назвіть файл credential.json.

2. Віртуальне оточення Python
- Створіть оточення та активуйте його:
  python -m venv .venv
  .venv\Scripts\activate
- Встановіть необхідні бібліотеки:
  pip install -r requirements.txt

3. Створення токена доступу
- При першому запуску create_token.pickle.py відкриється вікно авторизації Google.
- Виберіть Google акаунт, куди будуть завантажуватися результати.
- Після успішної авторизації згенерується файл token.pickle, який використовується для подальшого доступу до Google Sheets API без повторної авторизації.

4. Конфігурація
- У файлі CONFIG.py можна додатково налаштувати назви файлів та шляхи.

5. Конфігурація.env
- У файлі .env зберігаються дані для входу в ArcGIS:  
- USERNAME_GIS – ім'я користувача GIS  
- PASSWORD_GIS – пароль користувача GIS

Хід завдання 
Частина 1: Робота з табличними даними Google Spreadsheets
Cкрипт 1_script_google_sheet_automatization.py

Цей скрипт автоматизує обробку даних у Google Sheets та їх експорт у CSV.  

Імпортуються модулі для роботи з Google Sheets (GoogleSheet) та допоміжні функції з utils. Для роботи необхідні локальні облікові дані (.json), що зберігаються в CREDENTIALS_DIR.  

Ініціалізується об’єкт GoogleSheet:

g = GoogleSheet(CREDENTIALS_DIR)

Перевіряється наявність вихідної таблиці, якщо її немає, створюється нова з назвою "Test_task".  

Перевіряється наявність листів INPUT_SHEET_NAME та OUTPUT_SHEET_NAME. Якщо листи відсутні, вони копіюються зі стандартного шаблону та перейменовуються.  

Отримуються об’єкти всіх листів і видаляються зайві листи, що не потрібні для роботи.  

Визначається кількість рядків та стовпців у вхідному листі. Вихідний лист очищується перед записом нових даних:

g.clear_range(OUTPUT_SPREADSHEET_ID, OUTPUT_SHEET_NAME, f"A2:O{ws_work.get('gridProperties').get('rowCount')}")

Зчитуються заголовки стовпців, визначаються індекси стовпців для оновлення. Проходження по кожному рядку вхідного листа виконується з повторними спробами у випадку помилок. Рядки обробляються функціями make_new_range та expand_row_with_range. Оброблені рядки записуються у вихідний лист.  

Виконується експорт оброблених даних у CSV:

g.download_sheet_as_csv(OUTPUT_SPREADSHEET_ID, OUTPUT_SHEET_NAME, save_path=EXPORTS_DIR, filename=CSV_FILENAME)

Використовується затримка time.sleep(1.2) для уникнення обмежень API Google. Пропущені або порожні рядки автоматично ігноруються. Обробка помилок реалізована через три спроби для кожного рядка (TypeError та IndexError).

Частина 2: Внесення підготовлених даних до Hotsed Feature Layer

Скрипт 2_script_gis_automatization.py

Скрипт автоматизує завантаження підготовлених даних у Hosted Feature Layer на ArcGIS Online.

Імпортуються модулі для роботи з ArcGIS через кастомний драйвер GISDriver та dotenv для завантаження змінних середовища.

Змінні USERNAME та PASSWORD підвантажуються з .env файлу:

USERNAME = os.environ.get('USERNAME_GIS')
PASSWORD = os.environ.get('PASSWORD_GIS')

Ініціалізується підключення до порталу через GISDriver:

gis_custom = GISDriver(USERNAME, PASSWORD, PORTAL_URL)

Отримується елемент (item) по його ID:

test_item = gis_custom.get_item(TEST_ITEM_ID)

Переконуємося, що існує робоча папка WORK_FOLDER_NAME, якщо ні — створюємо її.
Копіюємо елемент у робочу папку:

test_item_copy = gis_custom.clone_item_to_folder(TEST_ITEM_ID, WORK_FOLDER_NAME)
test_layer_copy  = test_item_copy.layers[0]

Отримуємо список полів шару:

gis_custom.get_layer_fields(test_layer_copy)

Видаляємо всі існуючі об’єкти шару перед завантаженням нових даних:

gis_custom.delete_all_features(test_layer_copy)

Додаємо дані з CSV до шару:

gis_custom.add_csv(test_layer_copy, CSV_PATH)

Видаляємо непотрібні поля з шару:

gis_custom.delete_garbage_field(test_layer_copy,'Область')
gis_custom.delete_garbage_field(test_layer_copy,'date_1')
gis_custom.delete_garbage_field(test_layer_copy,'date__')
gis_custom.delete_garbage_field(test_layer_copy,'GlobalID')
