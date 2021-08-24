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
        return self.article_text.replace('/n', '')[:150] + '...'


class Comment(models.Model):
    post = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    #email = models.EmailField()
    body = models.CharField('Оставьте комментарий', max_length=80)
    created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
