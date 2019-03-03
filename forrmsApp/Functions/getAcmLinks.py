# -*- coding: utf-8 -*-
"""
Get candidate ACM profiles for an author
"""
def getAcmLinks(authorName, driver):
    sQuery = '%252B'
    for i in range(0, len(authorName)):
        if i == 0 or authorName[i - 1] == ' ':
            authorName[i].upper()

        if authorName[i] == ' ':
            sQuery += '%20%252B'
        else:
            sQuery += authorName[i]
            
    acmLinks = []
    acmNames = []    
    try:
        driver.get('https://dl.acm.org/results.cfm?query=persons.authors.personName:(' + sQuery + ')&within=owners.owner=GUIDE&filtered=&dte=&bfr=')
        
        links = driver.find_elements_by_partial_link_text(authorName)
        for link in links:
            url = link.get_attribute("href")
            if url in acmLinks:
                continue
            if len(acmLinks) > 5:
                break
            acmLinks.append(url)
            acmNames.append(link.text)
    
    except RuntimeError:
        pass
    
    return acmNames, acmLinks
