from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect

from defaultAPP.models import GeneralUser, Admin
from constants import INVALID_KIND

# Create your views here.


def get_user(request, kind):
    """

    :param request:
    :param kind: admin or generaluser
    :return: return Admin instance or GeneralUser instance
    """
    if request.session.get('kind', '') != kind or kind not in ["generaluser", "admin"]:
        return None
    if len(request.session.get('user', '')) != 10:
        return None

    uid = request.session.get('user')
    if kind == "generaluser":
        # 找到对应用户
        no = uid[:4]
        number = uid[4:]
        generaluser_set = GeneralUser.objects.filter(no=no, number=number)
        if generaluser_set.count() == 0:
            return None
        return generaluser_set[0]
    else:
        # 找到对应管理员
        no = uid[:3]
        number = uid[3:]
        admin_set = Admin.objects.filter(no=no, number=number)
        if admin_set.count() == 0:
            return None
        return admin_set[0]


def home(request, kind):
    if kind == "admin":
        return admin_home(request)
    elif kind == "generaluser":
        return generaluser_home(request)
    return HttpResponse(INVALID_KIND)


def admin_home(request):
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

    return render(request, 'PageNavigation/nav.html', context)


def generaluser_home(request):
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

    return render(request, 'PageNavigation/nav.html', context)

