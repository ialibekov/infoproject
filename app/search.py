#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import TextDocument, PostingList, DocumentRank
from pymystem3 import Mystem
import re
from math import log10
import mongoengine

PUNCTUATION = re.compile(u' .,?!:;|/\(\)]\[\\"\'-', re.UNICODE)
PARTSTRING = re.compile(u'[^.;\u2013]+', re.UNICODE)
SNIPPET_LENGHT = 300


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

    def lemmatize(self, text):
        for word in self.stemmer.lemmatize(text):
            term = PUNCTUATION.sub(" ", word).strip().lower()
            if term:
                yield term

    def count_inclusion(self, norm_query, text):
        count = 0
        for t in self.lemmatize(text):
            if t in norm_query:
                count += 1
        return count

    def snippet(self, text, query):
        print "+++++"
        query = [q for q in self.lemmatize(query)][:30]
        text = PARTSTRING.findall(text);

        weights = [(i, self.count_inclusion(query, t), len(t)) for i, t in enumerate(text)]

        sorted_weights = sorted(weights, key=lambda tup: tup[1], reverse=True)[:5]
        print sorted_weights
        print text[sorted_weights[0][0]]

        # regular snippeted lengths
        snippet_len = 0
        num_sentences = 0
        for num_sentences, w in enumerate(sorted_weights):
            snippet_len += w[2]
            num_sentences += 1
            if snippet_len > SNIPPET_LENGHT:
                break

        sorted_weights = sorted_weights[:num_sentences]
        sorted_weights = sorted(sorted_weights, key=lambda tup: tup[0])
        snippet = ""
        for w in sorted_weights:
            if w[1] > 0:
                snippet += text[w[0]]
                snippet += " ... "

        # if we don't return 
        if snippet == "":
            snippet == text[:SNIPPET_LENGHT]
        
        return snippet

    def go(self, query):
        result = dict()
        for word in self.stemmer.lemmatize(query):
            term = PUNCTUATION.sub(" ", word).strip().lower()
            if term:
                try:
                    ranked_documents = PostingList.objects.get(term=term).select_related(max_depth=2).documents
                    for rd in ranked_documents:
                        doc = rd.document
                        result[doc] = result.setdefault(doc, 0) + rd.rank
                except mongoengine.errors.DoesNotExist:
                    continue
        sorted_result = sorted(result.items(), key=lambda tup: tup[1], reverse=True)[:100]
        return [(doc.url, doc.title, self.snippet(doc.text, query)) for doc, rank in sorted_result]
