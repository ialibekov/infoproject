# -*- coding=utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from app.models import TextDocument, TextPostingList, TitlePostingList
from app.forms import SearchForm
from search import Search

def go_search(query, need_suggest=True):
    search = Search()
    if (need_suggest):
        suggest = search.generate_suggest(query)
    else:
        suggest = ""
    result = search.go(query)
    return result, suggest


def index(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                result, suggest = go_search(query)
                return render(request, 'app/result.html', {
                    'form': form,
                    'result': result,
                    'suggest': suggest
                })

            except ValueError, error:
                messages.error(request, error.message)
                return HttpResponseRedirect('')
        else:
            print "Invalid"
            messages.error(request, form.errors)
    else:
        query = request.GET.get('q', '')
        if query:
            form = SearchForm({'query': query})
            result, suggest = go_search(query)
            return render(request, 'app/result.html', {
                'form': form,
                'result': result,
                'suggest': suggest
                })
    
    return render(request, 'app/index.html', {
        'form': form,
    })


def build(request):
    search = Search()
    search.build()
    # search.export_index()
    return HttpResponseRedirect('/')


headers = {'User-Agent': 'Index Creating Bot POC'}
import requests
from bs4 import BeautifulSoup
import time
def walk_habr(request):
    """
    Walk habr and get url
    """
    base_url = 'http://habrahabr.ru/post/'
    with open('habr.json', 'w') as f:
        stories = list()
        # max_id = 246413
        # 243319
        max_id = 240000
        for i in range(229660, max_id):
            print i, 'out of', max_id
            time.sleep(1)
            url = base_url + str(i)
            try:
                r = requests.get(url, headers=headers)
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
                if score == u"\u2014":
                    continue
                score = score.replace(u"\u2013", "-")
                score = int(score)
                rating = soup.select("div.post_show")
                try:
                    TextDocument(id=i, url=url, title=title, text=text, score=score).save()
                except Warning:
                    continue
            # except requests.exceptions.ConnectionError:
            except:
                print "Some error at " + url
                continue
    return HttpResponseRedirect('/')