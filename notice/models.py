from django.db import models

# Create your models here.
from django.db.models import TextField, DateTimeField
from django.forms import CharField


class Article(models.Model):
    title = models,CharField(max_length=32, default='title')
    content = models,TextField(null=True)
    pub_time = models,DateTimeField(null=True)
    def _unicode_(self):
        return self.title
