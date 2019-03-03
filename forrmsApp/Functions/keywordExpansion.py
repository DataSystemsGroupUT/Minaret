# -*- coding: utf-8 -*-
'''
Expand Keyword to other equivilant words according to CS Ontology
'''
import csv
def keywordExpansion(topics):
    topicsLst = topics.lower().split(",")
    
    ontologyName = "/home/ubuntu/Integration/csOntology.csv"

    topicDict = {}
    with open(ontologyName) as f:
        reader = csv.reader(f)
        for row in reader:
            topicDict[ row[0] ] = [row[0]]
            for i in range(1, len(row)):
                word = row[i]
                topicDict[row[0]].append(word)
                    
    topicsOutput = []
    for topic in topicsLst:
        topicsOutput.append(topic)
        if topic in topicDict:
            topicsOutput.extend(topicDict[topic])

    topicsOutput = list(set(topicsOutput))
    return topicsOutput