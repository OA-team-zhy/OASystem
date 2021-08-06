from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse

from constants import INVALID_KIND
from defaultAPP.forms import GeneralUserLoginForm, AdminLoginForm
from defaultAPP.cbvs import CreateGeneralUserView, CreateAdminView, UpdateGeneralUserView, UpdateAdminView
from defaultAPP.models import GeneralUser, Admin

# Create your views here.


def home(request):
    return render(request, "defaultAPP/index.html")

def login(request, kind):
    if kind not in ["admin", "generaluser"]:
        return HttpResponse(INVALID_KIND)

    if request.method == 'POST':
        if kind == "admin":
            form = AdminLoginForm(data=request.POST)
        else:
            form = GeneralUserLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error("uid", "账号长度必须为10")
            else:
                if kind == "admin":
                    no = uid[:3]
                    number = uid[3:]
                    object_set = Admin.objects.filter(no=no, number=number)
                else:
                    no = uid[:4]
                    number = uid[4:]
                    object_set = GeneralUser.objects.filter(no=no, number=number)
                if object_set.count() == 0:
                    form.add_error("uid", "该账号不存在.")
                else:
                    user = object_set[0]#user为编号
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id

                        return redirect("PageNavigation", kind=kind)

            return render(request, 'defaultAPP/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            if kind == "admin":
                form = AdminLoginForm({"uid": uid, 'password': '12345678'})
            else:
                form = GeneralUserLoginForm({"uid": uid, 'password': '12345678'})
        else:
            if kind == "admin":
                form = AdminLoginForm()
            else:
                form = GeneralUserLoginForm()
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

        return render(request, 'defaultAPP/login_detail.html', context)

def register(request, kind):
    func = None
    if kind == "generaluser":
        func = CreateGeneralUserView.as_view()
    elif kind == "admin":
        func = CreateAdminView.as_view()

    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)

def logout(request):
    for sv in ["kind", "user", "id"]:
        if request.session.get(sv):
            del request.session[sv]
    return redirect(reverse("login"))

def update(request, kind):
    func = None
    if kind == "generaluser":
        func = UpdateGeneralUserView.as_view()
    elif kind == "admin":
        func = UpdateAdminView.as_view()
    else:
        return HttpResponse(INVALID_KIND)

    pk = request.session.get("id")
    if pk:
        context = {
            "name": request.session.get("name", ""),
            "kind": request.session.get("kind", "")
        }
        return func(request, pk=pk, context=context)

    return redirect("login")

def back(request):
    return redirect(reverse("login"))