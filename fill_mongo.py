#!/usr/bin/env python
import sys
import os
import argparse
import json
from app.models import TextDocument
from mongoengine import connect

MONGO_ID = 1
connect('infodb')

def putfile(path):
	global MONGO_ID
	f = open(path, 'r')
	serial = json.load(f)
	for d in serial:
		url = d['url']
		text = d['text']
		score = d['score']
		title = d['title']
		TextDocument(id=MONGO_ID, url=url, title=title, text=text, score=score).save()
		MONGO_ID += 1
		print title
	f.close

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="""
		Fill mongo database with json files from 'exclude' directory.
		""")
	parser.add_argument("-a", "--all", help="import all json-files",
						action="store_true")
	parser.add_argument("--clean", help="drop collection",
						action="store_true")
	parser.add_argument("files", nargs='*', help="specify json-files from extraction dir")
	args = parser.parse_args()
	if args.all:
		print "Not implemented yet."
		exit()
	if args.clean:
		TextDocument.drop_collection()
		exit()
	if args.files:
		for i in args.files:
			path = 'extraction/' + i
			putfile(path)