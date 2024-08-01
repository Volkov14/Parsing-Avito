import csv
from bs4 import BeautifulSoup
import requests
import time

base_url = 'https://www.avito.ru'
url = "https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&f=ASgBAQICAUSwCNRWAUCeww2E0NWOA~TjOeLjOZDZOY7ZOYzZOYjZOYbZOQ&s=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


response = requests.get(url, headers=headers)
response.encoding = 'utf-8'


if response.status_code != 200:
    print(f"Ошибка запроса: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

data = []

# тут парсим карточки объявлений (отдельные окна)
cards = soup.find_all('div', class_='iva-item-root-_lk9K')  # Класс для карточки объявления

for card in cards:
    # парсим ссылку на карточку (отдельное окно)
    link_tag = card.select_one('a.iva-item-sliderLink-uLz1v')
    link = base_url + link_tag.get('href') if link_tag else 'N/A'

    # Парсим адрес, указанный в объявлении по классу
    address_tag = card.select_one('span.style-item-address__string-wt61A')
    address = address_tag.text.strip() if address_tag else 'N/A'

    # ссылку и адрес добавляем в пустой список
    data.append({'link': link, 'address': address})

# Проверка на успешность выполнения
if not data:
    print("Не удалось извлечь данные. Проверьте правильность HTML-классов.")
else:
    # Запись данных в CSV-файл
    csv_file = 'avito_data.csv'
    csv_columns = ['link', 'address']

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except IOError:
        print("Ошибка при сохранении в файл.")

    print("Парсинг завершён, данные сохранены в", csv_file)
