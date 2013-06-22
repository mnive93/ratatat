from django.conf.urls import patterns, url, include
from authentication.views import lr,nlr
from core.views import *

urlpatterns = patterns('',
	(r'^u/([\w._-]+)', profile),
	(r'^search/', search),
)