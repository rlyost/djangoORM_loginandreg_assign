from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='in'),
    url(r'^logreg/dash$', views.dash, name='dash'),
    url(r'^logreg/add$', views.add, name='addnew'),
    url(r'^logreg/posts_dash$', views.add, name='posts_dash'),
    url(r'^all.json$', views.all_json),
    url(r'^all.html$', views.all_html),
    url(r'^add$', views.add, name='add'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^registration$', views.registration, name='reg'),
    url(r'^login$', views.login, name='login'),
    url(r'^logoff$', views.logoff, name='logoff'),
]