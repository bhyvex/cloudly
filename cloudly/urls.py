from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	# common views
	url(r'^$', 'dashboard.views.home', name='home'),
	url(r'^welcome/$', 'dashboard.views.welcome', name='welcome'),
	url(r'^help/$', 'dashboard.views.help', name='help'),
	url(r'^security/$', 'dashboard.views.security', name='security'),
	# userprofile / account
	url(r'^login/$', 'userprofile.views.auth', name='login'),
	url(r'^register/$', 'userprofile.views.register', name='login'),
	url(r'^logout/$', 'userprofile.views.user_logout', name='logout'),
	url(r'^account/settings/$', 'userprofile.views.account_settings', name='account_settings'),
	# support
	url(r'^support/$', 'support.views.support', name='support'),
	#url(r'^support/new/$', 'support.views.support_add_new', name='support_add_new'),
	#url(r'^support/ticket/(?P<ticket_id>\d+)/$', 'support.views.support_view_ticket', name='support_view_ticket'),
	# invoices
	url(r'^invoices/$', 'invoices.views.invoices', name='invoices'),
	#url(r'^invoice/177212(?P<id>\d+)s/$', 'invoices.views.invoice', name='invoice'),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
