# -*- coding: utf-8 -*-

import os
import time
import logging
import random
import string
import requests
import unicodedata

import base64
try: import cPickle as pickle
except: import pickle

import datetime
from django.utils import timezone

import json

from pprint import pprint

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity

from amazon import s3_funcs
from amazon import s3_funcs_shortcuts

from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import filesizeformat, upper
from django.contrib.humanize.templatetags.humanize import naturalday
from cloudly.templatetags.cloud_extras import clean_ps_command

from django.conf import settings

from operator import itemgetter, attrgetter, methodcaller

from cloudly.templatetags.cloud_extras import clear_filename, get_file_extension
from vms.models import Cache

import decimal
from django.db.models.base import ModelState

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

if settings.MONGO_USER:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)

mongo = client.cloudly

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def close_server_tabs(request, return_path):

    request.session["recently_clicked_servers"] = []
    request.session.modified = True
    return_path = "/" + return_path

    return HttpResponseRedirect(return_path)


@login_required()
def update_session(request):

    for value in request.POST:
        if(value != 'secret'):
            request.session[value] = request.POST[value]

    request.session.modified = True

    return render_to_response('ajax_null.html', locals())


@login_required()
def aws_vm_view(request,vm_name):

    print '-- aws_vm_view'

    print request.user

    user = request.user
    profile = userprofile.objects.get(user=request.user)
    user.last_login = datetime.datetime.now()
    user.save()

    aws_access_key = profile.aws_access_key
    aws_secret_key = profile.aws_secret_key

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/aws/"+vm_name,"aws_vm_view",ip=ip)

    vms_cache = Cache.objects.get(user=user)
    vm_cache =  vms_cache.vms_response
    vm_cache = base64.b64decode(vm_cache)

    try:
        vm_cache = pickle.loads(vm_cache)[vm_name]
    except:
        return HttpResponse(vm_name)


    ec2_region = vm_cache['instance']['region']['name']

    if(vm_cache['user_id']!=request.user.id):
        return HttpResponse("access denied")


    if(vms_cache.vms_console_output_cache):

        console_output = vms_cache.vms_console_output_cache
    else:

        aws_access_key = profile.aws_access_key
        aws_secret_key = profile.aws_secret_key
        aws_ec2_verified = profile.aws_ec2_verified

        ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
        reservations = ec2conn.get_all_instances(instance_ids=[vm_name,])
        instance = reservations[0].instances[0]

        console_output = instance.get_console_output()
        console_output = console_output.output

        if(not console_output):
            console_output = ""
        vms_cache.vms_console_output_cache = console_output
        vms_cache.save()

    end = datetime.datetime.now()
    start = end - datetime.timedelta(minutes=60)

    ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
    cloudwatch = boto.ec2.cloudwatch.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="NetworkIn")[0]
    networkin_datapoints = metric.query(start, end, 'Average', '')

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="NetworkOut")[0]
    networkout_datapoints = metric.query(start, end, 'Average', '')

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="DiskReadOps")[0]
    disk_readops_datapoints = metric.query(start, end, 'Average', '')

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="DiskWriteOps")[0]
    disk_writeops_datapoints = metric.query(start, end, 'Average', '')

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="DiskReadBytes")[0]
    disk_readbytes_datapoints = metric.query(start, end, 'Average', '')

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':vm_cache['id']}, metric_name="DiskWriteBytes")[0]
    disk_writebytes_datapoints = metric.query(start, end, 'Average', '')

    networkin_datapoints = json.dumps(networkin_datapoints,default=date_handler)
    networkout_datapoints = json.dumps(networkout_datapoints,default=date_handler)
    disk_readops_datapoints = json.dumps(disk_readops_datapoints,default=date_handler)
    disk_writeops_datapoints = json.dumps(disk_writeops_datapoints,default=date_handler)
    disk_readbytes_datapoints = json.dumps(disk_readbytes_datapoints,default=date_handler)
    disk_writebytes_datapoints = json.dumps(disk_writebytes_datapoints,default=date_handler)

    return render_to_response(
        'aws_vm.html',
        {
            'vm_name':vm_name,
            'vm_cache':vm_cache,
            'console_output':console_output,
            'networkin_datapoints':networkin_datapoints,
            'networkout_datapoints':networkout_datapoints,
            'disk_readops_datapoints':disk_readops_datapoints,
            'disk_writeops_datapoints':disk_writeops_datapoints,
            'disk_readbytes_datapoints':disk_readbytes_datapoints,
            'disk_writebytes_datapoints':disk_writebytes_datapoints,
        },
        context_instance=RequestContext(request))


@login_required()
def control_aws_vm(request, vm_name, action):

    print request.user

    user = request.user
    profile = userprofile.objects.get(user=request.user)
    user.last_login = datetime.datetime.now()
    user.save()

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/aws/"+vm_name+"/"+action+"/","control_aws_vm",ip=ip)

    vms_cache = Cache.objects.get(user=user)
    vm_cache =  vms_cache.vms_response
    vm_cache = base64.b64decode(vm_cache)
    vm_cache = pickle.loads(vm_cache)[vm_name]

    if(vm_cache['user_id']!=request.user.id):
        return HttpResponse("access denied")

    aws_access_key = profile.aws_access_key
    aws_secret_key = profile.aws_secret_key
    aws_ec2_verified = profile.aws_ec2_verified

    ec2_region = vm_cache['instance']['region']['name']
    ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    if(action=="reboot"):
        ec2conn.reboot_instances([vm_name,])
    if(action=="start"):
        ec2conn.start_instances([vm_name,])
    if(action=="stop"):
        ec2conn.stop_instances([vm_name,])
    if(action=="terminate"):
        ec2conn.terminate_instances([vm_name,])

    return HttpResponseRedirect("/")


@login_required()
def server_view(request, hwaddr):

    print '-- server_view'
    print request.user

    user = request.user
    profile = userprofile.objects.get(user=request.user)

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/server/"+hwaddr,"server_view",ip=ip)

    hwaddr_orig = hwaddr
    hwaddr = hwaddr.replace('-',':')
    server = mongo.servers.find_one({'secret':profile.secret,'uuid':hwaddr,})
    server['link'] = '/server/'+hwaddr_orig+'/'

    server_status = "Running"
    if((datetime.datetime.now()-server['last_seen']).total_seconds()>20):
        server_status = "Stopped"
        if((datetime.datetime.now()-server['last_seen']).total_seconds()>300):
            server_status = "Offline"

    try:
        uuid = server['uuid']
    except:
        return HttpResponse("access denied")


    networking = False

    params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr.replace(':','-') + '.sys.network'}
    tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
    tsdb_response = json.loads(tsdb.text)

    if(not "error" in tsdb_response and tsdb_response): networking = tsdb_response


    disks = False

    params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr.replace(':','-') + '.sys.disks'}
    tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
    tsdb_response = json.loads(tsdb.text)

    if(not "error" in tsdb_response and tsdb_response): disks = tsdb_response


    mem_usage_ = []
    #mem_usage = mongo.memory_usage.find({'uuid':uuid,}).sort('_id',-1).limit(60)
    #for i in mem_usage: mem_usage_.append(i)
    mem_usage = mem_usage_

    loadavg_ = []
    #loadavg = mongo.loadavg.find({'uuid':uuid,}).sort('_id',-1).limit(60)
    #for i in loadavg: loadavg_.append(i)
    loadavg = loadavg_

    disks = []
    disks_ = server[u'disks_usage']

    for disk in disks_:
        if not disk[5] in disks:
            disks.append(disk[5])


    reduced_disks = []
    for disk in disks:
        if(disk[:4]!="/run" and disk[:5]!="/boot" and disk[:4]!="/sys" and disk[:4]!="/dev"):
            reduced_disks.append(disk)


    historical_service_statuses = mongo.historical_service_statuses
    historical_service_statuses = historical_service_statuses.find({'secret':profile.secret,'server_id':server['uuid'],'type':'status',})

    activity_cummulative_types = []
    for event in historical_service_statuses:
        if not event["service"] in activity_cummulative_types:
            activity_cummulative_types.append(event["service"])

    historical_service_statuses = mongo.historical_service_statuses
    historical_service_statuses = historical_service_statuses.find({'secret':profile.secret,'server_id':server['uuid'],'type':'status',})
    historical_service_statuses = historical_service_statuses.sort("_id",pymongo.DESCENDING)
    historical_service_statuses = historical_service_statuses.limit(20)

    activity = mongo.historical_service_statuses
    activity = activity.find({'secret':profile.secret,'server_id':server['uuid'],'type':'activity',})
    activity = activity.sort("_id",pymongo.DESCENDING)
    activity = activity.limit(20)

    try:
        recently_clicked_servers = request.session["recently_clicked_servers"]
    except:
        recently_clicked_servers = []


    s_ = {'name':server['name'],'hwaddr':hwaddr,'link':'/server/'+hwaddr.replace(':','-')}

    if(not s_ in recently_clicked_servers):

        recently_clicked_servers.append(s_)
    else:

        server_to_delete = [i for i,x in enumerate(recently_clicked_servers) if x == s_]
        del recently_clicked_servers[server_to_delete[0]]
        recently_clicked_servers.append(s_)

    request.session["recently_clicked_servers"] = recently_clicked_servers
    request.session.modified = True

    services_common = mongo.services_tags.find()
    services = []
    for service in services_common:
        services.append(service)

    services_discovered = []
    try:
        server['tags']
    except:
        services_tags = []
        for process in server['processes']:
            for service in services:
                if(service['process'].lower() in process.lower()):
                    if(not [service['tag'],service['description']] in services_tags):
                        services_tags.append([service['tag'],service['description']])
                        try:
                            if(not [service['extra_tag'],""] in services_tags):
                                services_tags.append([service['extra_tag'],""])
                        except:
                            pass

        server['tags'] = {}
        server['tags']['tags'] = services_tags
        server['tags']['datacenters'] = []

        if(server['cpu_virtualization']):
            server['tags']['datacenters'].append(['Metal','Physical Office HW'])
        else:
            pass

        mongo.servers.update({'secret':server['secret'], 'uuid':server['uuid']}, server)


    active_service_statuses = mongo.active_service_statuses
    notifs = active_service_statuses.find({"$and":[{"secret": profile.secret,"server_id":server['uuid']},{"current_overall_status":{"$ne":"OK"}}]})
    server_notifs_count = notifs.count()

    for line in open('agent.py','rt').readlines():
        if('AGENT_VERSION' in line):
            AGENT_VERSION_CURRENT = line.split('"')[1]
            break

    is_outdated_agent_version = False
    if(server['agent_version'] != AGENT_VERSION_CURRENT):
        is_outdated_agent_version = True


    return render_to_response(
        'server_detail.html',
        {
            'request':request,
            'secret':profile.secret,
            'recently_clicked_servers':recently_clicked_servers,
            'hwaddr':hwaddr,
            'hwaddr_orig':hwaddr_orig,
            'server':server,
            'server_status':server_status,
            'disks':disks,
            'reduced_disks':reduced_disks,
            'mem_usage':mem_usage,
            'loadavg':loadavg,
            'disks':disks,
            'networking':networking,
            'historical_service_statuses':historical_service_statuses,
            'activity':activity,
            'activity_cummulative_types':activity_cummulative_types,
            'server_notifs_count':server_notifs_count,
            'is_outdated_agent_version':is_outdated_agent_version,
            'notifs':notifs,
        },
        context_instance=RequestContext(request))


@login_required()
def ajax_servers_incidents(request):
    response = {}

    secret = request.POST['secret']
    servers = mongo.servers.find({'secret':secret},{'uuid':1,'name':1,'last_seen':1}).sort('_id',-1);

    response['offline_servers'] = []
    servers_names = {}
    for server in servers:
        servers_names[server['uuid']] = server['name']
        if((datetime.datetime.now()-server['last_seen']).total_seconds()>300):
            server['_id'] = str(server["_id"])
            server['last_seen'] = server['last_seen'].strftime("%Y-%m-%d %H:%M:%S")
            response['offline_servers'].append(server)

    active_service_statuses = mongo.active_service_statuses

    active_notifs = {}
    notifs_types = ["CRITICAL","WARNING","UNKNOWN",]

    for notifs_type in notifs_types:
        response[notifs_type] = []
        notifs = active_service_statuses.find({"secret":secret,"current_overall_status":notifs_type})
        for notif in notifs:
            notif.update({'name':servers_names[notif['server_id']]})
            notif['_id'] = str(notif['_id'])
            notif['date'] = notif['date'].strftime("%Y-%m-%d %H:%M:%S")
            response[notifs_type].append(notif)

    response = str(response)
    response = response.replace("'",'"')
    response = response.replace('u"','"')

    return HttpResponse(
        response,
        content_type="application/json"
    )

@login_required()
def ajax_update_server_name(request):

    response = {}
    response["success"] = "true"
    response = str(response).replace('u"','"')
    response = response.replace("'",'"')

    server_ = request.POST['server']
    secret = request.POST['secret']
    server_ = server_.replace('-', ':')

    server = mongo.servers.find_one({'secret':secret,'uuid':server_,})

    if request.POST["servername"] == "":
        server['name'] = request.POST['server'].replace("-", ":")
    else:
        server['name'] = request.POST["servername"]

    server = mongo.servers.update({'secret':secret, 'uuid':server_}, server)

    vms_cache = Cache.objects.get(user=request.user)
    vms_cache.delete()


    return HttpResponse(response, content_type="application/json")


@login_required()
def ajax_vms_refresh(request):

    user = request.user
    profile = userprofile.objects.get(user=request.user)

    print 'Refreshing', user, 'VMs cache..'

    aws_access_key = profile.aws_access_key
    aws_secret_key = profile.aws_secret_key
    aws_ec2_verified = profile.aws_ec2_verified

    virtual_machines = {}
    servers = mongo.servers.find({'secret':profile.secret,}).sort('_id',-1)

    vms_cache = Cache.objects.get_or_create(user=user)
    vms_cache = vms_cache[0]
    vms_cache.is_updating = True
    vms_cache.save()

    if(servers.count()):

        print 'servers count', servers.count()

        for server in servers:

            instance_metrics = {}
            instance_metrics['id'] = server['uuid']
            instance_metrics['user_id'] = request.user.id
            instance_metrics['provider'] = 'agent'
            instance_metrics['instance'] = {}
            instance_metrics['instance']['user_id'] = request.user.id
            instance_metrics['instance']['state'] = {}
            instance_metrics['instance']['tags'] = {}

            try:
                instance_metrics["instance"]['tags']['Name'] = server['name']
                #instance_metrics["instance"]['tags']['Name'] = ''.join(x for x in unicodedata.normalize('NFKD', server['hostname']) if x in string.ascii_letters).lower()
            except:
                instance_metrics["instance"]['tags']['Name'] = server['hostname'].replace('.','-').lower()

            if 'tags' in server:
                instance_metrics["instance"]['tags']['tags'] = server['tags']

            uuid = server['uuid']

            if((datetime.datetime.now()-server['last_seen']).total_seconds()>20):
                instance_metrics['instance']['state']['state'] = "Stopped"
                if((datetime.datetime.now()-server['last_seen']).total_seconds()>300):
                    instance_metrics['instance']['state']['state'] = "Offline"
            else:
                instance_metrics['instance']['state']['state'] = "Running"

            cpu_usage_ = ""
            params = {'start':'2m-ago','m':'sum:' + uuid.replace(':','-') + '.sys.cpu'}

            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            tsdb_response = json.loads(tsdb.text)
            try:
                tsdb_response = tsdb_response[0]['dps']
            except:
                tsdb_response = []

            c=0
            for i in tsdb_response:
                cpu_usage_ += str(round(tsdb_response[i],2))
                cpu_usage_ += ","
                if(c==60): break
                c+=1

            cpu_usage = cpu_usage_[:-1]

            cpu_usage_reversed = ""
            cpu_usage_array_reversed = []
            for i in cpu_usage.split(','): cpu_usage_array_reversed.insert(0,i)
            for i in cpu_usage_array_reversed: cpu_usage_reversed += str(i)+","
            cpu_usage_reversed = cpu_usage_reversed[:-1]

            instance_metrics['cpu_utilization_datapoints'] = cpu_usage_reversed
            virtual_machines[server['uuid'].replace(':','-')] = instance_metrics

        #print 'virtual_machines', virtual_machines


    if aws_ec2_verified:

        aws_regions = profile.aws_enabled_regions.split(',')
        print 'AWS regions', aws_regions

        for ec2_region in aws_regions:

            if(ec2_region):

                ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
                cloudwatch = boto.ec2.cloudwatch.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

                try:
                    reservations = ec2conn.get_all_instances()
                except:
                    vms_cache.is_updating = False
                    vms_cache.vms_response = ""
                    vms_cache.save()
                    print vms_cache.is_updating
                    print vms_cache.vms_response
                    #return HttpResponse("access denied")

                instances = [i for r in reservations for i in r.instances]

                for instance in instances:

                    if not instance: continue

                    instance_metrics = {}
                    instance_metrics['instance'] = {}

                    print '** instance', instance.id, instance.private_ip_address

                    volumes = []
                    for volume in ec2conn.get_all_volumes(filters={'attachment.instance-id': instance.id}):
                        volumes.append([volume.id, volume.iops, volume.size,])

                    groups = []
                    for group in instance.__dict__['groups']:
                        groups.append([group.id, group.name,])

                    instance_metrics['id'] = instance.id
                    instance_metrics['user_id'] = request.user.id
                    instance_metrics['provider'] = "aws-ec2"
                    instance_metrics['instance']['placement'] = instance.placement
                    instance_metrics['instance']['user_id'] = request.user.id
                    instance_metrics['instance']['groups'] = groups
                    instance_metrics['instance']['block_device_mapping'] = volumes
                    instance_metrics['instance']['architecture'] = instance.architecture
                    instance_metrics['instance']['client_token'] = instance.client_token
                    instance_metrics['instance']['dns_name'] = instance.dns_name
                    instance_metrics['instance']['private_ip_address'] = instance.private_ip_address
                    instance_metrics['instance']['hypervisor'] = instance.hypervisor
                    instance_metrics['instance']['id'] = instance.id
                    instance_metrics['instance']['image_id'] = instance.image_id
                    instance_metrics['instance']['instance_type'] = instance.instance_type
                    instance_metrics['instance']['ip_address'] = instance.ip_address
                    instance_metrics['instance']['key_name'] = instance.key_name
                    instance_metrics['instance']['launch_time'] = instance.launch_time
                    instance_metrics['instance']['monitored'] = instance.monitored
                    instance_metrics['instance']['persistent'] = instance.persistent
                    instance_metrics['instance']['ramdisk'] = instance.ramdisk
                    instance_metrics['instance']['root_device_name'] = instance.root_device_name
                    instance_metrics['instance']['root_device_type'] = instance.root_device_type
                    instance_metrics['instance']['tags'] = instance.tags
                    instance_metrics['instance']['virtualization_type'] = instance.virtualization_type
                    instance_metrics['instance']['vpc_id'] = instance.vpc_id
                    instance_metrics['instance']['region'] = {"endpoint":instance.region.endpoint,"name":instance.region.name,}
                    instance_metrics['instance']['state'] = {"state":instance.state,"code":instance.state_code,"state_reason":instance.state_reason,}

                    virtual_machines[instance.id] = instance_metrics

                    print 'Updating', request.user, 'cache..'
                    print instance.platform, instance.product_codes

                    try:
                        ec2conn.monitor_instance(str(instance.id))
                    except:
                        print instance.id, 'instance not in a monitorable state!!'.upper()
                        #pprint(instance_metrics)
                        continue


                    # Here is where you define start - end for the Logs...............
                    end = datetime.datetime.now()
                    start = end - datetime.timedelta(minutes=60)

                    # This is how you list all possible values on the response....
                    # print ec2conn.list_metrics()

                    try:
                        metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="CPUUtilization")[0]
                    except: continue

                    cpu_utilization_datapoints = metric.query(start, end, 'Average', 'Percent')

                    instance_metrics['cpu_utilization_datapoints'] = json.dumps(cpu_utilization_datapoints,default=date_handler)
                    virtual_machines[instance.id] = instance_metrics


    vms_cache.vms_response = base64.b64encode(pickle.dumps(virtual_machines, pickle.HIGHEST_PROTOCOL))
    vms_cache.last_seen = datetime.datetime.now()
    vms_cache.is_updating = False
    vms_cache.save()

    print 'VMs cache was succesfully updated.'

    return HttpResponse("ALLDONE")


@login_required()
def ajax_virtual_machines(request):

    print '-- ajax virtual machines'
    print request.user

    user = request.user
    profile = userprofile.objects.get(user=request.user)

    try:
        vms_cache = Cache.objects.get(user=user)
        vm_cache =  vms_cache.vms_response
        vm_cache = base64.b64decode(vm_cache)
    except: vm_cache = {}

    try:
        vm_cache = pickle.loads(vm_cache)
    except: vm_cache = {}


    c=0
    ajax_vms_response = "{"
    for vm in vm_cache:

        if(vm_cache[vm]["instance"]["state"]["state"].lower()!="terminated"):

            data_median = 0
            isotope_filter_classes = " offline linux "

            try:
                data = ""
                cpu_utilization_datapoints = vm_cache[vm]["cpu_utilization_datapoints"]
                cpu_utilization_datapoints = json.loads(cpu_utilization_datapoints)
                z=0
                for i in cpu_utilization_datapoints:
                    data += str(i["Average"])
                    try:
                        data_median += float(i["Average"])
                    except: pass

                    if(len(cpu_utilization_datapoints)-1>z):
                        data += ","
                    #print data
                    z+=1
                try:
                    data_median = data_median/z
                except: data_median = 0
            except:
                try:
                    data = vm_cache[vm]["cpu_utilization_datapoints"]

                    z = 0
                    data_median = 0
                    for i in data.split(','):
                        z+=1
                        data_median += float(i)
                    data_median = data_median/z

                except: data = ""


            try:
                instance_name = vm_cache[vm]["instance"]["tags"]["Name"]
            except:
                instance_name = vm

            print 'instance_name', instance_name

            color = "silver "
            vm_state = vm_cache[vm]["instance"]["state"]["state"].title()

            server_mac_address = vm_cache[vm]['id']
            server_mac_address = str(server_mac_address).replace(':','-')

            active_service_statuses = mongo.active_service_statuses
            notifs = active_service_statuses.find({"$and":[{"secret": profile.secret,"server_id":vm_cache[vm]['id']},{"current_overall_status":{"$ne":"OK"}}]})
            notifs_count = notifs.count()

            if(vm_state=="Running"):

                isotope_filter_classes = " linux "

                try:
                    for tags in vm_cache[vm]["instance"]["tags"]["tags"]:
                        for tag in vm_cache[vm]["instance"]["tags"]["tags"][tags]:
                            isotope_filter_classes += str(tag[0]).replace(".","-") + " "
                except: pass

                if(data_median<17):
                    color = "lightBlue "
                if(data_median>=17 and data_median<=35):
                    color = "green "
                    isotope_filter_classes += " busy"
                if(data_median>35 and data_median<=50):
                    color = "darkGreen "
                    isotope_filter_classes += " busy"
                if(data_median>50 and data_median<=70):
                    color = "lightOrange "
                    isotope_filter_classes += " busy"
                if(data_median>70):
                    isotope_filter_classes += " busy critical"
                    color = "red "
                    if data_median>85:
                        vm_state = "Hot hot hot!"

                if(notifs_count):
                    isotope_filter_classes += " warn"
                if(data_median<85 and notifs_count>2):
                    color = "pink "

            if(vm_state=="Stopping"):
                color = "pink "
            if(vm_state=="Pending"):
                color = "pink "
            if(vm_state=="Shutting-Down"):
                color = "pink "
            if(vm_state=="Stopped"):
                isotope_filter_classes += " offline"

            if(vm_cache[vm]['provider']!='agent'):
                isotope_filter_classes += " cloud"

            ajax_vms_response += "\""
            ajax_vms_response += server_mac_address
            ajax_vms_response += "\": {"

            ajax_vms_response += "\"vmcolor\":\""
            ajax_vms_response += color
            ajax_vms_response += "\","

            ajax_vms_response += "\"vmname\":\""
            ajax_vms_response += instance_name
            if(notifs_count and vm_state=="Running"):
                ajax_vms_response += " <b>" + str(notifs_count) + "</b>"

            ajax_vms_response += "\","

            ajax_vms_response += "\"vmtitle\":\""
            ajax_vms_response += isotope_filter_classes
            ajax_vms_response += "\","

            ajax_vms_response += "\"averge\":\""
            ajax_vms_response += data
            ajax_vms_response += "\","

            ajax_vms_response += "\"state\":\""
            ajax_vms_response += vm_state
            ajax_vms_response += "\","

            ajax_vms_response += "\"link\":\""
            if(vm_cache[vm]['provider']=='agent'):
                ajax_vms_response += "/server/"+vm+"/"
            else:
                ajax_vms_response += "/aws/"+vm+"/"
            ajax_vms_response += "\""

            ajax_vms_response += "},"

        if(c==len(vm_cache)-1):
            ajax_vms_response += "}"

        c+=1

        #print '-_'*80
        #print vm_cache[vm]["instance"]["state"]["state"].title(), vm

    ajax_vms_response = ajax_vms_response.replace(",}","}")
    if(not vm_cache): ajax_vms_response = {}

    print '-'*random.randint(5,40)

    return render_to_response(
        'ajax_virtual_machines.html',
        {
            'user':user,
            'ajax_vms_response':ajax_vms_response,
            'vms_cached_response':vm_cache,
        },
        context_instance=RequestContext(request))


@login_required()
def ajax_aws_graphs(request, instance_id, graph_type="all"):

    print '-- ajax_aws_graphs', request.user

    user = request.user
    profile = userprofile.objects.get(user=request.user)

    vms_cache = Cache.objects.get(user=user)
    vm_cache =  vms_cache.vms_response
    vm_cache = base64.b64decode(vm_cache)

    try:
        vm_cache = pickle.loads(vm_cache)[instance_id]
    except:
        return HttpResponse("XXX " + instance_id)

    if(vm_cache['user_id']!=request.user.id):
        return HttpResponse("access denied")

    aws_access_key = profile.aws_access_key
    aws_secret_key = profile.aws_secret_key
    aws_ec2_verified = profile.aws_ec2_verified

    ec2_region = vm_cache['instance']['region']['name']

    ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
    cloudwatch = boto.ec2.cloudwatch.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    reservations = ec2conn.get_all_instances(instance_ids=[instance_id,])
    instance = reservations[0].instances[0]

    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=10)

    metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance_id}, metric_name="CPUUtilization")[0]
    cpu_utilization_datapoints = metric.query(start, end, 'Average', 'Percent',period=3600)

    return HttpResponse("data " + instance_id + "=" + str(instance) + " ** " + graph_type.upper())

@login_required()
def ajax_server_graphs(request, hwaddr, graph_type=""):

    print '-- ajax_server_graphs, type', graph_type
    print request.user

    graphs_mixed_respose = []

    secret = request.POST['secret']
    uuid = request.POST['server']
    uuid = uuid.replace('-',':')

    server = mongo.servers.find_one({'secret':secret,'uuid':uuid,})

    print 'debug', secret, uuid

    try:
        uuid = server['uuid']
    except:
        return HttpResponse("access denied")


    server_status = "Running"
    if((datetime.datetime.now()-server['last_seen']).total_seconds()>20):
        server_status = "Stopped"
        if((datetime.datetime.now()-server['last_seen']).total_seconds()>300):
            server_status = "Offline"
            print '*'*100
            print 'server is offline'
            print (datetime.datetime.now()-server['last_seen']).total_seconds()


    #activity = mongo.activity.find({'uuid':uuid,}).sort('_id',-1).limit(3)

    if(graph_type=="server_info"):

        graphs_mixed_respose = {}
        graphs_mixed_respose['name'] = server['name']
        graphs_mixed_respose['server_info_hostname'] = server['hostname']
        graphs_mixed_respose['cpu_used'] = server['cpu_usage']['cpu_used']
        graphs_mixed_respose['memory_used'] = server['memory_usage']['memory_used_percentage']
        graphs_mixed_respose['swap_used'] = server['memory_usage']['swap_used_percentage']
        graphs_mixed_respose['loadavg_used'] = server['loadavg'][1]
        graphs_mixed_respose['server_info_uptime'] = server['uptime']
        graphs_mixed_respose['server_info_loadavg'] = server['loadavg']
        graphs_mixed_respose['server_info_status'] = server_status
        graphs_mixed_respose = str(graphs_mixed_respose).replace('u"','"')
        graphs_mixed_respose = graphs_mixed_respose.replace("'",'"')
        graphs_mixed_respose = str(graphs_mixed_respose).replace('u"','"')

        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    if(graph_type=="processes"):

        processes_ = []
        processes = server['processes']

        c=0
        for line in processes:

            if(c>0):

                if not line:break
                line = line.split(' ')

                line_ = []
                for i in line:
                    if i: line_.append(i)
                line = line_

                process_user = line[0]
                process_pid = line[1]
                process_cpu = line[2]
                process_mem = line[3]
                process_vsz = line[4]
                process_rss = line[5]
                process_tty = line[6]
                process_stat = line[7]
                process_start_time = line[8]+'-'+line[9]

                process_command = line[10:]
                process_name = clean_ps_command(process_command[0])
                process_command = ' '.join(str(x) for x in process_command).replace("[", "").replace("]","")
                process_command = process_command.replace('"',"").replace("'",'')


                process = {
                    'pid': process_pid,
                    'cpu': process_cpu+'%',
                    'mem': process_mem+'%',
                    # 'vsz': process_vsz,
                    # 'rss': process_rss,
                    # 'tty': process_tty,
                    # 'stat': process_stat,
                    # 'start_time': process_start_time,
                    'process': process_name,
                    'command': process_command,
                }



                process['user'] = '<span class=\\"label label-success\\">'
                if int(float(process_cpu)) > 50:
                    process['user'] = '<span class=\\"label label-warning\\">'
                if int(float(process_cpu)) > 75:
                    process['user'] = '<span class=\\"label label-danger\\">'

                process['user'] += process_user
                process['user'] += '</span>'

                processes_.append(process)

            c+=1

        processes = {}
        processes['data'] = processes_

        processes = str(processes).replace(" u'"," '").replace("[u'","['").replace("'",'"').replace("\\\\", "\\")


        return HttpResponse(processes, content_type="application/json")


    if(graph_type=="network_connections"):

        network_connections_ = []
        network_connections = server['network_connections']['listen']

        for conn in network_connections:

            connection = {}
            connection['proto'] = conn[1]
            connection['recv-q'] = conn[2]
            connection['send-q'] = conn[3]
            connection['address'] = conn[4]

            if conn[6]:
                connection['port'] = conn[5] + "/" + conn[6]
            else:
                connection['port'] = conn[5]

            network_connections_.append(connection)

        network_connections = {}
        network_connections['data'] = network_connections_

        network_connections = str(network_connections).replace(" u'"," '")
        network_connections = str(network_connections).replace("'",'"')

        return HttpResponse(network_connections, content_type="application/json")


    if(graph_type=="active_network_connections"):

        active_network_connections_ = []
        active_network_connections = server['network_connections']['established']

        for conn in active_network_connections:

            connection = {}
            connection['proto'] = conn[1]
            connection['recv-q'] = conn[2]
            connection['send-q'] = conn[3]
            connection['foreign-address'] = conn[7]
            connection['local-address'] = conn[4]
            connection['foreign-port'] = conn[5]

            active_network_connections_.append(connection)


        active_network_connections = {}
        active_network_connections['data'] = active_network_connections_

        active_network_connections = str(active_network_connections).replace(" u'"," '")
        active_network_connections = str(active_network_connections).replace("'",'"')

        return HttpResponse(active_network_connections, content_type="application/json")


    if(graph_type=="loadavg"):

        params = None
        graph_interval = request.POST['interval']

        graphs_mixed_respose = [[],[],[]]
        loadavg_specific_queries = ['1-min','5-mins','15-mins']

        count = 0
        for i in loadavg_specific_queries:

            if(graph_interval=="3m"):
                params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr + '.sys.loadavg'}
            if(graph_interval=="15m"):
                params = {'start':'15m-ago','m':'avg:15s-avg:' + hwaddr + '.sys.loadavg'}
            if(graph_interval=="1h"):
                params = {'start':'1h-ago','m':'avg:1m-avg:' + hwaddr + '.sys.loadavg'}
            if(graph_interval=="1d"):
                params = {'start':'1d-ago','m':'avg:30m-avg:' + hwaddr + '.sys.loadavg'}
            if(graph_interval=="7d"):
                params = {'start':'7d-ago','m':'avg:3h-avg:' + hwaddr + '.sys.loadavg'}
            if(graph_interval=="30d"):
                params = {'start':'30d-ago','m':'avg:12h-avg:' + hwaddr + '.sys.loadavg'}

            params_ = params
            params_['m'] = params['m'] + "{avg="+i+"}"

            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            params = params_

            tsdb_response = json.loads(tsdb.text)

            try:
                tsdb_response = tsdb_response[0]['dps']
            except: tsdb_response = []

            for i in tsdb_response:
                graphs_mixed_respose[count].append([int(i),round(float(tsdb_response[i]),2)])

            graphs_mixed_respose[count] = sorted(graphs_mixed_respose[count], key=itemgetter(0))
            graphs_mixed_respose[count] = graphs_mixed_respose[count][::-1]
            count += 1

        graphs_mixed_respose = str(graphs_mixed_respose).replace("u'","'")

        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    if(graph_type=="disks"):

        mount_ponit = request.POST['mountPoint']

        graph_interval = request.POST['interval']
        graphs_mixed_respose = []

        if(graph_interval=="3m"):
            params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr + '.sys.disks'}
        if(graph_interval=="15m"):
            params = {'start':'15m-ago','m':'avg:15s-avg:' + hwaddr + '.sys.disks'}
        if(graph_interval=="1h"):
            params = {'start':'1h-ago','m':'avg:1m-avg:' + hwaddr + '.sys.disks'}
        if(graph_interval=="1d"):
            params = {'start':'1d-ago','m':'avg:30m-avg:' + hwaddr + '.sys.disks'}
        if(graph_interval=="7d"):
            params = {'start':'7d-ago','m':'avg:3h-avg:' + hwaddr + '.sys.disks'}
        if(graph_interval=="30d"):
            params = {'start':'30d-ago','m':'avg:12h-avg:' + hwaddr + '.sys.disks'}

        params['m'] += "{mm=disk_used,mount_point="+mount_ponit+"}"


        if(params):
            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            tsdb_response = json.loads(tsdb.text)

            try:
                tsdb_response = tsdb_response[0]['dps']
            except: tsdb_response = []

            for i in tsdb_response:
                graphs_mixed_respose.append([int(i),round(float(tsdb_response[i]),2)])

            graphs_mixed_respose = sorted(graphs_mixed_respose, key=itemgetter(0))
            graphs_mixed_respose = [graphs_mixed_respose[::-1],]

        graphs_mixed_respose = str(graphs_mixed_respose).replace("u'","'")


        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    if(graph_type=="cpu_usage"):

        params = None
        graph_interval = request.POST['interval']
        graphs_mixed_respose = []

        if(graph_interval=="3m"):
            params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr + '.sys.cpu'}
        if(graph_interval=="15m"):
            params = {'start':'15m-ago','m':'avg:15s-avg:' + hwaddr + '.sys.cpu'}
        if(graph_interval=="1h"):
            params = {'start':'1h-ago','m':'avg:1m-avg:' + hwaddr + '.sys.cpu'}
        if(graph_interval=="1d"):
            params = {'start':'1d-ago','m':'avg:30m-avg:' + hwaddr + '.sys.cpu'}
        if(graph_interval=="7d"):
            params = {'start':'7d-ago','m':'avg:3h-avg:' + hwaddr + '.sys.cpu'}
        if(graph_interval=="30d"):
            params = {'start':'30d-ago','m':'avg:12h-avg:' + hwaddr + '.sys.cpu'}

        if(params):

            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            tsdb_response = json.loads(tsdb.text)

            try:
                tsdb_response = tsdb_response[0]['dps']
            except: tsdb_response = []

            for i in tsdb_response:
                graphs_mixed_respose.append([int(i),round(float(tsdb_response[i]),2)])

            graphs_mixed_respose = sorted(graphs_mixed_respose, key=itemgetter(0))
            graphs_mixed_respose = [graphs_mixed_respose[::-1],]

        graphs_mixed_respose = str(graphs_mixed_respose).replace("u'","'")

        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    if(graph_type=="mem_usage" or graph_type=="swap_usage"):

        params = None
        graph_interval = request.POST['interval']
        graphs_mixed_respose = []

        if(graph_interval=="3m"):
            params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr + '.sys.memory'}
        if(graph_interval=="15m"):
            params = {'start':'15m-ago','m':'avg:15s-avg:' + hwaddr + '.sys.memory'}
        if(graph_interval=="1h"):
            params = {'start':'1h-ago','m':'avg:1m-avg:' + hwaddr + '.sys.memory'}
        if(graph_interval=="1d"):
            params = {'start':'1d-ago','m':'avg:30m-avg:' + hwaddr + '.sys.memory'}
        if(graph_interval=="7d"):
            params = {'start':'7d-ago','m':'avg:3h-avg:' + hwaddr + '.sys.memory'}
        if(graph_interval=="30d"):
            params = {'start':'30d-ago','m':'avg:12h-avg:' + hwaddr + '.sys.memory'}

        if(graph_type=="mem_usage"):
            params['m'] += "{mm=memory_used}"

        if(graph_type=="swap_usage"):
            params['m'] += "{mm=swap_used}"

        if(params):
            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            tsdb_response = json.loads(tsdb.text)

            try:
                tsdb_response = tsdb_response[0]['dps']
            except:
                tsdb_response = []

            for i in tsdb_response:
                graphs_mixed_respose.append([int(i),round(float(tsdb_response[i]),2)])

            graphs_mixed_respose = sorted(graphs_mixed_respose, key=itemgetter(0))
            graphs_mixed_respose = [graphs_mixed_respose[::-1],]

        graphs_mixed_respose = str(graphs_mixed_respose).replace("u'","'")

        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    if(graph_type=="network_input_packets" or graph_type=="inbound_traffic" or graph_type=="network_output_packets" or graph_type=="outbound_traffic"):

        params = None
        graph_interval = request.POST['interval']
        graphs_mixed_respose = []

        if(graph_interval=="3m"):
            params = {'start':'3m-ago','m':'avg:3s-avg:' + hwaddr + '.sys.network'}
        if(graph_interval=="15m"):
            params = {'start':'15m-ago','m':'avg:15s-avg:' + hwaddr + '.sys.network'}
        if(graph_interval=="1h"):
            params = {'start':'1h-ago','m':'avg:1m-avg:' + hwaddr + '.sys.network'}
        if(graph_interval=="1d"):
            params = {'start':'1d-ago','m':'avg:30m-avg:' + hwaddr + '.sys.network'}
        if(graph_interval=="7d"):
            params = {'start':'7d-ago','m':'avg:3h-avg:' + hwaddr + '.sys.network'}
        if(graph_interval=="30d"):
            params = {'start':'30d-ago','m':'avg:12h-avg:' + hwaddr + '.sys.network'}

        if(graph_type=="network_input_packets"):
            params['m'] += "{mm=input_accept_packets}"

        if(graph_type=="network_input_bytes"):
            params['m'] += "{mm=input_accept_bytes}"

        if(graph_type=="network_output_packets"):
            params['m'] += "{mm=output_accept_packets}"

        if(graph_type=="network_output_bytes"):
            params['m'] += "{mm=output_accept_bytes}"


        if(params):

            tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
            tsdb_response = json.loads(tsdb.text)

            try:
                tsdb_response = tsdb_response[0]['dps']
            except: tsdb_response = []

            for i in tsdb_response:
                graphs_mixed_respose.append([int(i),round(float(tsdb_response[i]),2)])

            graphs_mixed_respose = sorted(graphs_mixed_respose, key=itemgetter(0))
            graphs_mixed_respose = [graphs_mixed_respose[::-1],]

        graphs_mixed_respose = str(graphs_mixed_respose).replace("u'","'")

        return HttpResponse(graphs_mixed_respose, content_type="application/json")


    return HttpResponse("I'm sorry I don't understand")


def ajax_virtual_machines_box(request):

    return render_to_response('ajax_virtual_machines_box.html', locals(), context_instance=RequestContext(request))


def test(request):

    print '--  devel test:'

    params = {'start':'10m-ago','m':'avg:3s-avg:20-c9-d0-87-8c-5f.sys.network'}
    tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
    sys_network = json.loads(tsdb.text)

    #params = {'start':'10m-ago','m':'avg:3s-avg:30-65-ec-7c-c0-e2.sys.disks'}
    #tsdb = requests.get('http://'+settings.TSDB_HOST+':'+str(settings.TSDB_PORT)+'/api/query',params=params)
    #disks = json.loads(tsdb.text)

    return render_to_response( 'test.html',
        {
            'test':True,
            'sys_network':sys_network,
#            'disks':disks,
        },context_instance=RequestContext(request))
