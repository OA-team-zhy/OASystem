from django.urls import path
from officemanagement.views import *
from officemanagement.cbvs import ScoreUpdateView, RateUpdateView, GeneralUserOfficeDetailView


urlpatterns = [
    path('<slug:kind>/', officemanagement_home, name="officemanagement"),
    path('<slug:kind>/', home, name="office"),
    path('Admin/create_office', create_office, name="create_office"),
    path('Admin/view_detail/<int:office_id>', view_detail, name="view_detail"),
    path('Admin/create_schedule/<int:office_id>', create_schedule, name="create_schedule"),
    path('Admin/delete_schedule/<int:schedule_id>', delete_schedule, name="delete_schedule"),
    path('Admin/score/<int:pk>', ScoreUpdateView.as_view(), name="score"),
    path('Admin/handle_office/<int:office_id>/<int:handle_kind>', handle_office, name="handle_office"),

    path('GeneralUser/view/<slug:view_kind>', view_office, name="view_office"),
    path('GeneralUser/operate/<int:office_id>/<slug:operate_kind>', operate_office, name="operate_office"),

    path('GeneralUser/evaluate/<int:pk>', RateUpdateView.as_view(), name="evaluate"),
    path('GeneralUser/view_detail/<int:pk>', GeneralUserOfficeDetailView.as_view(), name="sview_detail"),
]




