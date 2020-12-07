# # Mission to Mars

#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# # Step 1 - Scraping

# ## NASA Mars News
# - setup splinter and open the browser
# - get the first title and paragraph

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#url of the page to be scraped
url = 'https://mars.nasa.gov/news/'

#get splinter to visit the url
browser.visit(url)

#create a soup object and parse it
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#get the first title
titles = soup.find_all('div', class_='content_title', limit = 2)
news_title = titles[1].text

#get the first paragraph
pargs = soup.find_all('div', class_='article_teaser_body', limit = 1)
news_p = pargs[0].text

#quit the running browser
browser.quit()


# ## JPL Mars Space Images - Featured Image
# - opening the browser
# - getting the featured image

#opening the browser
browser = Browser('chrome', **executable_path, headless=False)

#url of the page to be scraped
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

#get splinter to visit the url
browser.visit(url)

#create a soup object and parse it
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#navigate to the right page using splinter
browser.links.find_by_partial_text('FULL IMAGE').click()
browser.links.find_by_partial_text('more info').click()

#get the image url
img_url = soup.find('article', class_='carousel_item')['style'].replace('background-image: url(','').replace(');','')[1:-1]

#quit the running browser
browser.quit()


# ## Mars Facts
# - scrape using read_html
# - create a data frame
# - convert to html table string

#url of the page to be scraped
url = 'https://space-facts.com/mars/'

#perform the scrape
table = pd.read_html(url)

#creat a dataframe from the scrape
df = table[0]
df.head(5)

#get the HTML table string
html_table = df.to_html()

# ## Mars Hemispheres

#opening the browser
browser = Browser('chrome', **executable_path, headless=False)

#url of the page to be scraped
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#get splinter to visit the url
browser.visit(url)

links = browser.find_by_css('a.product-item h3')

hemisphere_image_urls = []

for x in range(len(links)):
    mars = {}
    
    browser.find_by_css('a.product-item h3')[x].click()
    
    soup = BeautifulSoup(browser.html, 'html.parser')
    
    mars['title'] = soup.find('h2', class_ = 'title').text
    
    browser.links.find_by_partial_text('Open').click()
    
    mars['img_url'] = soup.find('img', class_='wide-image')['src']
    
    hemisphere_image_urls.append(mars)
    
    browser.visit(url)
    
browser.quit()