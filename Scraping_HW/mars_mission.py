from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser


def news():
	url = 'https://mars.nasa.gov/news/'
	response = requests.get(url, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	header = soup.find('div', class_='content_title')
	print(header.text)
	body = soup.find('div', class_='rollover_description_inner')
	print(body.text)
	news_dict = {}
	news_dict['article_title'] = header.text.strip()
	news_dict['article_content'] = body.text.strip()
	print(news_dict)

def image():
	try:
		executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
		browser = Browser('chrome', **executable_path, headless=False)
		featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		browser.visit(featured_url)
		browser.click_link_by_partial_text('FULL IMAGE')
		featured_html = browser.html
		featured_soup = BeautifulSoup(featured_html, 'html.parser')
		url_suffix = featured_soup.find('img', class_='fancybox-image').attrs['src']
		featured_img_url = browser.url + url_suffix
		print(f'Featured img url: {featured_img_url}')
		featured_dict = {}
		featured_dict['title'] = 'Featured_Image'
		featured_dict['img_url'] = featured_img_url
		print(featured_dict)
	except Exception as e: 
		print(f'Error finding Featured Image: {e}')

def weather():
	twitter_url='https://twitter.com/marswxreport?lang=en'
	twit_resp = requests.get(twitter_url, timeout=5)
	twitter_soup = BeautifulSoup(twit_resp.text, 'html.parser')
	tweets = twitter_soup.find_all('p', class_='TweetTextSize')
	for tweet in tweets:
	    if tweet.text[:3] == 'Sol':
	        print(tweet.text)
	        weather_dict = {}
        	weather_dict['weather'] = tweet.text
	        break
	    else: next



def facts():
	fact_url = 'https://space-facts.com/mars/'
	fact_resp = requests.get(fact_url, timeout=5)
	fact_soup = BeautifulSoup(fact_resp.text, 'html.parser')
	facts = fact_soup.find_all('tr')
	fact_list = []
	for fact in facts:
	    fact_dict = {}
	    description, value = fact.text.strip().split(':')
	    fact_dict[description] = value
	    fact_list.append(fact_dict)
	print(fact_list)


def hemi():
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)
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
	    hemi_dict['title'] = hemi_title
	    hemi_dict['img_url'] = hemi_img
	    hemi_list.append(hemi_dict)
	    browser.back()
	print(hemi_list)

def store():
	return('this line in progress')
	#store the dicts


news()
image()
weather()
facts()
hemi()
store()