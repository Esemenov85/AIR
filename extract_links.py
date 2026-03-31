import pandas as pd
import re

def extract_links_from_excel(file_path):
    xls = pd.ExcelFile(file_path)
    links = []
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)  # без заголовков, чтобы обрабатывать произвольные структуры
        # Проходим по всем ячейкам
        for row_idx, row in df.iterrows():
            for col_idx, cell in enumerate(row):
                if isinstance(cell, str):
                    # Ищем URL-подобные строки
                    urls = re.findall(r'https?://[^\s<>"\']+', cell)
                    for url in urls:
                        # Описание: берем текст слева от URL или название столбца/листа
                        description = cell[:cell.find(url)].strip()
                        if not description:
                            # Если описание пустое, используем название листа и координаты
                            description = f"{sheet_name} (строка {row_idx+1}, колонка {col_idx+1})"
                        links.append({
                            'sheet': sheet_name,
                            'description': description,
                            'url': url,
                            'row': row_idx+1,
                            'col': col_idx+1
                        })
                elif pd.notna(cell):
                    # Если ячейка не строка, но содержит что-то, можно проверить, не является ли это URL (маловероятно)
                    pass
    return links

def main():
    file_path = "Ссылки на сайты_13.03.2026.xlsx"
    links = extract_links_from_excel(file_path)
    
    print(f"Найдено ссылок: {len(links)}")
    for link in links:
        print(f"{link['description']} -> {link['url']}")
    
    # Сохраним в CSV для дальнейшего использования
    df_out = pd.DataFrame(links)
    df_out.to_csv('extracted_links.csv', index=False, encoding='utf-8-sig')
    print("Ссылки сохранены в extracted_links.csv")
    
    # Также сохраним в простой текстовый файл
    with open('extracted_links.txt', 'w', encoding='utf-8') as f:
        for link in links:
            f.write(f"{link['description']}\t{link['url']}\n")
    print("Ссылки сохранены в extracted_links.txt")

if __name__ == '__main__':
    main()