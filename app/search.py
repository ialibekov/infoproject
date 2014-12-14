#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import TextDocument, PostingList, DocumentRank
from pymystem3 import Mystem
import re
from math import log10
import mongoengine

PUNCTUATION = re.compile(u' .,?!:;|/\(\)]\[\\"\'-', re.UNICODE)


class Search(object):

    def __init__(self):
        self.stemmer = Mystem()
        self.terms = dict()
        self.num_of_documents = 0.0

    def build(self):
        PostingList.drop_collection()
        DocumentRank.drop_collection()
        for doc_id, document in TextDocument.objects.values_list('id', 'text'):
            print doc_id
            self.num_of_documents += 1
            for word in self.stemmer.lemmatize(document):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms[term][doc_id] = self.terms.setdefault(term, dict()).setdefault(doc_id, 0) + 1

        for term, documents in self.terms.iteritems():
            idf = log10(self.num_of_documents / len(documents))
            p = PostingList.objects.create(term=term)
            for document, tf in sorted(documents.items(), key=lambda tup: tup[1], reverse=True):
                rank = (1 + log10(tf)) * idf
                p.documents.append(DocumentRank.objects.create(document=document, rank=rank))
            p.save()

        del self.terms

    def go(self, query):
        result = dict()
        for word in self.stemmer.lemmatize(query):
            term = PUNCTUATION.sub(" ", word).strip().lower()
            if term:
                print term
                try:
                    ranked_documents = PostingList.objects.get(term=term).select_related(max_depth=2).documents
                    for rd in ranked_documents:
                        doc = rd.document
                        result[doc] = result.setdefault(doc, 0) + rd.rank
                except mongoengine.errors.DoesNotExist:
                    continue
        print sorted(result.items(), key=lambda tup: tup[1], reverse=True)
        return [(doc.url, doc.title)for doc, rank in sorted(result.items(), key=lambda tup: tup[1], reverse=True)[:10]]