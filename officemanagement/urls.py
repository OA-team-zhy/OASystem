from django.urls import path
from officemanagement.views import *

urlpatterns = [
    path('<slug:kind>/', officemanagement_home, name="officemanagement"),
]