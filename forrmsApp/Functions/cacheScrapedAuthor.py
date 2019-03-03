# -*- coding: utf-8 -*-
'''
Collect and Store all the required information about specific author/reviewer
'''
try:
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
except ImportError:
     from urlparse import urlparse
     from urlparse import parse_qs 
import json
from os import listdir
from datetime import date
from datetime import datetime
from os.path import isfile, join
from queryDBLP import queryDBLP
from gscholarScrapeAuthorInfo2 import gscholarScrapeAuthorInfo2
from queryAcm import queryAcm
import codecs

def cacheScrapedAuthor(authorName, gscholarURL = "", driver = None, cntAffiliation = "", dblpURL = "", acmURL = ""):
    authorsDir="/home/ubuntu/Integration/AuthorsDir/Authors"
    authorFiles = [f for f in listdir(authorsDir) if isfile(join(authorsDir, f))]
   
    parsed = urlparse(gscholarURL)
    userLinkToken= parse_qs(parsed.query)['user'][0]
    timeInterval = 60
    authorCachedFlag =  0
    authorUpdatedFlag = 1
    
    if userLinkToken + ".json" in authorFiles:
            authorCachedFlag =  1 # for file exist. checking 0 means file exist 1 means file not exist

            with codecs.open(authorsDir + "/" + userLinkToken+ ".json", 'r', encoding='utf-8') as f:
                authorsDict = json.load(f)
            authorsDict['Name'] = authorsDict['Name'].encode('utf-8')

            lastMDate= authorsDict['last_Modified']
            todayDate = str(date.today())

            dateFormat = "%Y-%m-%d"
            lastMDate = datetime.strptime(lastMDate, dateFormat)
            todayDate = datetime.strptime(todayDate, dateFormat)
            
            
            if (todayDate-lastMDate).days > timeInterval:
                authorUpdatedFlag = 0 # for date checking.. Needs to be updated
                
    # the time passed 2 months  
    if authorUpdatedFlag == 0 or authorCachedFlag == 0:
         # Scrape data from Google scolar any way...
        authorsDict = gscholarScrapeAuthorInfo2(authorName, userLinkToken)

        affsHistAcm = queryAcm(authorName, acmURL, driver)
        affsHistAcm = list(set(affsHistAcm))

        if len(cntAffiliation)>0:
            affsHistAcm.append(cntAffiliation)

        authorsDict['AffiliationHistory'].extend(affsHistAcm)

        coAuthors, venues, recentPubs = queryDBLP(authorName)
        authorsDict['venues'] = venues
        authorsDict['co_Authors'] = coAuthors
        authorsDict['recentPubs'] = recentPubs
        todayDate = str(date.today())
        authorsDict['last_Modified'] = todayDate

        with codecs.open(authorsDir + "/" + userLinkToken + ".json", 'w', encoding='utf-8') as f:
            json.dump(authorsDict, f, ensure_ascii=False)
    return authorsDict
    
            