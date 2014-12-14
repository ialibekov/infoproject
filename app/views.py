# -*- coding=utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from app.models import TextDocument, PostingList
from app.forms import SearchForm
from search import Search


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                search = Search()
                result = search.go(query)
                return render(request, 'app/result.html', {
                    'form': form,
                    'result': result,
                })

            except ValueError, error:
                messages.error(request, error.message)
                return HttpResponseRedirect('')
        else:
            messages.error(request, form.errors)
    else:
        form = SearchForm()

    return render(request, 'app/index.html', {
        'form': form,
    })


def build(request):
    search = Search()
    search.build()
    # search.export_index()
    return HttpResponseRedirect('/')




headers = {'User-Agent': 'Index Creating Bot POC'}
from requests import get
from bs4 import BeautifulSoup
import time
def walk_habr(request):
    """
    Walk habr and get url
    """
    base_url = 'http://habrahabr.ru/post/'
    with open('habr.json', 'w') as f:
        stories = list()
        # max_id = 243319
        max_id = 241500
        for i in range(240546, max_id):
            print i, 'out of', max_id
            time.sleep(1)
            url = base_url + str(i)
            r = get(url, headers=headers)
            if r.status_code == 404:
                print 'Get 404', url
                continue
            if u'Доступ к публикации закрыт' in r.text:
                print 'Article was closed', url
                continue
            soup = BeautifulSoup(r.text)
            title = soup.find('title')
            title = unicode(title.renderContents(), 'utf-8')[:-12]  # deleting / Habrahabr in the end of title
            text = soup.find("div", {"class": "content html_format"})
            text = unicode(text.get_text())
            score = soup.select("div.post div.voting span.score")[0].get_text()
            score = score.replace(u"\u2013", "-")
            score = int(score)
            rating = soup.select("div.post_show")
            try:
                TextDocument(url=url, title=title, text=text, score=score).save()
            except Warning:
                continue
    return HttpResponseRedirect('/')