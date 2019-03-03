# -*- coding: utf-8 -*-
"""
# This Function Scrape ACM Author Profile for getting Their AffsHist.
# input: authorname
# output: list of affsHist
"""
def queryAcm(authorName, acmSearchURL = '', driverAcm = None):
    if len(acmSearchURL) == 0:
        acmSearchURL = 'https://dl.acm.org/results.cfm?within=owners.owner%3DGUIDE&srt=_score&query=persons.authors.personName:' + authorName
    affHist=[]
    try:
        driverAcm.get(acmSearchURL)
        linkAcmPAuthors= driverAcm.find_element_by_link_text(authorName)
        linkAcmPAuthors.click()
        affHistElems=driverAcm.find_elements_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div/a")
        
        for aff in affHistElems:
            affHist.append(aff.text)
    except:
        pass
    
    return affHist    
