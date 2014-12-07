# -*- coding=utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from app.models import Document


def index(request):
    # return HttpResponse("Hello!")
    return render(request, 'app/index.html')


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
        for i in range(240500, max_id):
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
            Document.objects.create(url=url, title=title, text=text)
    return HttpResponseRedirect('/')