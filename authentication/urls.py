from django.conf.urls import patterns,include,url
from views import *

urlpatterns = patterns('',
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', lr(logout_user)),
	(r'^signup/(\w+)$', nlr(signup)),
	(r'^welcome/$', lr(welcome)),
	(r'^facebook/$', nlr(beginFbAuth)),
	(r'^fb/', nlr(facebooksignupsuccess)),
	(r'^setpwd/(\w+)$', nlr(setpassword)),
	(r'^twitter/$', beginTwitterAuth),
	(r'^tw/$', twitterCallback),
	(r'^addtwitter/$', info),
	(r'^setpwd/twitter/(\d+)$', setpwdtwttr),
)