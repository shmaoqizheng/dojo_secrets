from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^secrets$', views.secrets),
	url(r'^add$',views.add),
	url(r'^like/(?P<id>\d+)$', views.like),
	url(r'^delete/(?P<id>\d+)$', views.delete),
	url(r'^popular$', views.popular)
]
