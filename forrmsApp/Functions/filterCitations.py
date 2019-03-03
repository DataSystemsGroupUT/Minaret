# -*- coding: utf-8 -*-
"""
Exclude Reviewers that are not within the defined citations range / H-Index range
"""
from cacheScrapedAuthor import cacheScrapedAuthor

def filterCitations(authorName,authorLink,mini=20,maxi=1000, citationsType = 'citations'):
    
    authorDict=cacheScrapedAuthor(authorName, 'https://scholar.google.com/citations?user=' + authorLink + '&hl=en')
    if citationsType == 'citations':
        authorCitations=int(authorDict['CitedBy'])
    else:
        authorCitations = int(authorDict['hindex'])
    
    return authorCitations in range(mini, maxi)