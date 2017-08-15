from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'prueba.custom_views.home', name='home'),
    url(r'^test-get/$', 'prueba.custom_views.use_case1.test_get', name='test_get'),
    url(r'^test-post/$', 'prueba.custom_views.use_case1.test_post', name='test_post')
)
