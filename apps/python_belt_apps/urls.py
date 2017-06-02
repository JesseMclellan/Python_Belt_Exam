from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^logged_in$', views.logged_in),
  url(r'^logout$', views.logging_out)
]
