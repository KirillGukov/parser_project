import requests
from bs4 import BeautifulSoup

url = 'https://rareplayingcards.com/collections/limited-edition'

response = requests.get(url=url)
soup = BeautifulSoup(response.text, "lxml")

page_count = int(soup.find("ul", class_="pagination-custom").find_all("a")[-2].text)


for page in range(1, 2):

    response = requests.get(f'https://rareplayingcards.com/collections/limited-edition?page={page}').text
    soup = BeautifulSoup(response, 'lxml')

    all_cards_hrefs = soup.find_all(class_='lazy-image double__image')
    for card_adr in all_cards_hrefs:
        card_href = card_adr.get('href')
        print(card_href)
