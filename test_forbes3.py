import cloudscraper
from bs4 import BeautifulSoup
import time

url = "https://www.forbes.com/personal-finance/"

scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
try:
    print("Загружаем страницу через cloudscraper...")
    response = scraper.get(url, timeout=30)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('forbes_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("HTML сохранен в forbes_page.html")
        # Поиск заголовков
        h3_tags = soup.find_all('h3')
        print(f"Найдено h3 тегов: {len(h3_tags)}")
        for h3 in h3_tags[:15]:
            text = h3.get_text(strip=True)
            if text:
                print(f"- {text}")
        # Поиск ссылок на статьи
        links = soup.find_all('a', href=True)
        article_links = []
        for a in links:
            href = a['href']
            if '/article/' in href or '/personal-finance/' in href:
                if not href.startswith('http'):
                    href = 'https://www.forbes.com' + href
                article_links.append(href)
        article_links = list(set(article_links))
        print(f"Уникальных ссылок на статьи: {len(article_links)}")
        for link in article_links[:5]:
            print(link)
    else:
        print("Ошибка загрузки страницы")
except Exception as e:
    print(f"Ошибка: {e}")