import csv

input_file = 'enriched_links.csv'
output_file = 'enriched_links_fixed2.csv'

with open(input_file, 'r', encoding='utf-8-sig') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        # Убираем кавычки из каждого поля
        row = [field.replace('"', '') for field in row]
        # Заменяем запятые в описании (второе поле) на точку с запятой
        if len(row) > 1:
            row[1] = row[1].replace(',', ';')
        writer.writerow(row)

print(f"CSV исправлен, сохранен как {output_file}")