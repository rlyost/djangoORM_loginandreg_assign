from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='in'),
    url(r'^logreg/dash$', views.dash, name='dash'),
    url(r'^logreg/add$', views.add, name='addnew'),
    url(r'^logreg/wish/(?P<id>\d+)$', views.wish, name='wish'),
    url(r'^addmywish/(?P<id>\d+)$', views.addmywish, name='addmywish'),
    url(r'^add$', views.add, name='add'),
    url(r'^additem$', views.additem, name='additem'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^registration$', views.registration, name='reg'),
    url(r'^login$', views.login, name='login'),
    url(r'^logoff$', views.logoff, name='logoff'),
]