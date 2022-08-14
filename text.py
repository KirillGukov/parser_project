import requests
from bs4 import BeautifulSoup

start_page = requests.get('https://rareplayingcards.com/collections/limited-edition?page=1').text
soup = BeautifulSoup(start_page, 'lxml')

common_page = soup.find('div', class_='figcaption under text-center')

name = common_page.find('p', class_='h5--accent strong name_wrapper').text.replace("\n", "")
price = common_page.find('span', class_='money').text

print(name)
print(price)
