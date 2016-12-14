from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',

    # common views
    url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^about/$', 'dashboard.views.about', name='about'),
    url(r'^welcome/$', 'dashboard.views.welcome', name='welcome'),
    url(r'^download/agent/$', 'dashboard.views.download_agent', name='download_agent'),


    # userprofile stuff
    url(r'^login/$', 'userprofile.views.auth', name='login'),
    url(r'^register/$', 'userprofile.views.register', name='login'),
    url(r'^logout/$', 'userprofile.views.user_logout', name='logout'),
    url(r'^account/settings/$', 'userprofile.views.account_settings', name='account_settings'),
    url(r'^account/password/$', 'userprofile.views.change_password', name='change_password'),
    #url(r'^cloud/settings/$', 'userprofile.views.cloud_settings', name='cloud_settings'),
    #url(r'^cloud/settings/reset/$', 'userprofile.views.reset_cloud_settings', name='reset_cloud_settings'),
    #url(r'^cloud/settings/regions/update/$', 'userprofile.views.cloud_settings_update_regions', name='cloud_settings_update_regions'),
    #url(r'^cloud/settings/credentials/update/$', 'userprofile.views.cloud_settings_update_credentials', name='cloud_settings_update_credentials'),

    url(r'^demo/$', 'userprofile.views.login_as_demo_user', name='demo'),
    # temp
    url(r'^nigel/$', 'userprofile.views.login_as_demo_user', name='demo'),
    url(r'^kamil/$', 'userprofile.views.login_as_demo_user', name='demo'),

    url(r'^goodbye/$', 'userprofile.views.goodbye', name='goodbye'),

    # admin
    url(r'^admin/$', 'admin.views.admin', name='admin'),
    url(r'^admin/user/(?P<user_id>\d+)/activity/$', 'admin.views.user_activity_report', name='user_activity_report'),

    # credits
    url(r'^credits/$', 'dashboard.views.credits', name='credits'),

    # servers
    url(r'^server/(?P<hwaddr>[\w\-\.]+)/$', 'vms.views.server_view', name='server_view'),

    # aws ec2 servers
    url(r'^aws/(?P<vm_name>[\w\-\.]+)/$', 'vms.views.aws_vm_view', name='aws_vm_view'),
    url(r'^aws/(?P<vm_name>[\w\-\.]+)/(?P<action>[\w\-\.]+)/$', 'vms.views.control_aws_vm', name='control_aws_vm'),

    # servers incidents
    url(r'^incidents/$', 'incidents.views.incidents', name='incidents'),

    # servers logs
    url(r'^logs/$', 'incidents.views.logs', name='logs'),

    # ajax
    url(r'^ajax/session/update/$', 'vms.views.update_session', name='update_session'),
    url(r'^ajax/cloud/vms/$', 'vms.views.ajax_virtual_machines', name='ajax_virtual_machines'),
    url(r'^ajax/cloud/vms/refresh/$', 'vms.views.ajax_vms_refresh', name='ajax_vms_refresh'),
    url(r'^ajax/cloud/box-template/$', 'vms.views.ajax_virtual_machines_box', name='ajax_virtual_machines_box'),
    url(r'^ajax/server/(?P<hwaddr>[\w\-\.]+)/metrics/(?P<graph_type>[\w\-\.]+)/$', 'vms.views.ajax_server_graphs', name='ajax_server_graphs'),
    url(r'^ajax/server/name/update/$', 'vms.views.ajax_update_server_name', name='ajax_update_server_name'),
    #url(r'^ajax/aws/(?P<instance_id>[\w\-\.]+)/metrics/(?P<graph_type>[\w\-\.]+)/$', 'vms.views.ajax_aws_graphs', name='ajax_aws_graphs'),
    url(r'^ajax/incidents/$', 'vms.views.ajax_servers_incidents', name='ajax_servers_incidents'),

    # specials
    url(r'^specials/clean/server/tabs/(?P<return_path>.*)/$', 'vms.views.close_server_tabs', name='close_server_tabs'),

    # devel / temp stuff
    url(r'^web/1/$', 'dashboard.views.web_new_1', name='web_new_1'),
    url(r'^web/2/$', 'dashboard.views.web_new_2', name='web_new_2'),
    url(r'^web/3/$', 'dashboard.views.web_new_3', name='web_new_3'),
    url(r'^web/4/$', 'dashboard.views.web_new_3', name='web_new_4'),
    #url(r'^temp/$', 'dashboard.views.temp', name='temp'),
    url(r'^support/$', 'dashboard.views.support', name='support'),
    url(r'^test/$', 'vms.views.test', name='test'),
)


urlpatterns += patterns('',

    # static and media files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, 'show_indexes': False,
    }),

    # First leg of the authentication journey...
    url(r'^twitter/login/?$', "userprofile.views.begin_twitter_auth", name="twitter_login"),
    url(r'^thanks/$', 'userprofile.views.thanks', name='thanks'),

)
