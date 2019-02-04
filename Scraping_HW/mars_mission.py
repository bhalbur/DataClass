import requests
from bs4 import BeautifulSoup as bs

url = 'https://mars.nasa.gov/news/'
response = requests.get(url, timeout=5).text

soup = bs(response, 'html.parser')

headers = soup.find_all('div', class_='content_title')
print(headers[0:3])