from django.shortcuts import reverse,redirect
from django.views.generic import CreateView, UpdateView

from defaultAPP.forms import GeneralUserRegisterForm, AdminRegisterForm, GeneralUserUpdateForm

from defaultAPP.models import GeneralUser, Admin
import random

from django.views.generic import UpdateView
from defaultAPP.forms import GeneralUserUpdateForm

class CreateGeneralUserView(CreateView):
    model = GeneralUser
    form_class = GeneralUserRegisterForm
    # fields = "__all__"
    template_name = "defaultAPP/register.html"
    success_url = "login"

    def form_valid(self, form):
        # 用户注册时通过注册编号自动生成账号
        no = form.cleaned_data["no"]
        # order_by默认升序排列，number前的负号表示降序排列
        generaluser_set = GeneralUser.objects.filter(no=no).order_by("-number")
        if generaluser_set.count() > 0:
            last_generaluser = generaluser_set[0]
            new_number = str(int(last_generaluser.number) + 1)
            for i in range(6 - len(new_number)):
                new_number = "0" + new_number
        else:
            new_number = "000001"

        # Create, but don't save the new user instance.
        new_generaluser = form.save(commit=False)
        # Modify the user
        new_generaluser.number = new_number
        # Save the new instance.
        new_generaluser.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_generaluser

        uid = no + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'generaluser'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))

    def get_context_data(self, **kwargs):
        context = super(CreateGeneralUserView, self).get_context_data(**kwargs)
        context["kind"] = "generaluser"

        return context


class CreateAdminView(CreateView):
    model = Admin
    form_class = AdminRegisterForm
    template_name = "defaultAPP/register.html"
    success_url = "login"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # 管理员注册时随机生成编号, 编号范围为[0,300)
        no = random.randint(0, 300)
        # 把非三位数的编号转换为以0填充的三位字符串，如1转换为'001'
        no = '{:0>3}'.format(no)
        admin_set = Admin.objects.filter(no=no).order_by("-number")
        if admin_set.count() > 0:
            last_admin = admin_set[0]
            new_number = int(last_admin.number) + 1
            new_number = '{:0>7}'.format(new_number)
        else:
            new_number = "0000001"

        # Create, but don't save the new admin instance.
        new_admin = form.save(commit=False)
        # Modify the admin
        new_admin.no = no
        new_admin.number = new_number
        # Save the new instance.
        new_admin.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_admin

        uid = no + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'admin'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))

    def get_context_data(self, **kwargs):
        context = super(CreateAdminView, self).get_context_data(**kwargs)
        context["kind"] = "admin"

        return context


class UpdateGeneralUserView(UpdateView):
    model = GeneralUser
    form_class = GeneralUserUpdateForm
    template_name = "defaultAPP/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateGeneralUserView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "GeneralUser"
        return context

    def get_success_url(self):
        return reverse("PageNavigation", kwargs={"kind": "generaluser"})


class UpdateAdminView(UpdateView):
    model = Admin
    form_class = AdminRegisterForm
    template_name = "defaultAPP/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateAdminView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "admin"
        return context

    def get_success_url(self):
        return reverse("PageNavigation", kwargs={"kind": "admin"})