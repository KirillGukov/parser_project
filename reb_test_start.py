import requests
from bs4 import BeautifulSoup

url = 'https://rareplayingcards.com/collections/limited-edition'

response = requests.get(url=url)
soup = BeautifulSoup(response.text, "lxml")

page_count = int(soup.find("ul", class_="pagination-custom").find_all("a")[-2].text)


for page in range(1, page_count + 1):

    response = requests.get(f'https://rareplayingcards.com/collections/limited-edition?page={page}').text
    soup = BeautifulSoup(response, 'lxml')

    for adr_part in soup.find_all('a', class_='lazy-image double__image'):
        card_adr = (adr_part.text.split())

        print(card_adr)

        card_page = requests.get(f'https://rareplayingcards.com/collections/limited-edition/products/{card_adr}',).text
        soup = BeautifulSoup(card_page, 'lxml')

        name = soup.find('h1', class_='h2').text.strip()
