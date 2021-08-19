from django.contrib import admin

from notice.models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_time')
    list_filter = ('pub_time',)


admin.site.register(Article, ArticleAdmin)