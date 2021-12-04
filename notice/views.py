import time

from django.http import HttpResponse
from django.shortcuts import render

from constants import INVALID_KIND
from notice import models


def notice_home(request, kind):
    if kind == "admin":
        return admin_notice_home(request)
    elif kind == "generaluser":
        return generaluser_notice_home(request)
    return HttpResponse(INVALID_KIND)


def admin_notice_home(request):

    articles = models.Article.objects.all()

    return render(request, 'notice/notice_home_admin.html', {'articles': articles})


def generaluser_notice_home(request):

    articles = models.Article.objects.all()

    return render(request, 'notice/notice_home_generaluser.html', {'articles': articles})


def index(request):
    articles = models.Article.objects.all()
    return render(request, 'notice/notice_home_anyone.html', {'articles': articles})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/article_page.html', {'article': article})

def article_page_generaluser(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/article_page_generaluser.html', {'article': article})

def article_page_anyone(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/article_page_anyone.html', {'article': article})

def edit_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'notice/edit_page_admin.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/edit_page_admin.html', {'article': article})

def edit_page_generaluser(request, article_id):
    if str(article_id) == '0':
        return render(request, 'notice/edit_page.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'notice/edit_page.html', {'article': article})


def change(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    pub_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        models.Article.objects.create(title=title, content=content, pub_time=pub_time)
        articles = models.Article.objects.all()
        return render(request, 'notice/notice_home.html', {'articles': articles})

    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.pub_time = pub_time
    article.save()
    return render(request, 'notice/article_page.html', {'article': article})

def change_generaluser(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    pub_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        models.Article.objects.create(title=title, content=content, pub_time=pub_time)
        articles = models.Article.objects.all()
        return render(request, 'notice/notice_home_generaluser.html', {'articles': articles})

    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.pub_time = pub_time
    article.save()
    return render(request, 'notice/article_page_generaluser.html', {'article': article})


def delete_page(request, article_id):
    models.Article.objects.filter(pk=article_id).delete()
    articles = models.Article.objects.all()
    return render(request, 'notice/notice_home_admin.html', {'articles': articles})