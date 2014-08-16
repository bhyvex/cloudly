from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$', 'dashboard.views.home', name='home'),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
