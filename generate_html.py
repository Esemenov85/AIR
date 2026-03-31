import pandas as pd
import html

def generate_html(csv_path='extracted_links.csv', output_path='links.html'):
    df = pd.read_csv(csv_path)
    
    # Экранируем описание и URL для безопасности HTML
    df['description_esc'] = df['description'].apply(html.escape)
    df['url_esc'] = df['url'].apply(html.escape)
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ссылки из Excel-файла</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            background-color: white;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #e0f7fa;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .count {
            margin-bottom: 10px;
            font-size: 1.1em;
            color: #555;
        }
        .sheet {
            font-size: 0.9em;
            color: #777;
        }
    </style>
</head>
<body>
    <h1>Ссылки из файла "Ссылки на сайты_13.03.2026.xlsx"</h1>
    <div class="count">Всего ссылок: """ + str(len(df)) + """</div>
    <table>
        <thead>
            <tr>
                <th>№</th>
                <th>Описание</th>
                <th>Ссылка</th>
                <th>Лист</th>
                <th>Строка</th>
                <th>Колонка</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for idx, row in df.iterrows():
        html_content += f"""
            <tr>
                <td>{idx+1}</td>
                <td>{row['description_esc']}</td>
                <td><a href="{row['url_esc']}" target="_blank">{row['url_esc']}</a></td>
                <td class="sheet">{row['sheet']}</td>
                <td>{row['row']}</td>
                <td>{row['col']}</td>
            </tr>
        """
    
    html_content += """
        </tbody>
    </table>
    <p style="margin-top: 30px; font-size: 0.9em; color: #888;">
        Сгенерировано автоматически из Excel-файла.
    </p>
</body>
</html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML-страница сохранена в {output_path}")

if __name__ == '__main__':
    generate_html()