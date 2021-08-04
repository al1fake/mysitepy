import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):

    header = models.CharField(max_length=100)
    article_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    img_link = models.CharField(max_length=50)

    @property
    def preview(self):
        return self.article_text[:150] + '...'

    @property
    def is_recently_published(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
