import requests
from bs4 import BeautifulSoup
import csv
import os
from time import sleep
from collections import defaultdict


def get_animals_count():
    base_url = "https://ru.wikipedia.org"
    start_url = base_url + "/wiki/Категория:Животные_по_алфавиту"

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    letter_counts = defaultdict(int)
    processed_urls = set()
    queue = [start_url]

    while queue:
        current_url = queue.pop(0)
        if current_url in processed_urls:
            continue

        print(f"Обрабатываю: {current_url}")

        try:
            response = session.get(current_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Обрабатываем животных на текущей странице
            process_animals(soup, letter_counts)

            # Находим все ссылки на другие страницы категории
            new_links = find_category_links(soup, base_url)
            queue.extend(new_links)

            processed_urls.add(current_url)
            sleep(1)

        except Exception as e:
            print(f"Ошибка при обработке {current_url}: {e}")
            continue

    return dict(letter_counts)


def process_animals(soup, letter_counts):
    category_div = soup.find('div', {'class': 'mw-category'})
    if not category_div:
        return

    for link in category_div.find_all('a'):
        name = link.get_text().strip()
        if not name:
            continue

        first_char = name[0].upper()
        if first_char.isalpha() and 'А' <= first_char <= 'Я':
            letter_counts[first_char] += 1


def find_category_links(soup, base_url):
    links = []

    # Ссылки на следующие страницы
    next_page = soup.find('a', text='Следующая страница')
    if next_page:
        links.append(base_url + next_page['href'])

    # Ссылки на подкатегории (по буквам)
    subcats = soup.find('div', {'id': 'mw-subcategories'})
    if subcats:
        for link in subcats.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                links.append(base_url + href)

    return links


def save_results(letter_counts, filename='beasts.csv'):
    full_path = os.path.abspath(filename)

    # Сортируем по русскому алфавиту
    sorted_letters = sorted(
        [(k, v) for k, v in letter_counts.items() if v > 0],
        key=lambda x: ord(x[0])
    )

    try:
        with open(full_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Буква', 'Количество'])
            writer.writerows(sorted_letters)

        print(f"Результаты сохранены в {full_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


if __name__ == '__main__':
    print("=== Начало работы ===")

    counts = get_animals_count()
    total = sum(counts.values())
    print(f"\nИтого найдено: {total} животных")

    # Выводим статистику
    for letter, count in sorted(counts.items(), key=lambda x: ord(x[0])):
        print(f"{letter}: {count}")

    if save_results(counts):
        print("Сохранение завершено успешно")
    else:
        print("Не удалось сохранить результаты")

    print("=== Работа завершена ===")
