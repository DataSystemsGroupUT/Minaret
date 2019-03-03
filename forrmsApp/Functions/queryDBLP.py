# -*- coding: utf-8 -*-
'''  
# This Function Scrape DBLP Author Profile for getting Their Co_Authors
# input: authorname
# output: list of Co_Authors, Venues that author published before in them, Recent publications
'''
import requests 

def queryDBLP(authorName):
    authorOrig = authorName
    authorName = authorName.replace(" ", "_")
    URL = "http://dblp.org/search/publ/api?q=author%3A" + authorOrig + "%3A$&format=json"
    r = requests.get(url = URL)
    data = r.json()
    coAuths=[]
    joursConfs=[]
    recentPubs = []
    try:
        data = data['result']['hits']
        if int(data['@total']) > 0:
            for d in data['hit']:
                dInfo = d['info']
            
                if 'title' in dInfo:
                    title = dInfo['title']
                    recentPubs.append(title)
            
                if 'authors' in dInfo:
                    coauthors = dInfo['authors']['author']
                    if type(coauthors) == list:
                        if authorOrig in coauthors:
                            coauthors.remove(authorOrig)
                        coAuths.extend(coauthors)
            
                venue = ''
                if 'venue' in dInfo:
                    venue = dInfo['venue']
                    joursConfs.append(venue)    
    
        coAuths = list(set(coAuths))
        joursConfs = list(set(joursConfs))
    except:
        pass
    return coAuths, joursConfs, recentPubs