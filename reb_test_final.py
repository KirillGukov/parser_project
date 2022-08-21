import json
import time
import requests
from bs4 import BeautifulSoup
import asyncio
import datetime
import csv
import aiohttp

cards_data = []                                                                                                         # список для данных по колодам
start_time = time.time()                                                                                                # задаем время начала скрипта


async def get_page_data(session, page):                                                                                 # задача для выполнения с параметрами сессии и страницы
    headers = {
        'Accept': "	*/*",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    url = f'https://rareplayingcards.com/collections/limited-edition?page={page}'                                       # задаем адресс сайта с пагинацией страницы

    async with session.get(url=url, headers=headers) as response:                                                       # отправляем запрос на страницу
        response_text = await response.text()                                                                           # сохраняем ответ в переменную

        soup = BeautifulSoup(response_text, 'lxml')                                                                     # создаем объект супа

        all_cards_hrefs = soup.find_all(class_='lazy-image double__image')                                              # парсим все карточки с колодами

        for card_adr in all_cards_hrefs:                                                                                # проходим по всем карточкам на странице
            card_data = card_adr.get('href')                                                                            # забираем данные по тэгу href

            card_page = requests.get(f'https://rareplayingcards.com{card_data}',                                        # отправляем запрос на страницу колоды
                                     headers).text
            soup = BeautifulSoup(card_page, 'lxml')                                                                     # создаем объект супа

            try:
                name = soup.find('h1', class_='h2').text.strip()                                                        # берем название колоды с ее страницы
            except:
                name = "Название не найдено"

            try:
                seller = soup.find('a', class_='border-bottom-link uppercase').text.strip()                             # берем название производителя со страницы колоды
            except:
                seller = "Производитель не найден"
            try:
                price = soup.find('span', class_='add-to-cart__price').text.strip()                                     # берем цену колоды с ее страницы
            except:
                price = "Цена не найдена"

            cards_data.append(                                                                                          # добавляем данные о колодах
                {
                    'name': name,
                    'seller': seller,
                    'price': price
                }
            )
    print(f'[INFO] Обработал страницу {page}')                                                                      # выводим кол-во обработанных страниц


async def gather_data():                                                                                                # формируем список задач
    headers = {                                                                                                         # вносим данные о user-agent
        'Accept': "	*/*",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    url = 'https://rareplayingcards.com/collections/limited-edition'                                                    # задаем адресс сайта

    async with aiohttp.ClientSession() as session:                                                                      # создаем клиент-сессию, которая позволяет использовать уже открытое соединение
        response = await session.get(url=url, headers=headers)                                                          # отправляем запрос на страницу
        soup = BeautifulSoup(await response.text(), 'lxml')                                                             # создаем объект супа
        page_count = int(soup.find("ul", class_="pagination-custom").find_all("a")[-2].text)                            # код нахождение пагинации

        tasks = []                                                                                                      # пустой список задач

        for page in range(1, page_count + 1):                                                                           # цикл для прохождения страниц с колодами(задаем диапазон от кол-ва страниц)
            task = asyncio.create_task(get_page_data(session, page))                                                    # создаем задачу и задаем функцию с параметром сессии и страницы
            tasks.append(task)                                                                                          # пополняем список задач

        await asyncio.gather(*tasks)                                                                                    # собираем задачи по окончанию цикла


def main():
    asyncio.run(gather_data())                                                                                          # запускаем функцию с помощью метода run
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")                                                       # получаем текущее время

    with open(f'rareplayingcards_{cur_time}_async.json', "w", encoding="utf-8") as file:                                # сохраняем данные в json
        json.dump(cards_data, file, indent=4, ensure_ascii=False)

    with open(f'rareplayingcards_{cur_time}_async.csv', "w") as file:                                                   # сохраняем данные в csv
        writer = csv.writer(file)                                                                                       # создаем writer-а для записи в csv для заголовков столбцов

        writer.writerow(                                                                                                # создаем заголовки столбцов
             (
                 'Название колоды',
                 'Производитель',
                 'Цена'
             )
         )

    for card in cards_data:                                                                                             # проходим по списку словарей колод

        with open(f'rareplayingcards_{cur_time}_async.csv', "a", encoding="utf-8") as file:                             # сохраняем данные по каждой колоде
            writer = csv.writer(file)                                                                                   # создаем writer-а для записи в csv для данных о колодах

            writer.writerow(                                                                                            # выводим данные в столбцы
                (
                    card["name"],
                    card["seller"],
                    card["price"]
                )
            )

    finish_time = time.time() - start_time                                                                              # задаем время завершения скрипта
    print(f"Затраченное на работу время: {finish_time}")                                                                # выводим затраченное на скрипт время


if __name__ == "__main__":
    main()

