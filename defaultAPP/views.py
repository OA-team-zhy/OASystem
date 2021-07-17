from django.shortcuts import render
from django.http.response import HttpResponse

from constants import INVALID_KIND
from defaultAPP.forms import UserLoginForm, AdminLoginForm
from defaultAPP.cbvs import CreateUserView,CreateAdminView

# Create your views here.
def home(request):
    return render(request, "defaultAPP/login_home.html")

def login(request, *args, **kwargs):
    if not kwargs or "kind" not in kwargs or kwargs["kind"] not in ["admin", "user"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind':kind}

    if request.method == 'POST':
        if kind == "admin":
            form = AdminLoginForm(data=request.POST)
        else:
            form = UserLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]

            temp_res = "hello, %s" % uid
            return HttpResponse(temp_res)
        else:
            context['form'] = form
    elif request.method == 'GET':
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            data = {"uid":uid, 'password':'12345678'}
            if kind == "admin":
                form = AdminLoginForm(data)
            else:
                form = UserLoginForm
        else:
            if kind == "admin":
                form = AdminLoginForm()
            else:
                form = UserLoginForm()

        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

        return render(request, 'defaultAPP/login_detail.html', context)

def register(request, kind):
    func = None
    if kind == "user":
        func = CreateUserView.as_view()
    elif kind == "admin":
        func = CreateAdminView.as_view()

    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)