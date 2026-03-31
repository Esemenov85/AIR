import pandas as pd
import re

def categorize_url(url):
    """Определяет категорию URL: российский, региональный (Татарстан), международный."""
    # Региональные (Татарстан)
    if re.search(r'\.tatarstan\.ru', url) or re.search(r'kzn\.ru', url) or re.search(r'nabchelny\.ru', url):
        return 'regional'
    # Российские (домены .ru, .рф, .gov.ru, .customs.gov.ru и т.д.)
    if re.search(r'\.ru(?:/|$)', url) or re.search(r'\.рф', url) or re.search(r'\.gov\.ru', url):
        return 'russian'
    # Международные (все остальные)
    return 'international'

def detect_country(url, description):
    """Определяет страну по URL или описанию."""
    # Эвристики по доменам
    if re.search(r'\.sa(?:/|$)', url) or 'saudi' in url.lower():
        return 'Саудовская Аравия'
    if re.search(r'\.ch(?:/|$)', url) or 'switzerland' in url.lower() or 's-ge' in url:
        return 'Швейцария'
    if re.search(r'\.qa(?:/|$)', url) or 'qatar' in url.lower():
        return 'Катар'
    if re.search(r'\.my(?:/|$)', url) or 'malaysia' in url.lower() or 'mida' in url:
        return 'Малайзия'
    if re.search(r'\.cn(?:/|$)', url) or 'china' in url.lower() or 'chinadaily' in url:
        return 'Китай'
    if re.search(r'\.in(?:/|$)', url) or 'india' in url.lower():
        return 'Индия'
    if re.search(r'\.cy(?:/|$)', url) or 'cyprus' in url.lower():
        return 'Кипр'
    if re.search(r'\.kz(?:/|$)', url) or 'kazakhstan' in url.lower():
        return 'Казахстан'
    if re.search(r'\.it(?:/|$)', url) or 'italy' in url.lower():
        return 'Италия'
    if re.search(r'\.fr(?:/|$)', url) or 'france' in url.lower():
        return 'Франция'
    if re.search(r'\.az(?:/|$)', url) or 'azerbaijan' in url.lower():
        return 'Азербайджан'
    if re.search(r'\.kr(?:/|$)', url) or 'korea' in url.lower():
        return 'Южная Корея'
    if re.search(r'\.de(?:/|$)', url) or 'germany' in url.lower():
        return 'Германия'
    if re.search(r'\.org(?:/|$)', url) and ('unctad' in url or 'imf' in url or 'worldbank' in url):
        return 'Международная организация'
    if re.search(r'\.com(?:/|$)', url) and ('dinarstandard' in url):
        return 'США (исламская экономика)'
    # По умолчанию
    return 'Другая'

def main():
    df = pd.read_csv('extracted_links.csv')
    
    # Применяем категоризацию
    df['category'] = df['url'].apply(categorize_url)
    df['country'] = df.apply(lambda row: detect_country(row['url'], row['description']), axis=1)
    
    # Подсчет метрик
    total_links = len(df)
    russian_links = len(df[df['category'] == 'russian'])
    regional_links = len(df[df['category'] == 'regional'])
    international_links = len(df[df['category'] == 'international'])
    
    # Разбивка международных по странам
    international_df = df[df['category'] == 'international']
    country_counts = international_df['country'].value_counts().to_dict()
    
    # Ссылки, связанные с инвестициями (эвристика по ключевым словам)
    investment_keywords = ['инвест', 'invest', 'investment', 'гид', 'guide', 'отчет', 'report', 'экономик', 'economy', 'бизнес', 'business']
    def is_investment(desc, url):
        text = (desc + ' ' + url).lower()
        return any(keyword in text for keyword in investment_keywords)
    
    df['investment'] = df.apply(lambda row: is_investment(row['description'], row['url']), axis=1)
    investment_links = df[df['investment']]
    
    print("=== МЕТРИКИ ===")
    print(f"Всего ссылок: {total_links}")
    print(f"Российские: {russian_links} (из них региональные (Татарстан): {regional_links})")
    print(f"Международные: {international_links}")
    print("\nРазбивка международных по странам:")
    for country, count in country_counts.items():
        print(f"  {country}: {count}")
    
    print(f"\nСсылки, связанные с инвестициями: {len(investment_links)}")
    
    # Сохраняем обогащенные данные
    df.to_csv('enriched_links.csv', index=False, encoding='utf-8-sig')
    print("\nОбогащенные данные сохранены в enriched_links.csv")
    
    # Генерируем JSON для использования в веб-странице
    import json
    metrics = {
        'total_links': total_links,
        'russian_links': russian_links,
        'regional_links': regional_links,
        'international_links': international_links,
        'country_counts': country_counts,
        'investment_links_count': len(investment_links),
        'investment_links': investment_links[['sheet', 'description', 'url']].to_dict('records')
    }
    with open('metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print("Метрики сохранены в metrics.json")

if __name__ == '__main__':
    main()