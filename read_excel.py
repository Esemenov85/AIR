import pandas as pd
import sys

file_path = "Ссылки на сайты_13.03.2026.xlsx"
try:
    # Читаем все листы
    xls = pd.ExcelFile(file_path)
    print(f"Листы: {xls.sheet_names}")
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
        print(f"\n--- Лист: {sheet} ---")
        print(f"Колонки: {list(df.columns)}")
        print(f"Первые строки:")
        print(df.head())
except Exception as e:
    print(f"Ошибка: {e}")
    sys.exit(1)