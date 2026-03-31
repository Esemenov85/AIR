import requests
from bs4 import BeautifulSoup
import json
import time

url = "https://www.forbes.com/personal-finance/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

try:
    response = requests.get(url, headers=headers, timeout=30)
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
        # Поиск ссылок
        links = soup.find_all('a', href=True)
        article_links = [a['href'] for a in links if '/article/' in a['href'] or '/personal-finance/' in a['href']]
        print(f"Найдено ссылок на статьи: {len(article_links)}")
        for link in article_links[:5]:
            print(link)
    else:
        print("Ошибка загрузки страницы")
except Exception as e:
    print(f"Ошибка: {e}")