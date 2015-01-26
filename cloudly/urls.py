from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	# common views
	url(r'^$', 'dashboard.views.home', name='home'),
	url(r'^welcome/$', 'dashboard.views.welcome', name='welcome'),
	# agent
	url(r'^download/agent/$', 'dashboard.views.download_agent', name='download_agent'),
	# userprofile stuff
	url(r'^login/$', 'userprofile.views.auth', name='login'),
	url(r'^register/$', 'userprofile.views.register', name='login'),
	url(r'^logout/$', 'userprofile.views.user_logout', name='logout'),
	url(r'^account/settings/$', 'userprofile.views.account_settings', name='account_settings'),
	url(r'^account/password/$', 'userprofile.views.change_password', name='change_password'),
	url(r'^cloud/settings/$', 'userprofile.views.cloud_settings', name='cloud_settings'),
	url(r'^cloud/settings/reset/$', 'userprofile.views.reset_cloud_settings', name='reset_cloud_settings'),
	url(r'^cloud/settings/regions/update/$', 'userprofile.views.cloud_settings_update_regions', name='cloud_settings_update_regions'),
	url(r'^cloud/settings/credentials/update/$', 'userprofile.views.cloud_settings_update_credentials', name='cloud_settings_update_credentials'),
	url(r'^goodbye/$', 'userprofile.views.goodbye', name='goodbye'),	
	# private cloud stuff
	url(r'^private/servers/$', 'private_servers.views.servers', name='servers'),
	url(r'^private/server/(?P<uuid>[\w\-\.]+)/$', 'private_servers.views.server_detail', name='server_detail'),
	# ajax
	url(r'^ajax/cloud/vms/$', 'vms.views.ajax_virtual_machines', name='ajax_virtual_machines'),
	url(r'^ajax/cloud/box-template/$', 'vms.views.ajax_virtual_machines_box', name='ajax_virtual_machines_box'),
	url(r'^ajax/cloud/vms/refresh/$', 'vms.views.ajax_vms_refresh', name='ajax_vms_refresh'),
	# aws ec2 stuff
	url(r'^aws/(?P<vm_name>[\w\-\.]+)/$', 'vms.views.aws_vm_view', name='aws_vm_view'),
	url(r'^aws/(?P<vm_name>[\w\-\.]+)/(?P<action>[\w\-\.]+)/$', 'vms.views.control_aws_vm', name='control_aws_vm'),
	url(r'^aws/(?P<instance_id>[\w\-\.]+)/request/help/$', 'support.views.support_new_aws', name='support_new_aws'),
	url(r'^ajax/aws/(?P<instance_id>[\w\-\.]+)/metrics/$', 'vms.views.ajax_aws_graphs', name='ajax_aws_graphs'),
	url(r'^ajax/aws/(?P<instance_id>[\w\-\.]+)/metrics/(?P<graph_type>[\w\-\.]+)/$', 'vms.views.ajax_aws_graphs', name='ajax_aws_graphs'),
	# servers
	url(r'^server/(?P<hwaddr>[\w\-\.]+)/$', 'vms.views.server_view', name='server_view'),
	# incidents
	url(r'^incidents/$', 'incidents.views.incidents', name='incidents'),
	# admin
	url(r'^admin/$', 'admin.views.admin', name='admin'),
	url(r'^admin/user/(?P<user_id>\d+)/activity/$', 'admin.views.user_activity_report', name='user_activity_report'),	
)


urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT, 'show_indexes': False,
	}),
)
