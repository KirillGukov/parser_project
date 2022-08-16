import requests
from bs4 import BeautifulSoup
import re

main_page = 'https://rareplayingcards.com/collections/limited-edition'

headers = {
    'Accept': "	*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

page = 1
for i in range(8):
    start_page = requests.get(f'https://rareplayingcards.com/collections/limited-edition?page={page}').text
    soup = BeautifulSoup(start_page, 'lxml')

    for name in soup.find_all('p', class_='h5--accent strong name_wrapper'):
        print(name.text.strip())
    for price in soup.find_all('span', class_='price'):
        print(price.text.strip())
    page += 1