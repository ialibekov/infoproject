from django.db import models


class Document(models.Model):
    url = models.URLField(max_length=255)
    title = models.CharField(max_length=1000)
    text = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.title)