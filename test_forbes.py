import requests
from bs4 import BeautifulSoup
import json

url = "https://www.forbes.com/personal-finance/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Сохраним HTML для анализа
        with open('forbes_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("HTML сохранен в forbes_page.html")
        # Попробуем найти заголовки статей
        articles = soup.find_all('article')
        print(f"Найдено article тегов: {len(articles)}")
        for i, article in enumerate(articles[:5]):
            print(f"--- Article {i+1} ---")
            print(article.prettify()[:500])
            print()
        # Поиск по классам
        h3_tags = soup.find_all('h3')
        print(f"Найдено h3 тегов: {len(h3_tags)}")
        for h3 in h3_tags[:10]:
            print(h3.get_text(strip=True))
    else:
        print("Ошибка загрузки страницы")
except Exception as e:
    print(f"Ошибка: {e}")