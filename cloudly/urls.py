from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cloudly.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', 'dashboard.views.home', name='home'),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
