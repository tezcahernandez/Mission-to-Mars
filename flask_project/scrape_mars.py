from bs4 import BeautifulSoup
import requests
import pymongo
import re
from splinter import Browser
import pandas as pd
import time

def main():
    _nasaMarsNews = nasaMarsNews()
    _marsSpacemages = marsSpacemages()
    _marsWeather = marsWeather()
    _marsFacts = marsFacts()
    _marsHemispheres = marsHemispheres()
    return {**_nasaMarsNews, **_nasaMarsNews, **_marsWeather, **_marsFacts, **_marsHemispheres, **_marsSpacemages}

def initBrowser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def nasaMarsNews():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_title = soup.select('div.content_title > a')[0].text.strip()
    news_p = soup.select('.image_and_description_container .rollover_description_inner')[0].text.strip()

    return {
        'news_title': news_title,
        'news_p': news_p
    }
    
def marsSpacemages():
    browser = initBrowser()
    marsNasaBaseUrl = 'https://www.jpl.nasa.gov/'
    marsImagesPath ='spaceimages/?search=&category=Mars'
    browser.visit(marsNasaBaseUrl + marsImagesPath)
    
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    backgroundImagePath = soup.select('.carousel_item')[0]['style'].split("'")[1]

    featured_image_url = marsNasaBaseUrl + backgroundImagePath

    return {
        'featured_image_url': featured_image_url
    }

def marsWeather():
    marsWeatherUrl = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(marsWeatherUrl)
    soup = BeautifulSoup(response.text, 'lxml')

    mars_weather  = soup.select('.js-tweet-text-container p')[0].text.strip().replace('\n', ' ')

    return {
        'mars_weather': mars_weather
        }

def marsFacts():
    marsFactsBaseUrl = 'https://space-facts.com/mars/'


    marsFactsBaseUrl = 'https://space-facts.com/mars/'
    marsFactsTables = pd.read_html(marsFactsBaseUrl)
    marsFactDf = marsFactsTables[0]
    marsFactDf.rename(columns={0:'property', 1:'value'}, inplace=True)
    marsFactsTableHtml = marsFactDf.to_html()
    marsFactsTableHtml = marsFactsTableHtml.replace('\n', '')
    return{
        'marsFactsHtml': marsFactsTableHtml
    }

def marsHemispheres():
    browser = initBrowser()
    
    astrogeologyMarsBaseUrl = 'https://astrogeology.usgs.gov'
    astrogeologyMarsSearchUrl = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeologyMarsBaseUrl + astrogeologyMarsSearchUrl)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    hemisphere_image_urls = []

    itemsToVisit = soup.select('.item div.description a.itemLink')
    for itemToVisit in itemsToVisit:
        browser.visit(astrogeologyMarsBaseUrl + itemToVisit['href'])
        _html = browser.html
        _soup = BeautifulSoup(_html, 'lxml')
        hemisphereName = _soup.select('div.content h2.title')
        downloadLinks = _soup.select('div.downloads ul li a')
        #     print(downloadLinks[1]['href'])
        #     print(hemisphereName[0].text)
        hemisphere_image_urls.append({
            'title': hemisphereName[0].text,
            'image_url': downloadLinks[0]['href']
        })

    return {
        'hemisphere_image_urls':hemisphere_image_urls
        }