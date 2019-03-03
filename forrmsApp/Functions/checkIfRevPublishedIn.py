# -*- coding: utf-8 -*-
"""
Check if candidate reviewer has published in the venue before or not
"""
from cacheScrapedAuthor import cacheScrapedAuthor
from getJournalConferenceTopRev import getJournalConferenceTopRev
def checkIfRevPublishedIn(journal = '', reviewer = "",link = "", driver = None):
    authorDict = cacheScrapedAuthor(authorName = reviewer, gscholarURL = 'https://scholar.google.com/citations?user=' + link + '&hl=en', driver = driver)
    authorPublishedVenues = authorDict['venues']
    count = 0
    venueDict = getJournalConferenceTopRev(journal, driver)
    journal = venueDict['journalName']
    for jourConf in authorPublishedVenues:
        if type(jourConf) == list:
            jourConf = jourConf[0]
        if type(journal) == list:
            journal = journal[0]
        if (jourConf.lower() in journal.lower()):
            count += 1
    
    return count        
