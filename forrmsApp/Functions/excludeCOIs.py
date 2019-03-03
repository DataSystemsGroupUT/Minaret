# -*- coding: utf-8 -*-
"""
Exclude Reviewers with Conflict of Interests
"""
from cacheScrapedAuthor import cacheScrapedAuthor
from filterCitations import filterCitations

def excludeCOIs(revName, authName, citationsRangeMin, citationsRangeMax, revGscholarLink = "", authorGscholarLink = "", citationsType = 'citations', driver = None):
    # get rid of COIs (Reviewer : not one of authors, no co-work or afilliations, not in a same country)        
    revDict = cacheScrapedAuthor(revName, 'https://scholar.google.com/citations?user=' + revGscholarLink + '&hl=en', driver)
    authDict = cacheScrapedAuthor(authName,authorGscholarLink, driver)
    
    if(authName == revName):
        return False
    
    authCoAuthors = authDict['co_Authors']
    
    for coAuthor in authCoAuthors:
        if(coAuthor == revName):
            return False
    
    authAffHist = authDict['AffiliationHistory']
    revAffHist = revDict['AffiliationHistory']
    
    for aff in authAffHist:
        if(aff in revAffHist):
            return False
    
    if(filterCitations(revName, revGscholarLink, int(citationsRangeMin), int(citationsRangeMax), citationsType) == False):
        return False
     
    return True