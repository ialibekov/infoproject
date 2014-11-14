#/usr/bin/env python
import requests
import json

from requests import get

def walk_hackernews():
	'''
	Walks ang get list urls with articles
	'''
	base_url = 'https://hacker-news.firebaseio.com/v0/'
	with open('hn.json', 'w') as f:
		stories = list()
		# top_stories = json.loads(get(base_url + 'topstories.json').text)
		max_id = int(get(base_url + 'maxitem.json').text)
		print max_id
		for item in range(max_id - 300, max_id + 1):
		 	url = base_url + 'item/' + str(item) + '.json'
		 	j = json.loads(get(url).text)
		 	if j['type'] == 'story' and 'deleted' not in j:
		 		print j['id']
		 		stories.append({'url': j['url'], 'title': j['title'], 
		 			'score': j['score']})
		 		print j['url']
		json.dump(stories, f)

if __name__ == '__main__':
	walk_hackernews()
