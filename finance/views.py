from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from PageNavigation.views import get_user
from constants import INVALID_KIND


def finance_home(request, kind):
    if kind == "admin":
        return admin_finance_home(request)
    elif kind == "generaluser":
        return generaluser_finance_home(request)
    return HttpResponse(INVALID_KIND)


def admin_finance_home(request):
    kind = "admin"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'PageNavigation/model.html', context)


def generaluser_finance_home(request):
    kind = "generaluser"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'PageNavigation/model.html', context)

