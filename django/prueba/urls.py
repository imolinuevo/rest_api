from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'prueba.views.home', name='home'),
    url(r'^aptest/$', 'prueba.views.aptest', name='aptest')
)
