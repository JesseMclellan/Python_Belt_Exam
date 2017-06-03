from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^quo$', views.quo),
  url(r'^post_quote$', views.post_quote),
  url(r'^favorite/(?P<id>\d+)$', views.favorite),
  url(r'^remove/(?P<id>\d+)$', views.remove),
  url(r'^users/(?P<id>\d+)$', views.users),
  url(r'^logout$', views.logging_out)
]
