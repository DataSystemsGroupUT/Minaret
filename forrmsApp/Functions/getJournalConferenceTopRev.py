# -*- coding: utf-8 -*-
"""
Get top reviewers in a specific venue
"""
import json
from os import listdir
from datetime import date
from datetime import datetime
from os.path import isfile, join
def getJournalConferenceTopRev(venue, driver):    
    joursConfsDir="/home/ubuntu/Integration/AuthorsDir/Journals"
    venueFiles = [f for f in listdir(joursConfsDir) if isfile(join(joursConfsDir, f))]
    
    timeInterval=60
    
    journalConfScraped=1
    journalConfUpdated=0
    
    if(venue+".json" in venueFiles):
        journalConfScraped=0
        journalConfUpdated=1
        
        with open(joursConfsDir+"/"+ venue+".json") as f:
            topRevDict = json.load(f)
            
        lastMDate= topRevDict['lastModified']
        todayDate = str(date.today())

        dateFormat = "%Y-%m-%d"
        lastMDate = datetime.strptime(lastMDate, dateFormat)
        todayDate = datetime.strptime(todayDate, dateFormat)
        
        
        if((todayDate-lastMDate).days>timeInterval):
            journalConfUpdated = 0 # for date checking..
            
    if journalConfUpdated == 0:
         # Scrape data from Google scolar any way...
        if journalConfScraped == 1: # file not existed!!
            Publons_SEARCH_URL ='https://publons.com/journal/'
            trials = 0
            topRevDict={}
            topRevDict['topReviewers'] = []
            while trials < 3:
                try:
                    driver.get(Publons_SEARCH_URL + str(venue))
                    toprevElement = driver.find_elements_by_xpath("//*[@class='row']/div/div/section/div/a")            
                    for rev in toprevElement:
                        revDict = {}
                        s=str(rev.text.encode('utf-8'))
                        revDict['rank'] = s[s.find("(")+1:s.find(")")]
                        revDict['name'] = s.split(') ')[-1]
                
                        if(len(revDict['name']) < 2):
                            continue
                        topRevDict['topReviewers'].append(revDict)
                    
            
                    journalTitle=driver.find_element_by_xpath('//*[@id="body"]/div[2]/div[4]/div/div[1]/div/section[1]/div/div/h1').text
                    topRevDict['journalName']=journalTitle
            
                    journalID=venue
                    topRevDict['journalID']=journalID
            
                    todayDate = str(date.today())       
                    topRevDict['lastModified'] = todayDate
                        
                    with open(joursConfsDir+"/"+venue+".json", 'w') as outfile:
                        json.dump(topRevDict, outfile)
  
                    return topRevDict

                except:
                    trials += 1                        
    return topRevDict