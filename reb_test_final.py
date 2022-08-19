import json
import time
import requests
from bs4 import BeautifulSoup
import asyncio
import datetime
import csv

main_page = 'https://rareplayingcards.com/collections/limited-edition'

headers = {
    'Accept': "	*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

start_time = time.time()


async def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f'rareplayingcards_{cur_time}.csv', "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Название колоды',
                'Производитель',
                'Цена'
            )
        )

    url = 'https://rareplayingcards.com/collections/limited-edition'

    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")

    page_count = int(soup.find("ul", class_="pagination-custom").find_all("a")[-2].text)

    cards_data = []

    for page in range(1, page_count + 1):

        response = requests.get(f'https://rareplayingcards.com/collections/limited-edition?page={page}', headers).text
        soup = BeautifulSoup(response, 'lxml')

        for adr_part in soup.find_all('a', class_='h5--accent strong name_wrapper'):
            card_adr = '-'.join(adr_part.text.split())                           # ДОБАВИТЬ remove('-')

            card_page = requests.get(f'https://rareplayingcards.com/collections/limited-edition/products/{card_adr}',
                                     headers).text
            soup = BeautifulSoup(card_page, 'lxml')

            try:
                name = soup.find('h1', class_='h2').text.strip()
            except:
                name = "Название не найдено"

            try:
                seller = soup.find('a', class_='border-bottom-link uppercase').text.strip()
            except:
                seller = "Производитель не найден"
            try:
                price = soup.find('span', class_='add-to-cart__price').text.strip()
            except:
                price = "Цена не найдена"

                cards_data.append(
                    {
                        'name': name,
                        'seller': seller,
                        'price': price
                    }
                )

            with open(f'rareplayingcards_{cur_time}.csv', "a", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        name,
                        seller,
                        price
                    )
                )

        print(f"Обработана {page}/{page_count}")
        time.sleep(1)

    with open(f'rareplayingcards_{cur_time}.json', "w") as file:
        json.dump(cards_data, file, indent=4, ensure_ascii=False)


def main():
    asyncio.run(get_data())
    finish_time = time.time() - start_time
    print(f"Затраченное на работу время: {finish_time}")


if __name__ == '__main__':
    main()