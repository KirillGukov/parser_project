import requests
from bs4 import BeautifulSoup
import asyncio

main_page = 'https://rareplayingcards.com/collections/limited-edition'

headers = {
    'Accept': "	*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}


async def reb_func():
    page = 1
    for _ in range(8):
        start_page = requests.get('https://rareplayingcards.com/collections/limited-edition?page=1', headers).text
        soup = BeautifulSoup(start_page, 'lxml')

        for adr_part in soup.find_all('p', class_='h5--accent strong name_wrapper'):
            card_adr = '-'.join(adr_part.text.split())                                           # ДОБАВИТЬ remove('-')

            card_page = requests.get(f'https://rareplayingcards.com/collections/limited-edition/products/{card_adr}', headers).text
            soup = BeautifulSoup(card_page, 'lxml')

            for name in soup.find_all('h1', class_='h2'):
                print(name.text.strip())
            for price in soup.find_all('span', class_='add-to-cart__price'):
                print(price.text.strip())
        page += 1

asyncio.run(reb_func())