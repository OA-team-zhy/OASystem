"""OASystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from defaultAPP.views import home

urlpatterns = [
    path('', home, name="login"),
    path(r'', include("defaultAPP.urls")),
    path(r'PageNavigation/', include("PageNavigation.urls")),
    path(r'notice/', include("notice.urls")),
    path(r'officemanagement/', include("officemanagement.urls")),
    path(r'finance/', include("finance.urls"))
]
