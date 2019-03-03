# -*- coding: utf-8 -*-
"""
This Function Scrape GoogleScholar Author Profiles for getting Their Info for each topic of the submitted queried topics.
input: topics list
output: full resulted dataframe of the dictonaries infos of scholars for each page and topics  

"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from cacheScrapedAuthor import cacheScrapedAuthor
def getURL(PrevNextURL):
    url=PrevNextURL
    url=url.replace("\\x3d","=")
    url=url.replace("\\x26","&")
    url=url.replace("&oe=ASCII","")
    url=url.replace("window.location='","https://scholar.google.com")
    url=url.replace("'","")
    return url


def gscholarScrapeTopics(topicsLst, driver):
    maxRevs = 35
    names = []
    urls = []
    for topic in topicsLst:
        driver.get("https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:" + topic)
        prevNext = []
        PrevNextURL = ''

        while True:
            authors = driver.find_elements_by_xpath('//*[@class="gsc_1usr gs_scl"]')
            for author in authors:
                try:
                    name = author.find_element_by_xpath('.//h3[@class="gsc_oai_name"]/a').get_attribute('innerHTML')
                    # Scrape Link here....... and pass it to cacheScrapedAuthor
                    link = author.find_element_by_xpath('.//h3[@class="gsc_oai_name"]/a').get_attribute('href')
                    names.append(name)
                    urls.append(link)
                except:
                    continue

            try:  
                prevNext = driver.find_element_by_xpath("//button[@type='button'][@aria-label='Next']").get_attribute('onclick')
                PrevNextURL = str(prevNext)
                PrevNextURL = getURL(PrevNextURL)
    
            except:
                pass

            if prevNext == None or len(urls) > maxRevs or len(prevNext) == 0:
                break

            driver.get(PrevNextURL)
        if (len(urls) > maxRevs):
            break
    return names, urls