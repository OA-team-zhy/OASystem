from django.urls import path
from PageNavigation.views import *

urlpatterns = [
    path('<slug:kind>/', home, name="PageNavigation"),
]