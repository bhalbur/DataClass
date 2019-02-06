from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_mission
db.variables.drop()


def news():
	news_url = 'https://mars.nasa.gov/news/'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=True)
	browser.visit(news_url)
	news_soup = BeautifulSoup(browser.html, 'html.parser')
	print(len(browser.html))
	header = news_soup.find('div', class_='content_title')
	print(header.text)
	body = news_soup.find('div', class_='rollover_description_inner')
	print(body.text)
	news_dict = {}
	news_dict['type'] = 'news'
	news_dict['title'] = header.text.strip()
	news_dict['content'] = body.text.strip()
	print(news_dict)
	db.variables.insert_one(news_dict)

def image():
	try:
		executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
		browser = Browser('chrome', **executable_path, headless=True)
		featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		browser.visit(featured_url)
		browser.click_link_by_partial_text('FULL IMAGE')
		featured_html = browser.html
		featured_soup = BeautifulSoup(featured_html, 'html.parser')
		url_suffix = featured_soup.find('img', class_='fancybox-image').attrs['src']
		featured_img_url = 'https://www.jpl.nasa.gov' + url_suffix
		print(f'Featured img url: {featured_img_url}')
		featured_dict = {}
		featured_dict['type'] = 'featured_image'
		featured_dict['content'] = featured_img_url
		print(featured_dict)
		db.variables.insert_one(featured_dict)
	except Exception as e: 
		print(f'Error finding Featured Image: {e}')

def weather():
	twitter_url='https://twitter.com/marswxreport?lang=en'
	twit_resp = requests.get(twitter_url, timeout=15)
	twitter_soup = BeautifulSoup(twit_resp.text, 'html.parser')
	tweets = twitter_soup.find_all('p', class_='TweetTextSize')
	for tweet in tweets:
	    if tweet.text[:3] == 'Sol':
	        print(tweet.text)
	        weather_dict = {}
	        weather_dict['type'] = 'weather'
        	weather_dict['content'] = tweet.text
	        break
	    else: next
	db.variables.insert_one(weather_dict)


def facts():
	fact_url = 'https://space-facts.com/mars/'
	fact_resp = requests.get(fact_url, timeout=15)
	fact_soup = BeautifulSoup(fact_resp.text, 'html.parser')
	facts = fact_soup.find_all('tr')
	fact_dict = {}
	fact_subdict = {}
	fact_dict['type'] = 'facts'
	for fact in facts:
	    description, value = fact.text.strip().split(':')
	    fact_subdict[description] = value
	    fact_dict['content'] = fact_subdict
	print(fact_dict)
	db.variables.insert_one(fact_dict)


def hemi():
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=True)
	hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemi_url)
	
	hemispheres = ['Cerberus','Schiaparelli','Syrtis','Valles']
	hemi_list = []
	
	for hemi in hemispheres:
	    hemi_dict = {}
	    browser.click_link_by_partial_text(hemi)
	    hemi_soup = BeautifulSoup(browser.html, 'html.parser')
	    hemi_title = hemi_soup.find('h2', class_='title')
	    hemi_title = hemi_title.text.split(' Enhanced')[0]
	    print(hemi_title)
	    dl_tag = hemi_soup.find('div', class_='downloads')
	    hemi_img = dl_tag.find('a').attrs['href']
	    print(hemi_img)
	    hemi_dict['type'] = 'hemisphere'
	    hemi_dict['title'] = hemi_title
	    hemi_dict['content'] = hemi_img
	    hemi_list.append(hemi_dict)
	    browser.back()
	print(hemi_list)
	db.variables.insert_many(hemi_list)



news()
image()
weather()
facts()
hemi()