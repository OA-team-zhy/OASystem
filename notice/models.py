from django.db import models

# Create your models here.
from django.db.models import TextField, DateTimeField
from django.forms import CharField


class Article(models.Model):
    title = models.CharField(max_length=32, default='title')
    content = models.TextField(null=True)
    pub_time = models.DateTimeField(null=True)
    egis = False

    def _unicode_(self):
        return self.title

class Schedule(models.Model):
    time = Article.pub_time
    title = Article.title
    egis = Article.egis

    def __str__(self):
        s = "时间：%s--题目：%s--审核：%s" % (self.time, self.title, self.egis)
        return s


