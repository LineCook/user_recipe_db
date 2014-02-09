from django.conf.urls import patterns, url

from linecook import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<user_name>\w+)/$', views.user_detail, name='user_detail'),
	url(r'^(?P<user_name>\w+)/prefs/$', views.user_prefs, name='user_prefs'),
	url(r'^(?P<user_name>\w+)/(?P<recipe_id>\d+)/$', views.recipe_detail, name='recipe_detail'),
	url(r'^(?P<app_id>\d+)/upc/(?P<upc>\w+)$', views.scan, name='scan'),
)
