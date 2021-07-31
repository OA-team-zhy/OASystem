from django.views.generic import CreateView

from defaultAPP.models import GeneralUser


class CreatCheckView(CreateView):
    model = GeneralUser
