#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import TextDocument, PostingList
from pymystem3 import Mystem
import pickle
import re
from math import log10

PUNCTUATION = re.compile(u' .,?!:;\(\)"\'-', re.UNICODE)


class Search(object):

    def __init__(self):
        self.stemmer = Mystem()
        # self.index = dict()
        self.terms = list()
        self.num_of_documents = 0.0

    def build(self):
        for doc_id, document in TextDocument.objects.values_list('id', 'text'):
            print doc_id
            self.num_of_documents += 1
            for word in self.stemmer.lemmatize(document):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms.append((term, doc_id))

        self.terms.sort(key=lambda tup: (tup[0], tup[1]))

        current_term = self.terms[0][0]
        current_doc_id = self.terms[0][1]
        doc_ids = list()
        tf_idfs = list()
        tf = 1.0
        for term, doc_id in self.terms:
            if term == current_term:
                if doc_id != current_doc_id:
                    tf = 1.0 + log10(tf)
                    doc_ids.append(current_doc_id)
                    tf_idfs.append(tf)
                    current_doc_id = doc_id
                    tf = 1.0
                else:
                    tf += 1.0
            else:
                doc_ids.append(current_doc_id)
                tf_idfs.append(tf)
                # self.index[current_term] = doc_id_tf
                print tf_idfs
                PostingList(term=current_term, documents=doc_ids, tf_idfs=tf_idfs).save()
                current_term = term
                current_doc_id = doc_id
                doc_ids = list()
                tf_idfs = list()
                tf = 1.0
        tf = 1.0 + log10(tf)
        doc_ids.append(current_doc_id)
        tf_idfs.append(tf)
        PostingList(term=current_term, documents=doc_ids, tf_idfs=tf_idfs).save()
        del self.terms

        """
        for key, values in self.index.items():
            idf = log10(self.num_of_documents/len(values))
            self.index[key] = list()
            for doc_id, tf in values:
                self.index[key].append((doc_id, tf * idf))
                self.index[key].sort(key=lambda tup: tup[1], reverse=True)
        """

    """
    def export_index(self):
        with open("index", "w") as f:
            pickle.dump(self.index, f)

    def import_index(self):
        with open("index", "r") as f:
            self.index = pickle.load(f)
    """

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
        return TextDocument.objects.filter(id__in=result_doc_id).values_list('url', 'title')