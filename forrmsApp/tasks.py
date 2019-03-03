from celery import shared_task,current_task
from celery_progress.backend import ProgressRecorder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from numpy import random
from scipy.fftpack import fft
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rankFullRevDF import rankFullrevsDF
from cacheScrapedAuthor import cacheScrapedAuthor
from gscholarScrapeTopics import gscholarScrapeTopics
from excludeCOIs import excludeCOIs
from keywordExpansion import keywordExpansion


@shared_task
def fft_random(n):
    """
    Brainless number crunching just to have a substantial task:
    """
    for i in range(n):
        x = random.normal(0, 0.1, 2000)
        y = fft(x)
        if(i%30 == 0):
            process_percent = int(100 * float(i) / float(n))
            current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})
    return random.random()

@shared_task()
def my_task(authors, topicsq, citationsType, citationsRangeMin, citationsRangeMax, venueq, currentAffsList, citationsWt, topRevWt, topicMatchWt, pubInVenueWt, recencyWt, linksList, linksListD, linksListA):
    current_task.update_state(state='PROGRESS', meta={'process_percent': 1})
    #Open Bowser in Headless Mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options = options)
    current_task.update_state(state='PROGRESS', meta={'process_percent': 10})

    #Cached File Name
    fName = (''.join(topicsq))
    if len(fName) > 100:
        fName = fName[:100] + '_'

    # keyword Expansion ....
    topicsq = keywordExpansion(topicsq)
    current_task.update_state(state='PROGRESS', meta={'process_percent': 20})

    names, urls = gscholarScrapeTopics(topicsq, driver)
    completeAuthorsDataframe = []
    revsDF = []
    counter = 20
    for name, url in zip(names, urls):
        authorDict = cacheScrapedAuthor(name, url, driver)
        authorDictKeys = list(authorDict.keys())
        for k in authorDictKeys:
            if type(authorDict[k]) != 'list':
                authorDict[k] = [authorDict[k]]
        firstAuthorsDataframe = pd.DataFrame.from_dict(authorDict, orient='index').transpose()
        completeAuthorsDataframe.append(firstAuthorsDataframe)
        counter += 1
        current_task.update_state(state='PROGRESS', meta={'process_percent': int(counter)})

    if(len(completeAuthorsDataframe) > 0):
        revsDF = pd.concat(completeAuthorsDataframe, sort = True)
        revsDF.reset_index(drop=True, inplace=True)    
        # used to remove duplicate reviwers when scraped from different topic pages....
        revsDF.sort_values('Name', ascending=True, inplace=True)
    indexToRemove = []
    for index in range(1, len(revsDF)):
        cntRev = revsDF.iloc[index]
        prevRev = revsDF.iloc[index-1]
        if cntRev['Name'] == prevRev['Name']:
            indexToRemove.append(index)
    
    revsDF.drop(revsDF.index[indexToRemove], inplace=True)

    current_task.update_state(state='PROGRESS', meta={'process_percent': 75})
        
    #Collect and Cache the candidate reviewers Info
    for author,link,cntAffiliation,linkD,linkA in zip(authors, linksList,currentAffsList, linksListD, linksListA):
        authorDict = cacheScrapedAuthor(author, link, driver, cntAffiliation, linkD, linkA)
    current_task.update_state(state='PROGRESS', meta={'process_percent': 95})

    for index, row in revsDF.iterrows():
        checkResult = excludeCOIs(row['Name'], authorDict['Name'], citationsRangeMin, citationsRangeMax, row['Link'], link, citationsType, driver)
        if not checkResult:
            revsDF.drop(index, inplace = True)
    
    rankedRevsDF = rankFullrevsDF(revsDF, venueq, topicsq, float(pubInVenueWt), float(topicMatchWt), float(topRevWt), float(citationsWt), float(recencyWt), driver)
    rankedRevsDF.to_pickle('/home/ubuntu/Integration/tmpCache/finalResults.pkl')
    driver.quit()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 100})
    return random.random()
