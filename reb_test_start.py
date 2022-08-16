import requests
from bs4 import BeautifulSoup

start_page = requests.get('https://rareplayingcards.com/collections/limited-edition?page=1').text
soup = BeautifulSoup(start_page, 'lxml')

for name in soup.find_all('p', class_='h5--accent strong name_wrapper'):
    print(name.text.strip())
for price in soup.find_all('span', class_='price'):
    print(price.text.strip())