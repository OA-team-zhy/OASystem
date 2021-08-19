from django.shortcuts import render

# Create your views here.

from notice import models



def index(request):
    articles = models.Article.objects.all()
    return render(request, 'notice/notice_home.html', {'articles': articles})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/article_page.html', {'article': article})


def edit_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'notice/edit_page.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/edit_page.html', {'article': article})


def change(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        models.Article.objects.create(title=title, content=content)
        articles = models.Article.objects.all()
        return render(request, 'notice/notice_home.html', {'articles': articles})

    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    return render(request, 'notice/article_page.html', {'article': article})


def delete_page(request, article_id):
    models.Article.objects.filter(pk=article_id).delete()
    articles = models.Article.objects.all()
    return render(request, 'notice/index.html', {'articles': articles})