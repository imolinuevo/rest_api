from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'prueba.views.home', name='home'),
    url(r'^test-get/$', 'prueba.views.test_get', name='test_get'),
    url(r'^test-post/$', 'prueba.views.test_post', name='test_post')
)
