#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time

# Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()

    #url of the page to be scraped
    url1 = 'https://mars.nasa.gov/news/'

    #get splinter to visit the url
    browser.visit(url1)

    #slow the process down
    time.sleep(1)

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

    #url of the page to be scraped
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #get splinter to visit the url
    browser.visit(url2)

    #create a soup object and parse it
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #navigate to the right page using splinter
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    #get the image url
    img_url = soup.find('article', class_='carousel_item')['style'].replace('background-image: url(','').replace(');','')[1:-1]
    img_url_full = 'https://www.jpl.nasa.gov' + img_url
    #quit the running browser

    #url of the page to be scraped
    url3 = 'https://space-facts.com/mars/'

    #perform the scrape
    table = pd.read_html(url3)

    #creat a dataframe from the scrape
    df = table[0]

    #get the HTML table string
    df.columns = ['Description', 'Mars']
    df = df.set_index('Description')
    html_table = df.to_html()

    #url of the page to be scraped
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #get splinter to visit the url
    browser.visit(url4)

    #get the legnth of the list for the for loop
    links = browser.find_by_css('a.product-item h3')

    #define the empty list
    hemisphere_image_urls = []

    #for loopin it for the title and url
    for x in range(len(links)):
        #empty dict
        mars = {}

        main_url = 'https://astrogeology.usgs.gov'
        
        #click into the specific hemisphere
        browser.find_by_css('a.product-item h3')[x].click()
        
        #create the soup object
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        #store the title in the dictionary
        mars['title'] = soup.find('h2', class_ = 'title').text
        
        #open for the full image
        browser.links.find_by_partial_text('Open').click()
        
        #store the image url in the dictionary 
        mars['img_url'] = main_url + str(soup.find('img', class_='wide-image')['src'])
        
        #append append append!
        hemisphere_image_urls.append(mars)

        #go back to the inital page
        browser.visit(url4)
        
    browser.quit()

    #create a dictionary with all of the information
    mars_dict = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img': img_url_full,
        'table': html_table,
        'hemispheres' : hemisphere_image_urls
    }

    return mars_dict
