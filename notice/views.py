from django.shortcuts import render

# Create your views here.
from notice.models import Article


def notice_index(request):
    article_list = Article.objects.all()
    return render(request, 'article.html',{'article_list':article_list})