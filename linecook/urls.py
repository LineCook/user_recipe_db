from django.conf.urls import patterns, url

from linecook import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
