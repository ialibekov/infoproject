#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import TextDocument, PostingList, DocumentRank
from pymystem3 import Mystem
import re
from math import log10

PUNCTUATION = re.compile(u' .,?!:;\(\)"\'-', re.UNICODE)


class Search(object):

    def __init__(self):
        self.stemmer = Mystem()
        # self.index = dict()
        # self.terms = list()
        self.terms = dict()
        self.num_of_documents = 0.0

    def build(self):
        for doc_id, document in TextDocument.objects.values_list('id', 'text'):
            self.num_of_documents += 1
            for word in self.stemmer.lemmatize(document):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms[term][doc_id] = self.terms.setdefault(term, dict()).setdefault(doc_id, 0) + 1

        for term, documents in self.terms.iteritems():
            idf = log10(self.num_of_documents / len(documents))
            p = PostingList.objects.create(term=term, documents=list())
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
                for doc_id, tf_idf in self.index.get(term, []):
                    if doc_id in result:
                        result[doc_id] += tf_idf
                    else:
                        result[doc_id] = tf_idf
        result_doc_id = [doc_id for doc_id, tf_idf in sorted(result.items(), key=lambda tup: tup[1], reverse=True)[:10]]
        return TextDocument.objects.filter(id__in=result_doc_id).values_list('url', 'title')