# -*- coding: utf-8 -*-
'''
Check if the candidate reviewer is one of Top reviewers of a venue
'''
from getJournalConferenceTopRev import getJournalConferenceTopRev

def checkIfTopRanked(reviewer, venue, driver):

    topRevDict = getJournalConferenceTopRev(venue, driver)
    
    tCount=0
    for topRev in topRevDict['topReviewers']:
        if reviewer.lower() == topRev['name'].lower():
            tCount = topRev.get('rank')
        
    return tCount 