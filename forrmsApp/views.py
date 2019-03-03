# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import shared_task
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import os
import glob
import sys
import time
import json
import pandas as pd
from django.http import HttpResponse
sys.path.insert(0, r'/home/ubuntu/Integration/forrmsApp/Functions')

from .tasks import fft_random, my_task
from .forms import UserForm
from celery.result import AsyncResult
from verifyAuthornames import verifyAuthornames

def showResults(request):
    rankedRevsDF = pd.read_pickle('/home/ubuntu/Integration/tmpCache/finalResults.pkl')
    revNames = rankedRevsDF.Name
    revImages = rankedRevsDF.Image
    revLinks = rankedRevsDF.Link
    revEmails = rankedRevsDF.Email
    revTopics = rankedRevsDF.Topics
    revCitations = rankedRevsDF.CitedBy
    revAffs = rankedRevsDF.AffiliationHistory
    revScores = rankedRevsDF.Score
    revsPublishedInVenue = rankedRevsDF.publishedInVenue
    revsisTopReviewerInVenue = rankedRevsDF.isTopReviewerInVenue
    revskeyWordsMatched = rankedRevsDF.keyWordsMatched
    revsRecency = rankedRevsDF.recency
    lstPosts = list(range(len(revImages)))
    
    paginator = Paginator(lstPosts, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    mylist = zip(revImages,revNames, revLinks, revEmails, revTopics,revCitations,revAffs,revScores, revsPublishedInVenue, revsisTopReviewerInVenue, revskeyWordsMatched, lstPosts, revsRecency)

    return render(request, 'Results.html',
            {'mylist':mylist,
            'authornames':request.session['authornames'],
            'topicsq':request.session['topicsq'],
            'citationsRangeMin':request.session['minCitations'],
            'citationsRangeMax': request.session['maxCitations'],
            'venueq':request.session['venueq'],
            'posts': posts,
            })


def Results(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request, "resultsProgress.html", context)
    else:
        # Authors Names
        authornames = request.session['authornames']
        authors = authornames.split(',')
        # Topics Keywords
        topicsq = ','.join(request.session['topicsq'])
        # Citations Range Filter
        citationsType = request.session['citationsType']
        citationsRangeMin = request.session['minCitations']
        citationsRangeMax = request.session['maxCitations']
        # Venue that manuscript was submitted to
        venueq=request.session['venueq']
        # Current affiliations of authors
        affsq=request.session['affs']
        currentAffsList=affsq.split(',')
        # Weights of different filters
        citationsWt = request.session['citationsWt']
        topRevWt = request.session['topRevWt']
        topicMatchWt = request.session['topicMatchWt']
        pubInVenueWt = request.session['pubInVenueWt']
        recencyWt = request.session['recencyWt']

        # Get Google AuthorLinks from URL
        numberLinks = 0
        linksList = []
        while True:
            linkName = 'link' + str(numberLinks+1)
            if linkName in request.GET :
                res = request.GET[linkName]
                linkURL = res.split('*')[1]
                if linkURL != '#$':
                    linksList.append(linkURL)
                else:
                    linksList.append(request.GET['linkCustom' + str(numberLinks + 1)])
                numberLinks += 1
            else:
                break
    
        # Get DBLP AuthorLinks from URL
        numberLinks = 0
        linksListD = []
        while True:
            linkName = 'linkD' + str(numberLinks + 1)
            if linkName in request.GET:
                res = request.GET[linkName]
                linkURL = res.split('*')[1]
                if linkURL != '#$':
                    linksListD.append(linkURL)
                else:
                    linksListD.append(request.GET['linkDCustom' + str(numberLinks + 1)])
  
                numberLinks += 1
            else:
                break
    
       # Get ACM AuthorLinks from URL
        numberLinks = 0
        linksListA = []
        while True:
            linkName = 'linkA' + str(numberLinks + 1)
            if linkName in request.GET:
                res = request.GET[linkName]
                linkURL = res.split('*')[1]
                if linkURL != '#$':
                    linksListA.append(linkURL)
                else:
                    linksListA.append(request.GET['linkACustom' + str(numberLinks + 1)])
                numberLinks += 1
            else:
                break

        job = my_task.delay(authors, topicsq, citationsType, citationsRangeMin, citationsRangeMax, venueq, currentAffsList, citationsWt, topRevWt, topicMatchWt, pubInVenueWt, recencyWt, linksList, linksListD, linksListA)
        request.session['job'] = job.id
        return HttpResponseRedirect('/minaret' + reverse('Results') + '?job=' + job.id)

# Create your views here.
def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def index2(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request, "show_t.html", context)
    elif 'n' in request.GET:
        n = request.GET['n']
        job = fft_random.delay(int(n))
        request.session['job'] = job.id
        return HttpResponseRedirect('/minaret' + reverse('index2') + '?job=' + job.id)
    else:
        form = UserForm()
        context = {'form':form,}
        return render(request,"post_form.html",context)

def rapSearch(request):
    #Check Author Names are Entered
    if 'pAuthnames' in request.GET and 'topics[]' in request.GET and 'TargetVenue' in request.GET:
        authornames = request.GET['pAuthnames']
        topicsq = request.GET.getlist('topics[]')
        citationsRangeMin = request.GET['minCitations']
        citationsRangeMax = request.GET['maxCitations']
        citationsType = request.GET['citationsType']
        venueq = request.GET['TargetVenue']
        affsq = request.GET['affs']
        affsq = affsq.replace("_", " ")
        citationsWt = request.GET['citationsWt']
        topRevWt = request.GET['topRevWt']
        topicMatchWt = request.GET['topicMatchWt']
        pubInVenueWt = request.GET['pubInVenueWt']
        recencyWt = request.GET['recencyWt']
        # Clean TmpCache
        files = glob.glob('tmpCache/*')
        for f in files:
            os.remove(f)
        
        request.session['authornames'] = authornames
        request.session['topicsq'] = topicsq
        request.session['minCitations'] = citationsRangeMin
        request.session['maxCitations'] = citationsRangeMax
        request.session['venueq'] = venueq
        request.session['affs'] = affsq
        request.session['citationsWt'] = citationsWt
        request.session['topRevWt'] = topRevWt
        request.session['topicMatchWt'] = topicMatchWt
        request.session['pubInVenueWt'] = pubInVenueWt
        request.session['recencyWt'] = recencyWt
        request.session['citationsType'] = citationsType
        
        #Open Bowser in Headless Mode
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options = options)
        eachAuthorLst, eachAuthorLstDblp, eachAuthorLstAcm = verifyAuthornames(authornames, driver)
        driver.quit()
        return render(request,'AuthorVerification.html', 
                      {
                           'authornames':authornames, 'eachAuthorLst':zip(authornames.split(',')[::-1], eachAuthorLst), 'eachAuthorLstDblp':zip(authornames.split(',')[::-1], eachAuthorLstDblp), 'eachAuthorLstAcm':zip(authornames.split(',')[::-1], eachAuthorLstAcm)
                      })
    else:
        t = get_template("index.html")
        html = t.render()
        return HttpResponse(html)
        
def About(request):
    t = get_template("about.html")
    html = t.render()
    return HttpResponse(html)
        
def Contact(request):
    t = get_template("contact.html")
    html = t.render()
    return HttpResponse(html)