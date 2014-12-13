# from django.db import models
from mongoengine import Document, fields


class TextDocument(Document):
    url = fields.URLField(required=True)
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


class PostingList(Document):
    term = fields.StringField(required=True)
    documents = fields.ListField(field=fields.ObjectIdField(), required=True)

    def __unicode__(self):
        return u"{0}".format(self.term)


class TfIdf(Document):
    pass