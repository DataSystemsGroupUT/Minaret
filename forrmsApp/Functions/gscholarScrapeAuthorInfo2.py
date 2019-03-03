# -*- coding: utf-8 -*-
"""
"""
from keywordExpansion import keywordExpansion
import scholarly
def gscholarScrapeAuthorInfo2(authorName = '', link = ''):
    search_query = scholarly.search_author(authorName.encode('utf8'))
    try:
        authorInfo = next(search_query).fill()
        while(authorInfo.id != link):
           authorInfo = next(search_query).fill()

        name = authorInfo.name
        image = 'https://scholar.google.com' + authorInfo.url_picture
        Affliation = authorInfo.affiliation
        email = authorInfo.email
        try:
            citedby = authorInfo.citedby
        except:
            citedby = 0
        topics = authorInfo.interests
        topicsList = []
        for topic in topics:
            expandedTopic = keywordExpansion(topic)
            topicsList.extend(expandedTopic)
        topicsList = list(set(topicsList))
        authorsDict = {'Name':name,'Image':image,'AffiliationHistory':[Affliation], 'Email':email,'Link' :link,'CitedBy':citedby,'Topics':topicsList}
    except:
        authorsDict = {'Name':authorName,'Image':'#','AffiliationHistory':['#'], 'Email':'#','Link' :link,'CitedBy':-1,'Topics':[]}

    return authorsDict 