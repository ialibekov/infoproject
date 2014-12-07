#!/usr/bin/env python
# -*- coding=utf-8 -*- 
import requests
import json
import time

from requests import get
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Index Creating Bot POC'}


def walk_hackernews():
    """
    Walks ang get list urls with articles
    """
    base_url = 'https://hacker-news.firebaseio.com/v0/'
    with open('hn_2.json', 'w') as f:
        stories = list()
        # top_stories = json.loads(get(base_url + 'topstories.json').text)
        # max_id = int(get(base_url + 'maxitem.json', headers=headers).text)
        max_id = 8614319
        max_id = max_id - 10000
        for item in range(max_id - 1000, max_id + 1):
            print item, 'out of', max_id
            time.sleep(1)
            url = base_url + 'item/' + str(item) + '.json'
            j = json.loads(get(url, headers=headers).text)
            if j['type'] == 'story' and 'deleted' not in j:
                print j['id']
                stories.append({'url': j['url'], 'title': j['title'],
                                'score': j['score']})
                print j['url']
        json.dump(stories, f)


def walk_reddit():
    """
    Walk reddit and get urls
    """
    base_url = 'http://www.reddit.com/r/programming/'
    option_api = 'new.json?sort=new&limit=100&after={after}'
    with open('reddit_2.json', 'w') as f:
        stories = list()

        i = 0
        after = ''
        while i < 30:
            url = base_url + option_api.format(after=after)
            print url
            time.sleep(1)
            r = get(url, headers=headers)
            while not r.ok:
                print 'Repeat attempt'
                time.sleep(5)
                r = get(url, headers=headers)

            j = r.json()
            # print j
            try:
                wj = j['data']
                after = wj['after']
                wj = wj['children']
                for elem in wj:
                    elem = elem['data']
                    # print elem
                    stories.append({'url': elem['url'], 'title': elem['title'],
                                    'score': elem['score']})

            except KeyError:
                print 'Error', r
                after = None

            print 'Iteration ', i
            i += 1
            if not after:
                print j
                print 'None after'
                break

        json.dump(stories, f)


def walk_habr():
    """
    Walk habr and get url
    """
    base_url = 'http://habrahabr.ru/post/'
    with open('habr.json', 'w') as f:
        stories = list()
        # max_id = 243319
        max_id = 2400010
        for i in range(240000, max_id + 1):
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
            title = unicode(title.renderContents(), 'utf-8')
            text = soup.find("div", {"class": "content html_format"})
            text = unicode(text.get_text())
            stories.append({'url': url, 'title': title, 'text': text})
        json.dump(stories, f)


if __name__ == '__main__':
    # walk_hackernews()
    # walk_reddit()
    walk_habr()