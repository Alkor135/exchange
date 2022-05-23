import requests
from bs4 import BeautifulSoup


url = 'https://www.forexfactory.com/calendar'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

print(soup)
