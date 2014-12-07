#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import Document
from pymystem3 import Mystem
import pickle
import re
from math import log10

PUNCTUATION = re.compile(u' .,?!:;\(\)"\'-', re.UNICODE)


class Search(object):

    def __init__(self):
        self.stemmer = Mystem()
        self.index = dict()
        self.terms = list()
        self.num_of_documents = 0.0

    def build(self):
        for doc_id, document in Document.objects.values_list('id', 'text'):
            print doc_id
            self.num_of_documents += 1
            for word in self.stemmer.lemmatize(document):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms.append((term, doc_id))

        self.terms.sort(key=lambda tup: (tup[0], tup[1]))

        current_term = self.terms[0][0]
        current_doc_id = self.terms[0][1]
        doc_id_tf = list()
        tf = 1
        for term, doc_id in self.terms:
            if term == current_term:
                if doc_id != current_doc_id:
                    tf = 1 + log10(tf)
                    doc_id_tf.append((current_doc_id, tf))
                    current_doc_id = doc_id
                    tf = 1
                else:
                    tf += 1
            else:
                doc_id_tf.append((current_doc_id, tf))
                self.index[current_term] = doc_id_tf
                current_term = term
                current_doc_id = doc_id
                doc_id_tf = list()
                tf = 1
        tf = 1 + log10(tf)
        doc_id_tf.append((current_doc_id, tf))
        self.index[current_term] = doc_id_tf
        del self.terms

        for key, values in self.index.items():
            idf = log10(self.num_of_documents/len(values))
            self.index[key] = list()
            for doc_id, tf in values:
                self.index[key].append((doc_id, tf * idf))
                self.index[key].sort(key=lambda tup: tup[1], reverse=True)

    def export_index(self):
        with open("index", "w") as f:
            pickle.dump(self.index, f)

    def import_index(self):
        with open("index", "r") as f:
            self.index = pickle.load(f)

    def go(self, query):
        result = dict()
        for word in self.stemmer.lemmatize(query):
            term = PUNCTUATION.sub(" ", word).strip().lower()
            if term:
                print len(self.index.get(term, []))
                for doc_id, tf_idf in self.index.get(term, []):
                    if doc_id in result:
                        result[doc_id] += tf_idf
                    else:
                        result[doc_id] = tf_idf
        result_doc_id = [doc_id for doc_id, tf_idf in sorted(result.items(), key=lambda tup: tup[1], reverse=True)[:10]]
        return Document.objects.filter(id__in=result_doc_id).values_list('url', 'title')