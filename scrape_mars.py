from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find_all("div", class_ = "content_title")
    title_text = title[1].get_text()
    paragraph = soup.find_all("div", class_ = "article_teaser_body")
    paragraph_text = paragraph[0].get_text()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    image = browser.find_by_id("full_image")
    image.click()
    info = browser.find_link_by_partial_text("more info")
    info.click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.select_one("figure.lede a img")
    src = image.get('src')
    url = 'https://www.jpl.nasa.gov'
    src = url + src
    mars_scrape = pd.read_html("https://space-facts.com/mars/")
    mars_table = mars_scrape[0]
    mars_html = mars_table.to_html()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links = browser.find_by_css("a.product-item h3") 
    j= 0
    images = []
    for i in links:
        browser.find_by_css("a.product-item h3")[j].click()
        link = browser.find_link_by_text("Sample").first["href"]
        images.append(link)
        j = j+1
        browser.back()
    print(src)

    # Store data in a dictionary
    mars_data = {
        "title": title_text,
        "paragraph": paragraph_text,
        "image": src,
        "table": mars_html,
        "images": images
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
