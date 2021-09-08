from django.urls import path
from notice import views

urlpatterns = [
    path('^notice/$<slug:kind>/', views.notice_home, name="notice"),
    path(r'^index/$', views.index, name='notice_home'),
    path(r'^article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
    path(r'^article_generaluser/(?P<article_id>[0-9]+)$', views.article_page_generaluser, name='article_page_generaluser'),
    path(r'^article_anyone/(?P<article_id>[0-9]+)$', views.article_page_anyone, name='article_page_anyone'),
    path(r'^edit/(?P<article_id>[0-9]+)$', views.edit_page, name='edit_page'),
    path(r'^change/$', views.change, name='change'),
    path(r'^delete/(?P<article_id>[0-9]+)$', views.delete_page, name='delete_page'),
]