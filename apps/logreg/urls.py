from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='in'),
    url(r'^logreg/success$', views.success, name='usuccess'),
    url(r'^registration$', views.registration, name='reg'),
    url(r'^login$', views.login, name='log'),
]