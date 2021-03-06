from django.conf.urls import patterns, include, url
from authentication.views import hello, lr, nlr
from core.views import feed
import os

media = os.path.join(os.path.dirname(__file__), 'media')

urlpatterns = patterns('',
	(r'^$', nlr(hello)),
	(r'^feed/$', lr(feed)),
	(r'^', include('core.urls')),
    (r'^auth/', include('authentication.urls')),
)

'''

Media URLs will be served by rewriting URL confs for the same. This is however only for development purposes. In production, media will mostly be served via Apache or lighthttpd or a similar server.

'''

urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':media}),
)