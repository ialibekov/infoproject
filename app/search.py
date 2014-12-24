#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import TextDocument, TextPostingList, TitlePostingList, TextDocumentRank, TitleDocumentRank
from pymystem3 import Mystem
from spell.spell import SpellChecker
import re
from math import log10
from nltk.tokenize import word_tokenize
import mongoengine
import sys

PUNCTUATION = re.compile(u' .,?!:;|/\(\)]\[\\"\'-', re.UNICODE)
PARTSTRING = re.compile(u'[^.;\u2013]+', re.UNICODE)
WORDS = re.compile(u'\w+', re.UNICODE)
SNIPPET_LENGHT = 500

def enc_check(word):
    if isinstance(word, unicode):
        return word
    return unicode(word, 'utf-8')


class Search(object):

    def __init__(self):
        self.stemmer = Mystem()
        self.terms_in_text = dict()
        self.terms_in_title = dict()
        self.num_of_documents = 0.0
        self.spell_checker = SpellChecker()

    def build(self):
        TextPostingList.drop_collection()
        TitlePostingList.drop_collection()
        TextDocumentRank.drop_collection()
        TitleDocumentRank.drop_collection()
        for doc_id, text, title in TextDocument.objects.values_list('id', 'text', 'title'):
            print doc_id
            self.num_of_documents += 1
            for word in self.stemmer.lemmatize(text):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms_in_text[term][doc_id] = self.terms_in_text.setdefault(term, dict()).setdefault(doc_id, 0) + 1

            for word in self.stemmer.lemmatize(title):
                term = PUNCTUATION.sub(" ", word).strip().lower()
                if term:
                    self.terms_in_title[term][doc_id] = self.terms_in_title.setdefault(term, dict()).setdefault(doc_id, 0) + 1

        # building index for texts
        print "\nbuilding index for texts"
        i = 1
        n = len(self.terms_in_text)
        print "{0} of {1}".format(i, n)

        for term, documents in self.terms_in_text.iteritems():

            if i % 100 == 0:
                print "{0} of {1}".format(i, n)
            i += 1

            idf = log10(self.num_of_documents / len(documents))
            p = TextPostingList.objects.create(term=term)
            for document, tf in sorted(documents.items(), key=lambda tup: tup[1], reverse=True):
                rank = (1 + log10(tf)) * idf
                p.documents.append(TextDocumentRank.objects.create(document=document, rank=rank))
            p.save()
        del self.terms_in_text

        # building index for titles
        print "\nbuilding index for titles"
        i = 1
        n = len(self.terms_in_title)
        print "{0} of {1}".format(i, n)

        for term, documents in self.terms_in_title.iteritems():

            if i % 100 == 0:
                print "{0} of {1}".format(i, n)
            i += 1

            idf = log10(self.num_of_documents / len(documents))
            p = TitlePostingList.objects.create(term=term)
            for document, tf in sorted(documents.items(), key=lambda tup: tup[1], reverse=True):
                rank = (1 + log10(tf)) * idf
                p.documents.append(TitleDocumentRank.objects.create(document=document, rank=rank))
            p.save()
        del self.terms_in_title

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

    def bold_snippet(self, norm_query, snippet):
        bold_snippet = snippet
        for t in word_tokenize(snippet):
            t = self.lemmatize(t)[0]


    def snippet(self, text, query):
        query = [q for q in self.lemmatize(query)][:30]
        text = PARTSTRING.findall(text)

        #weights = [(i, self.count_inclusion(query, t), len(t)) for i, t in enumerate(text)]

        len_snippet = 0
        snippet = ""
        for t in text:
            if self.count_inclusion(query, t) != 0:
                snippet += t
                snippet += " ... "
                len_snippet += len(t)
                if len_snippet > SNIPPET_LENGHT:
                    break

        # sorted_weights = sorted(weights, key=lambda tup: tup[1], reverse=True)[:5]
        # print sorted_weights
        # print text[sorted_weights[0][0]]

        # regular snippeted lengths
        # snippet_len = 0
        # num_sentences = 0
        # for num_sentences, w in enumerate(sorted_weights):
        #     snippet_len += w[2]
        #     num_sentences += 1
        #     if snippet_len > SNIPPET_LENGHT:
        #         break

        # sorted_weights = sorted_weights[:num_sentences]
        # sorted_weights = sorted(sorted_weights, key=lambda tup: tup[0])
        # snippet = ""
        # for w in sorted_weights:
        #     if w[1] > 0:
        #         snippet += text[w[0]]
        #         snippet += " ... "

        # if we don't return 
        if snippet == "":
            snippet == text[:SNIPPET_LENGHT]


        
        return snippet

    def go(self, query):
        result = dict()
        title_weight = 2
        for word in self.stemmer.lemmatize(query):
            term = PUNCTUATION.sub(" ", word).strip().lower()
            if term:
                try:
                    ranked_documents = TitlePostingList.objects.get(term=term).select_related(max_depth=2).documents
                    for rd in ranked_documents:
                        doc = rd.document
                        result[doc] = result.setdefault(doc, 0) + rd.rank * title_weight
                except mongoengine.errors.DoesNotExist:
                    pass
                try:
                    ranked_documents = TextPostingList.objects.get(term=term).select_related(max_depth=2).documents
                    for rd in ranked_documents:
                        doc = rd.document
                        result[doc] = result.setdefault(doc, 0) + rd.rank
                except mongoengine.errors.DoesNotExist:
                    continue
        sorted_result = sorted(result.items(), key=lambda tup: tup[1], reverse=True)[:100]
        return [(doc.url, doc.title, self.snippet(doc.text, query)) for doc, rank in sorted_result]
        #return [(doc.url, doc.title) for doc, rank in sorted_result]

    def generate_suggest(self, query):
        text = WORDS.findall(query)
        try: 
            if text:
                sug = u' '.join([enc_check(self.spell_checker.spell(i)) for i in text])
                orig = u' '.join([i for i in text])
                if sug != orig:
                    return sug
        except:
            print "Some errors occured... ", sys.exc_info()[0] 
        return None

