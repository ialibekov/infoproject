# from django.db import models
from mongoengine import Document, fields


class TextDocument(Document):
    url = fields.URLField(required=True)
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


class DocumentRank(Document):
    document = fields.ReferenceField(TextDocument, required=True)
    tf_idf = fields.FloatField(required=True)

    def __unicode__(self):
        return u"{0} : {1}".format(self.document, self.tf_idf)


class PostingList(Document):
    term = fields.StringField(required=True)
    documents = fields.ListField(field=fields.ReferenceField(DocumentRank), required=True, default=list())

    def __unicode__(self):
        return u"{0}".format(self.term)