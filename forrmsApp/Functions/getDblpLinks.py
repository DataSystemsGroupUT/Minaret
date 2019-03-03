# -*- coding: utf-8 -*-
import requests 
"""
Search for Candidate Authors with the Same Entered Name in DBLP
"""
def getDblpLinks(authorName):
    
    URL = "http://dblp.org/search/author/api?q=" + authorName.replace(" ", "+") + "&format=json"
    r = requests.get(url = URL)
    data = r.json()
    data = data['result']['hits']['hit']
    dblpNames = []
    dblpUrls = []
    for person in data:
        if len(dblpNames) < 8:
            dblpNames.append(person['info']['author'])
            dblpUrls.append(person['info']['url'])
        else:
            break
    return dblpNames, dblpUrls
