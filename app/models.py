# from django.db import models
from mongoengine import Document, fields


class TextDocument(Document):
    url = fields.URLField(required=True)
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    score = fields.IntField(required=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


class DocumentRank(Document):
    document = fields.ReferenceField(TextDocument, required=True)
    rank = fields.FloatField(required=True)

    def __unicode__(self):
        return u"{0} : {1}".format(self.document, self.rank)


class PostingList(Document):
    term = fields.StringField(required=True)
    documents = fields.ListField(field=fields.ReferenceField(DocumentRank), default=list())

    def __unicode__(self):
        return u"{0}".format(self.term)