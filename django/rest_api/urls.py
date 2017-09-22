from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'rest_api.views.home', name='home'),
    url(r'^auth-jwt/$', 'rest_api.views.auth_jwt', name='auth_jwt'),
    url(r'^test-get/$', 'rest_api.controllers.use_case_example.test_get', name='test_get'),
    url(r'^test-post/$', 'rest_api.controllers.use_case_example.test_post', name='test_post')
)
