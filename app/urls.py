from django.conf.urls import patterns, url, include
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^habr/$', views.walk_habr, name='habr'),
    url(r'^build/$', views.build, name='build'),
)
