from django.db import models
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=32, default='title')
    content = models.TextField(null=True)
    pub_time = models.TextField(null=True)

    def __unicode__(self):
        return self.title