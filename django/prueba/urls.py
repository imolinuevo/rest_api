from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'prueba.views.home', name='home'),
    url(r'^auth-jwt/$', 'prueba.views.auth_jwt', name='auth_jwt'),
    url(r'^test-get/$', 'prueba.controllers.use_case_example.test_get', name='test_get'),
    url(r'^test-post/$', 'prueba.controllers.use_case_example.test_post', name='test_post')
)
