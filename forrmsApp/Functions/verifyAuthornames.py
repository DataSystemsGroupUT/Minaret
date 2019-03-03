# -*- coding: utf-8 -*-
"""
Verify the entered authors profiles and allow user to choose the correct profiles
"""
from getGscholarLinks import getGscholarLinks
from getDblpLinks import getDblpLinks
from getAcmLinks import getAcmLinks
from interruptingcow import timeout
import signal
def signal_handler(signum, frame):
    raise Exception("Timed out!")
    
def verifyAuthornames(authors, driver):
    authorsLst = set(authors.split(',') )
        
    eachAuthorLst = []
    eachAuthorLstDblp = []
    eachAuthorLstAcm = []
    for author in authorsLst:
        pageNames, pageLinks, pageImages, pageAffs = getGscholarLinks(author, driver)
        
        dblpNames, dblpLinks = getDblpLinks(author)
        
        try:
            while True:
                acmNames, acmLinks = getAcmLinks(author, driver)
                break
        except Exception as msg:
            acmNames = []
            acmLinks = []
            print(msg)

        acmNames.append('Not Found')
        acmLinks.append('#')
        dblpNames.append('Not Found')
        dblpLinks.append('#')

        #Custom URLs
        acmNames.append('Custom')
        acmLinks.append('#$')
        dblpNames.append('Custom')
        dblpLinks.append('#$')
        pageNames.append('Custom')
        pageLinks.append('#$')
	pageImages.append('#')
	pageAffs.append(' ')
        
        eachAuthorLst.append(zip(pageNames, pageLinks, pageImages,pageAffs))
        eachAuthorLstDblp.append(zip(dblpNames, dblpLinks))
        eachAuthorLstAcm.append(zip(acmNames, acmLinks))

    return eachAuthorLst, eachAuthorLstDblp, eachAuthorLstAcm