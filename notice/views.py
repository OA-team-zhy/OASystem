from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from PageNavigation.views import get_user
from constants import INVALID_REQUEST_METHOD
from notice.forms import ArtForm
from notice.models import Article


# def notice_index(request):
#     article_list = Article.objects.all()
#     return render(request, 'article.html',{'article_list':article_list})

def create_notice(request):
    user = get_user(request, "generaluser")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "generaluser"}))

    info = {
        "name": user.name,
        "kind": "generaluser",
    }

    if request.method == 'POST':
        form = ArtForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 1
            obj.generaluser = user

            obj.save()
            return redirect(reverse("course", kwargs={"kind": "generaluser"}))
    elif request.method == 'GET':
        form = ArtForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'notice/create_notice.html', {'info': info, 'form': form})