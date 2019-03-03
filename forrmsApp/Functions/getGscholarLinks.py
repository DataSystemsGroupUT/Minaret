# -*- coding: utf-8 -*-
"""
Search for Candidate Authors with the Same Entered Name in GScholar
"""
import scholarly

def getGscholarLinks(authorName, driver = None):
    pageNames= []
    pageImages=[]
    pageLinks= []
    pageAffs=[]
    try:
        searchAuthors = scholarly.search_author(authorName)
        while len(pageNames) < 5:
            try:
                cntAuthor = next(searchAuthors)
            except:
                break
            pageNames.append(cntAuthor.name)
            pageLinks.append('https://scholar.google.com/citations?user=' + cntAuthor.id + '&hl=en')
            pageImages.append('https://scholar.google.com' + cntAuthor.url_picture)
            
            if type(cntAuthor.affiliation) == list:
                pageAffs.append(cntAuthor.affiliation[0])
            else:
                pageAffs.append(cntAuthor.affiliation)
    except:
        driver.get("https://scholar.google.com.eg/citations?hl=en&view_op=search_authors&mauthors="+authorName)
        authors=driver.find_elements_by_xpath('//*[@class="gsc_1usr gs_scl"]')
        for author in authors:
            link= author.find_element_by_xpath('.//h3[@class="gsc_oai_name"]/a').get_attribute('href')
            name= author.find_element_by_xpath('.//h3[@class="gsc_oai_name"]/a').get_attribute('textContent')
            image=author.find_element_by_xpath('//*[@id="gsc_sa_ccl"]/div/span/img').get_attribute('src')
            affliation=author.find_element_by_xpath('.//*[@class="gsc_oai_aff"]').get_attribute('innerHTML')
            pageLinks.append(link)
            pageNames.append(name)
            pageImages.append(image)
            pageAffs.append(affliation)
        
    return pageNames, pageLinks, pageImages, pageAffs