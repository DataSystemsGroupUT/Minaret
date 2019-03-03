# -*- coding: utf-8 -*-
"""
Ranking List of Candidate Reviewers according to specified metrics
"""
from checkIfRevPublishedIn import checkIfRevPublishedIn
from checkIfTopRanked import checkIfTopRanked
import pandas as pd

def rankFullrevsDF(revsDF, venue, paperTopics, pubInVenueWt, topicMatchWt, topRevWt, citationsWt, recencyWt, driver):    
    paperTopicsLst = paperTopics
    revsDF['Score'] = 0
    revsDF['recency'] = 0
    revsDF['keyWordsMatched'] = 0
    revsDF['isTopReviewerInVenue'] = 0
    revsDF['publishedInVenue'] = 0

    for index, row in revsDF.iterrows():
        fois = row['Topics']
        fois = [i.lower() for i in fois]
        pubs = row['recentPubs']
        pubs = [i.lower() for i in pubs]

        scoreMatched = 0
        recencyFlag = 0
        for topicKey in paperTopicsLst:
            topicKey = topicKey.replace('_', ' ').lower()
            if topicKey in fois:
                scoreMatched += 1
            for pub in pubs:
                for k in topicKey:
                    if topicKey in pub.lower():
                        recencyFlag = 1
                        break
                if recencyFlag == 1:
                    break

            if recencyFlag == 1:
                pass

        topReviewerRank = checkIfTopRanked(row['Name'], venue, driver)
        revPubInVenueCount = checkIfRevPublishedIn(venue, row['Name'],row['Link'], driver)

        revsDF.loc[index,'keyWordsMatched'] = scoreMatched
        revsDF.loc[index,'isTopReviewerInVenue'] = topReviewerRank
        revsDF.loc[index,'publishedInVenue'] = revPubInVenueCount
        revsDF.loc[index, 'recency'] = recencyFlag

    revsDF['keyWordsMatched'] = revsDF['keyWordsMatched'].apply(pd.to_numeric, downcast='float', errors='coerce')
    revsDF['publishedInVenue'] = revsDF['publishedInVenue'].apply(pd.to_numeric, downcast='float', errors='coerce')
    revsDF['CitedBy'] = revsDF['CitedBy'].apply(pd.to_numeric, downcast='float', errors='coerce')

    maxTopicMatch = max(1, revsDF['keyWordsMatched'].max())
    maxCitations = max(1.0, revsDF['CitedBy'].max())
    maxPubInVenue = max(1, revsDF['publishedInVenue'].max())

    topicMatchWtN = topicMatchWt / (topicMatchWt + pubInVenueWt + topRevWt + citationsWt + recencyWt)
    pubInVenueWtN = pubInVenueWt / (topicMatchWt + pubInVenueWt + topRevWt + citationsWt + recencyWt)
    topRevWtN = topRevWt / (topicMatchWt + pubInVenueWt + topRevWt + citationsWt + recencyWt)
    citationsWtN = citationsWt / (topicMatchWt + pubInVenueWt + topRevWt + citationsWt + recencyWt)
    recencyWtN = recencyWt / (topicMatchWt + pubInVenueWt + topRevWt + citationsWt + recencyWt)

    maxScore = 0
    for index, row in revsDF.iterrows():
        cntScore = 100 * (float(row['keyWordsMatched'])/maxTopicMatch * topicMatchWtN + float(row['publishedInVenue']) * pubInVenueWtN / maxPubInVenue + float(row['isTopReviewerInVenue']) * topRevWtN + float(row['CitedBy']) / maxCitations * citationsWtN + float(row['recency']) * recencyWtN)
        revsDF.set_value(index,'Score', cntScore)
        maxScore = max(maxScore, int(cntScore))

    for index, row in revsDF.iterrows():
        score = float(row['Score']) / maxScore * 100
        revsDF.set_value(index, 'Score', score)

    revsDF['Rank'] = revsDF.Score.rank(method='dense', ascending =False).astype(int)
    revsDF.sort_values('Rank', ascending=True, inplace=True)

    return revsDF
