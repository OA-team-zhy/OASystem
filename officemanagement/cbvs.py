from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, reverse, redirect

from officemanagement.models import Schedule, GeneralUserOffice
from officemanagement.forms import ScoreForm, RateForm


class ScoreUpdateView(UpdateView):
    model = GeneralUserOffice
    form_class = ScoreForm
    template_name = 'officemanagement/Admin/score.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        title = "给分"
        if request.GET.get("update"):
            title = "修改评价"

        info = {}
        return_url = reverse("office", kwargs={"kind": "admin"})
        if self.object:
            admin = self.object.office.admin
            info = {
                "name": admin.name,
                "kind": "admin",
            }
            return_url = reverse("view_detail", kwargs={"office_id": self.object.office.id})

        return self.render_to_response(self.get_context_data(info=info, title=title, return_url=return_url))

    def get_success_url(self):
        if self.object:
            return reverse("view_detail", kwargs={"office_id": self.object.office.id})
        else:
            return reverse("office", kwargs={"kind": "admin"})


class RateUpdateView(UpdateView):
    model = GeneralUserOffice
    form_class = RateForm
    template_name = 'officemanagement/GeneralUser/rating.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        info = {}
        return_url = reverse("view_office", kwargs={"view_kind": "is_end"})
        if self.object:
            generaluser = self.object.generaluser
            info = {
                "name": generaluser.name,
                "kind": "generaluser",
            }

        return self.render_to_response(self.get_context_data(info=info, return_url=return_url))

    def get_success_url(self):
        return reverse("view_office", kwargs={"view_kind": "is_end"})


class GeneralUserOfficeDetailView(DetailView):
    model = GeneralUserOffice
    template_name = 'offficemanagement/GeneralUser/office.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            context["info"] = {
                "name": self.object.generaluser.name,
                "kind": "generaluser",
            }
        return self.render_to_response(context)
