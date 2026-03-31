import pandas as pd

df = pd.read_csv('enriched_links.csv')
# Удаляем кавычки из description
df['description'] = df['description'].str.replace('"', '')
# Сохраняем без индекса и без BOM
df.to_csv('enriched_links_fixed.csv', index=False, encoding='utf-8-sig')
print("CSV исправлен, сохранен как enriched_links_fixed.csv")