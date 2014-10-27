from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',

	# common views
	url(r'^$', 'dashboard.views.home', name='home'),
	url(r'^welcome/$', 'dashboard.views.welcome', name='welcome'),
	url(r'^help/$', 'dashboard.views.help', name='help'),

	# pricing
	url(r'^pricing/$', 'dashboard.views.pricing', name='pricing'),
	url(r'^pricing/activate/$', 'dashboard.views.activate_pricing_plan', name='activate_pricing_plan'),

	# userprofile / account
	url(r'^login/$', 'userprofile.views.auth', name='login'),
	url(r'^register/$', 'userprofile.views.register', name='login'),
	url(r'^logout/$', 'userprofile.views.user_logout', name='logout'),
	url(r'^account/settings/$', 'userprofile.views.account_settings', name='account_settings'),
	url(r'^account/password/$', 'userprofile.views.change_password', name='change_password'),
	url(r'^cloud/settings/$', 'userprofile.views.cloud_settings', name='cloud_settings'),
	url(r'^cloud/settings/reset/$', 'userprofile.views.reset_cloud_settings', name='reset_cloud_settings'),
	url(r'^cloud/settings/regions/update/$', 'userprofile.views.cloud_settings_update_regions', name='cloud_settings_update_regions'),
	url(r'^cloud/settings/credentials/update/$', 'userprofile.views.cloud_settings_update_credentials', name='cloud_settings_update_credentials'),
	url(r'^lock/$', 'userprofile.views.lock', name='lock'),
	url(r'^goodbye/$', 'userprofile.views.goodbye', name='goodbye'),
	
	# support
	url(r'^support/$', 'support.views.support', name='support'),
	url(r'^support/devel/ticket$', 'support.views.support_devel_ticket', name='support_devel_ticket'),
	url(r'^support/add/new/$', 'support.views.support_add_new', name='support_add_new'),
	#url(r'^support/ticket/(?P<ticket_id>\d+)/$', 'support.views.support_view_ticket', name='support_view_ticket'),

	# invoices
	url(r'^invoices/$', 'invoices.views.invoices', name='invoices'),
	#url(r'^invoice/177212(?P<id>\d+)s/$', 'invoices.views.invoice', name='invoice'),

	# private cloud stuff
	url(r'^private/servers/$', 'private_servers.views.servers', name='servers'),
	url(r'^private/server/(?P<uuid>[\w\-\.]+)/$', 'private_servers.views.server_detail', name='server_detail'),
	url(r'^private/storage/$', 'private_storage.views.private_storage', name='private_storage'),

	# cloud stuff
	url(r'^cloud/software/$', 'cloud_software.views.cloud_software', name='cloud_software'),
	url(r'^cloud/software/add/new/$', 'cloud_software.views.cloud_software_add_new', name='cloud_software_add_new'),
	url(r'^cloud/software/tag/(?P<tag_slug>[\w\-\.]+)/$', 'cloud_software.views.cloud_software_view_tag', name='cloud_software_view_tag'),
	url(r'^cloud/backups/$', 'cloud_backup.views.cloud_backups', name='cloud_backups'),
	url(r'^cloud/storage/$', 'cloud_storage.views.cloud_storage', name='cloud_storage'),
	url(r'^cloud/file/(?P<file_id>\d+)/delete/$', 'cloud_storage.views.delete_file', name='delete_file'),
	url(r'^cloud/sharing/$', 'cloud_storage.views.cloud_sharing', name='cloud_sharing'),
	url(r'^cloud/dropzone/$', 'cloud_storage.views.cloud_dropzone', name='cloud_dropzone'),
	url(r'^cloud/photos/$', 'cloud_photos.views.cloud_photos', name='cloud_photos'),
	url(r'^files_uploader/$', 'cloud_storage.views.dropzone_uploader', name='dropzone_uploader'),
	url(r'^ajax/cloud/storage/$', 'cloud_storage.views.ajax_cloud_storage', name='ajax_cloud_storage'),
	url(r'^ajax/cloud/vms/$', 'cloud_vms.views.ajax_virtual_machines', name='ajax_virtual_machines'),
	url(r'^ajax/cloud/box-template/$', 'cloud_vms.views.ajax_virtual_machines_box', name='ajax_virtual_machines_box'),
	url(r'^ajax/cloud/vms/refresh/$', 'cloud_vms.views.ajax_vms_refresh', name='ajax_vms_refresh'),

	# aws ec2 stuff
	url(r'^aws/(?P<vm_name>[\w\-\.]+)/$', 'cloud_vms.views.aws_vm_view', name='aws_vm_view'),
	url(r'^aws/(?P<vm_name>[\w\-\.]+)/(?P<action>[\w\-\.]+)/$', 'cloud_vms.views.control_aws_vm', name='control_aws_vm'),
	url(r'^aws/(?P<instance_id>[\w\-\.]+)/request/help/$', 'support.views.support_new_aws', name='support_new_aws'),
	url(r'^ajax/aws/(?P<instance_id>[\w\-\.]+)/metrics/$', 'cloud_vms.views.ajax_aws_graphs', name='ajax_aws_graphs'),
	url(r'^ajax/aws/(?P<instance_id>[\w\-\.]+)/metrics/(?P<graph_type>[\w\-\.]+)/$', 'cloud_vms.views.ajax_aws_graphs', name='ajax_aws_graphs'),

	# system logs
	url(r'^logs/$', 'logs.views.logs', name='logs'),

	# admin
	url(r'^admin/$', 'admin.views.admin', name='admin'),
	url(r'^admin/user/(?P<user_id>\d+)/activity/$', 'admin.views.user_activity_report', name='user_activity_report'),
	
	###### devel
	url(r'^devel/$', 'devel.views.devel', name='devel'),	
	url(r'^devel/(?P<dev>[\w\-\.]+)/$', 'devel.views.devel', name='devel'),
	
)


urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT, 'show_indexes': False,
	}),
)
