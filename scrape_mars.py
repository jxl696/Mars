from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
import pandas as pd
from selenium import webdriver
import time
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_data = {}

    browser =init_browser()

# Nasa Mars News
    url= "https://mars.nasa.gov/news/"
    response.get(url)
    soup = bs(response.text, 'html.parser')
    latests = soup.find_all('div', class_="image_and_description_container")[0]
    news_p = latests.find('a').text
    news_title = latests.find('img', class_="img-lazy")["alt"]

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
#JPL Space Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html =browser.html
    jpl_soup = bs(html, "html.parser")
    results = jpl_soup.find_all('a', class_="button fancybox")
    image_link = results[0]["data-fancybox-href"]
    feature_image_url = url2 + image_link
    
    mars_data['featured_image_url'] = feature_image_url

#Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    twitter_soup = bs(response.text, 'html.parser')
    mars_weather = twitter_soup.find("div", class_ = "js-tweet-text-container").text.strip()
    
    mars_data["Mars_weather"] = mars_weather

#Mars Fact
    fact_url = "https://space-facts.com/mars/"
    tables = pd.read_html(fact_url)
    df = tables[0]
    df.columns = ["Description", "Values"]
    df.set_index("Description", inplace = True)
    html_table = df.to_html()
    mars_data["mars_table"] = html_table

#Mars Hemisphere
    hemisphere_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
                   'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                   'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                   'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
                  ]

    image_html = ""

    root_url = "https://astrogeology.usgs.gov"

    hemisphere_img_url = []

    for hemisphere_url in hemisphere_urls:
        with Browser('chrome', headless=False) as browser:
            url = hemisphere_url
            browser.visit(url)
            image_html = browser.html

        soup = bs(image_html, 'html.parser')
    
        title_results = soup.find('h2', class_ = 'title')
    
        for result in title_results:
            title = title_results.text
            print(title) 

        image_results = soup.find_all('img', class_='wide-image')
    
        for result in image_results:
            image_link = result['src']
            image_url = root_url + image_link
            print(image_url)
        
        img_dict = {
          'title': title,
          'image_url': image_url
         }
    
        hemisphere_img_url.append(img_dict)  

    mars_data["hemisphere_images"] =  hemisphere_img_url
    
    




