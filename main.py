import json
import time
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import datetime
import csv

cards_data = []
start_time = time.time()
headers = {
    'Accept': "*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def get_card_data(session, card_url):
    """
    Gathering data from objects
    """
    card_page = await fetch(session, card_url)
    soup = BeautifulSoup(card_page, 'html.parser')

    name = soup.select_one('h1.h2')
    seller = soup.select_one('a.border-bottom-link.uppercase')
    price = soup.select_one('span.add-to-cart__price')

    return {
        'name': name.text.strip() if name else "Название не найдено",
        'seller': seller.text.strip() if seller else "Производитель не найден",
        'price': price.text.strip() if price else "Цена не найдена"
    }


async def get_page_data(session, page):
    """
    Collection objects address
    """
    url = f'https://rareplayingcards.com/collections/limited-edition?page={page}'
    response_text = await fetch(session, url)
    soup = BeautifulSoup(response_text, 'html.parser')

    all_cards_hrefs = soup.select('.lazy-image.double__image')

    tasks = []
    for card_adr in all_cards_hrefs:
        card_data = card_adr.get('href')
        task = asyncio.create_task(get_card_data(session, f'https://rareplayingcards.com{card_data}'))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    cards_data.extend(results)
    print(f'[INFO] Обработал страницу {page}')


async def gather_data():
    """
    Getting pages count
    """
    url = 'https://rareplayingcards.com/collections/limited-edition'

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url)
        soup = BeautifulSoup(response, 'html.parser')
        page_count = int(soup.select_one("ul.pagination-custom").find_all("a")[-2].text)

        tasks = [asyncio.create_task(get_page_data(session, page)) for page in range(1, page_count + 1)]
        await asyncio.gather(*tasks)


def main():
    """
    Writing csv and json docs
    """
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f'rareplayingcards_{cur_time}_async.csv', "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(('Название колоды', 'Производитель', 'Цена'))
        writer.writerows([(card["name"], card["seller"], card["price"]) for card in cards_data])

    with open(f'rareplayingcards_{cur_time}_async.json', "w", encoding="utf-8") as json_file:
        json.dump(cards_data, json_file, ensure_ascii=False, indent=4)

    finish_time = time.time() - start_time
    print(f"Затраченное на работу время: {finish_time:.2f} секунд")

if __name__ == "__main__":
    main()
