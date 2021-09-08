from django.urls import path
from finance.views import *

urlpatterns = [
    path('<slug:kind>/', finance_home, name="finance"),
]