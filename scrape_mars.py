#Importing Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    
    # ### NASA Mars News

    # Loading Chromedriver
    browser = init_browser()
    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response = requests.get(mars_news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #print(soup.prettify())

    #getting the full version of HTML
    browser.visit(mars_news_url)
    html_nasa_news = browser.html
    soup = BeautifulSoup(html_nasa_news, 'html.parser')
    #print(soup)




    #getting all lists under slide
    content = soup.find_all('div', class_="content_title")
    sidebar = content[1]
    # getting the title and the paragraph
    p_results = soup.find('div', class_='list_text')
    para = p_results.find('div', class_='article_teaser_body')
    news_p = para.text
    print(news_p)
    header = sidebar.find('a')
    #extracting just the title
    #news_p = p.text
    news_title = header.text
    #printing the title and paragraph
    #print(f"news_title = {news_title}")
    #print(f"news_p = {news_p}")


    # ### JPL Mars Space Images - Featured Image

    # In[38]:


    #visit url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #click by partial stuff
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    #in order to get the largesize image, I had to click by partial href
    browser.click_link_by_partial_href('largesize')
    #saving the URL
    featured_image_url = browser.url
    #exiting out of view
    #browser.quit()


    #print(f"featured_image_url = {featured_image_url}")
        


    # ### Mars Facts
    # 
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # Use Pandas to convert the data to a HTML table string.
    # 

    #going to the URL
    mars_facts_url = 'https://space-facts.com/mars/'
    #reading the tables
    tables = pd.read_html(mars_facts_url)
    #print(len(tables))

    #print(tables[0])



    # I will only need the first table
    #making it into a DF
    mars_fact_df = pd.DataFrame(tables[0])
    #displaying mars facts
    #mars_fact_df

    #converting to HMTL
    table_html = mars_fact_df.to_html()
    #printing lines of HTML
    #print(table_html)


    # ### Mars Hemispheres
    # 
    # 
    #visit url
    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    #click by partial stuff
    hemisphere_image_urls = []
    browser.click_link_by_partial_text('Cerberus')
    browser.click_link_by_partial_text('Sample')
    Cer_url = browser.url
    cer_raw_title = browser.title
    cer_title = cer_raw_title.split("|")
    browser.visit(url_hem)
    browser.click_link_by_partial_text('Schiaparelli')
    browser.click_link_by_partial_text('Sample')
    sch_url = browser.url
    sch_raw_title = browser.title
    sch_title = sch_raw_title.split("|")
    #print(sch_url)
    #print(sch_title[0])
    browser.visit(url_hem)
    browser.click_link_by_partial_text('Syrtis')
    browser.click_link_by_partial_text('Sample')
    syr_url = browser.url
    syr_raw_title = browser.title
    syr_title = syr_raw_title.split("|")
    #print(syr_url)
    #print(syr_title[0])
    browser.visit(url_hem)
    browser.click_link_by_partial_text('Valles')
    browser.click_link_by_partial_text('Sample')
    val_url = browser.url
    val_raw_title = browser.title
    val_title = val_raw_title.split("|")
    #print(val_url)
    #print(val_title[0])


    hemisphere_image_urls = [{"title":cer_title[0],"image_url": Cer_url},
                            {"title":sch_title[0],"image_url":sch_url},
                            {"title": syr_title[0],"image_url":syr_url},
                            {"title": val_title[0],"image_url":val_url}]

    browser.quit()
    mars_data = [{
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "mars_facts": table_html,
        "hemispheres": hemisphere_image_urls
    }]
    
    return mars_data


results = scrape()

print(results)





