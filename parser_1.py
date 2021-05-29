import requests
from bs4 import BeautifulSoup
import csv
import subprocess, sys

HOST = 'https://flatfy.ua'
file = 'flats.csv'
url = 'https://flatfy.ua/search?built_year_min=2000&floor_count_min=15&floor_min=10&geo_id=1&price_max=70000&room_count=2&room_count=3&section_id=1&sort=insert_time&sub_geo_id=513762'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
streets = soup.find_all('a', class_='realty-preview__title-link')
prices = soup.find_all('div', class_='realty-preview__price')
number_of_rooms = soup.find_all('span', class_='realty-preview__info rooms')
descriptions = soup.find_all('p', class_='realty-preview__description')

layoyt_content = soup.find('div', class_='realty-content-layout')

with open(file, mode='w', newline='', encoding='utf-8') as w_file:
    writer = csv.writer(w_file, lineterminator='\r\n')
    writer.writerow(['Улица;', 'Цена;', 'Ссылка;', 'Описание;'])
    for i in range(0, len(layoyt_content)):
        streetName = streets[i].text
        price = prices[i].text
        link = HOST + streets[i].get('href')
        description = descriptions[i].text
        writer.writerow([streetName, ';', price, ';', link, ';', description])

        print(f'Улица: {streetName}, цена: {price} \n Описание: \n {description} \n {HOST}{link} \n \n')

pages = soup.find('div', class_='paging__wrapper')
urls = []
links = pages.find_all('a', class_='paging-button')

with open(file, mode='w', newline='', encoding='utf-8') as w_file:
    writer = csv.writer(w_file, lineterminator='\r\n')
    writer.writerow(['Улица;', 'Цена;', 'Ссылка;', 'Описание;'])
    for link in links:
        pageNum = int(link.text) if link.text.isdigit() else None
        if pageNum != None:
            hrefval = link.get('href')
            urls.append(hrefval)
    for slug in urls:
        newUrl = url.replace('?page=1', slug)
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.text, 'lxml')
        streets = soup.find_all('a', class_='realty-preview__title-link')
        for i in range(0, len(streets)):
            streetName = streets[i].text
            price = prices[i].text
            link = HOST + streets[i].get('href')
            description = descriptions[i].text
            writer.writerow([streetName, ';', price, ';', link, ';', description])

            print(f'Улица: {streetName}, цена: {price} \n Описание: \n {description} \n {HOST}{link} \n \n')

opener = "open" if sys.platform == "darwin" else "xdg-open"
subprocess.call([opener, file])
