from django.contrib import admin

# Register your models here.
from notice.models import Article


class Wnotice(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time']


admin.site.register(Article, Wnotice)