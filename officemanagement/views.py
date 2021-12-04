from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from PageNavigation.views import get_user
from constants import INVALID_KIND, INVALID_REQUEST_METHOD, ILLEGAL_KIND
from officemanagement.models import Office, Schedule, GeneralUserOffice
from django.db.models import Q
from officemanagement.forms import OfficeForm, ScheduleForm
from django.utils import timezone


def officemanagement_home(request, kind):
    if kind == "admin":
        return admin_officemanagement_home(request)
    elif kind == "generaluser":
        return generaluser_officemanagement_home(request)
    return HttpResponse(INVALID_KIND)


def admin_officemanagement_home(request):
    kind = "admin"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    is_search = False
    search_key = ""
    if request.method == "POST":
        search_key = request.POST.get("search")
        if search_key:
            is_search = True

    context = {
        "info": info
    }
    q = Q(admin=user)
    if is_search:
        q = q & Q(name__icontains=search_key)
        context["search_key"] = search_key

    context["office_list"] = Office.objects.filter(q).order_by('status')

    return render(request, 'officemanagement/Admin/home.html', context)


def generaluser_officemanagement_home(request):
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

    return render(request, 'officemanagement/GeneralUser/home.html', context)




def home(request):
    return render(request, "officemanagement/Admin/office.html")


def create_office(request):

    user = get_user(request, "admin")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "admin"}))

    info = {
        "name": user.name,
        "kind": "admin",
    }

    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 1
            obj.admin = user

            obj.save()
            return redirect(reverse("office", kwargs={"kind": "admin"}))
    elif request.method == 'GET':
        form = OfficeForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'officemanagement/Admin/create_office.html', {'info': info, 'form': form})


def create_schedule(request, office_id):
    kind = "admin"
    user = get_user(request, kind)
    if not user:
        return redirect(reverse("login", kwargs={"kind": kind}))

    info = {
        "name": user.name,
        "kind": kind,
    }

    office = Office.objects.get(pk=office_id)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.office = office
            obj.save()

            return redirect(reverse("view_detail", kwargs={"office_id": office_id}))
    elif request.method == 'GET':
        form = ScheduleForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'officemanagement/Admin/create_schedule.html',
                  {'info': info, 'form': form, "office": office})


def delete_schedule(request, schedule_id):
    user = get_user(request, "admin")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "admin"}))

    schedule = Schedule.objects.get(pk=schedule_id)

    office_id = request.GET.get("office_id") or schedule.office.id

    schedule.delete()

    return redirect(reverse("view_detail", kwargs={"office_id": office_id}))


def handle_office(request, office_id, handle_kind):
    """
    :param request:
    :param office_id:
    :param handle_kind:
            1: "开始选会议室",
            2: "结束选会议室",
            3: "关闭会议室",
            4: "给分完成"
    :return:
    """
    user = get_user(request, "admin")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "admin"}))

    info = {
        "name": user.name,
        "kind": "admin",
    }

    office = Office.objects.get(pk=office_id)
    if office.status == handle_kind and office.status < 5:
        if office.status == 4:
            scs = GeneralUserOffice.objects.filter(office=office)
            all_given = True
            res = ""
            for sc in scs:
                if sc.scores is None:
                    all_given = False
                    res += "<div>%s 未打分</div>" % sc.generaluser

            if all_given:
                office.status += 1
                office.save()
                return redirect(reverse("view_detail", kwargs={"office_id": office.id}))
            else:
                return HttpResponse(res)
        else:
            office.status += 1
            office.save()

    office_list = Office.objects.filter(admin=user)
    return render(request, 'officemanagement/Admin/home.html', {'info': info, 'office_list': office_list})


def view_detail(request, office_id):
    user = get_user(request, "admin")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "admin"}))

    info = {
        "name": user.name,
        "kind": "admin",
    }

    office = Office.objects.get(pk=office_id)
    c_stu_list = GeneralUserOffice.objects.filter(office=office)
    sche_list = Schedule.objects.filter(office=office)

    context = {
        "info": info,
        "office": office,
        "office_generalusers": c_stu_list,
        "schedules": sche_list
    }

    if office.status == 5:
        sorted_cs_list = sorted(c_stu_list, key=lambda cs: cs.scores)
        context["sorted_office_generalusers"] = sorted_cs_list

    return render(request, "officemanagement/Admin/office.html", context)


def view_office(request, view_kind):
    """
    :param view_kind:
        current: 查看当前会议室
        is_end: 查看已关会议室
        select: 选会议室
        withdraw: 撤销会议室
    """
    user = get_user(request, "generaluser")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "generaluser"}))

    is_search = False
    search_key = ""
    if request.method == "POST":
        search_key = request.POST.get("search")
        if search_key:
            is_search = True

    info = {
        "name": user.name,
        "kind": "generaluser",
    }

    office_list = []

    if view_kind in ["select", "current", "withdraw", "is_end"]:
        if view_kind == "select":
            q = Q(status=2)
            if is_search:
                q = q & (Q(name__icontains=search_key) | Q(admin__name__icontains=search_key))

            office_list = Office.objects.filter(q)

            my_office = GeneralUserOffice.objects.filter(Q(generaluser=user) & Q(with_draw=False))
            my_cids = [c.office.id for c in my_office]
            office_list = [c for c in office_list if c.id not in my_cids]
        else:
            q = Q(generaluser=user) & Q(with_draw=False)
            if is_search:
                q = q & (Q(name__icontains=search_key) | Q(admin__name__icontains=search_key))
            my_office = GeneralUserOffice.objects.filter(q)
            if view_kind == "current":
                office_list = [c.office for c in my_office if c.office.status < 4]
            elif view_kind == "withdraw":
                office_list = [c.office for c in my_office if c.office.status == 2]
            elif view_kind == "is_end":
                office_list = [c for c in my_office if c.office.status >= 4]

    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    context = {
        'info': info,
        'view_kind': view_kind,
        'office_list': office_list
    }
    if is_search:
        context["search_key"] = search_key

    return render(request, 'officemanagement/GeneralUser/home.html', context)


def operate_office(request, operate_kind, office_id):
    """
    :param operate_kind:
        select: 选会议室
        withdraw: 撤销会议室
    """
    user = get_user(request, "generaluser")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "generaluser"}))

    if operate_kind not in ["select", "withdraw"]:
        return HttpResponse(ILLEGAL_KIND)
    elif operate_kind == "select":
        office = Office.objects.filter(pk=office_id).get()
        new_office = GeneralUserOffice(generaluser=user, office=office)
        new_office.save()
    elif operate_kind == "withdraw":
        q = Q(office__id=office_id) & Q(generaluser=user) & Q(with_draw=False)
        office = GeneralUserOffice.objects.filter(q).get()
        office.with_draw = True
        office.with_draw_time = timezone.now()
        office.save()

    return redirect(reverse("view_office", kwargs={"view_kind": operate_kind}))
