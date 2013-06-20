from django.conf.urls import patterns,include,url
from views import *

urlpatterns = patterns('',
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_user),
	(r'^signup/(\w+)$', signup),
	(r'^welcome/$', welcome)
)