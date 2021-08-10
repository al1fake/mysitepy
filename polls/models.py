import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):

    header = models.CharField(max_length=100)
    article_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    img_link = models.CharField(max_length=50)
    article_img_link = models.TextField()

    @property
    def preview(self):
        return self.article_text[:150] + '...'
