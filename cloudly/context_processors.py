# content processor functions

import datetime

from django.conf import settings

from django.contrib.auth.models import User
from userprofile.models import Profile

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

if settings.MONGO_USER:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)

mongo = client.cloudly

def incidents_notifs(request):
    
    profile = Profile.objects.get(user=request.user)

    if (not request.user.is_authenticated()):
        return {}

    secret = profile.secret

    servers = mongo.servers.find({'secret':profile.secret},{'uuid':1,'name':1,'last_seen':1}).sort('_id',-1);

    offline_servers = []
    offline_servers_count = 0
    servers_names = {}

    for server in servers:
        servers_names[server['uuid']] = server['name']
        if((datetime.datetime.now()-server['last_seen']).total_seconds()>20):
            offline_servers.append(server)
            offline_servers_count += 1

    notifs_counter = 0
    active_service_statuses = mongo.active_service_statuses
    active_service_statuses_data = active_service_statuses.find({"$and":[{"secret": secret},{"current_overall_status":{"$ne":"OK"}}]})

    active_notifs = {}
    notifs_types = ["CRITICAL","WARNING","UNKNOWN",]

    for notifs_type in notifs_types:

        active_notifs[notifs_type] = []
        notifs = active_service_statuses.find({"secret":secret,"current_overall_status":notifs_type})

        for notif in notifs:

            new_notif = {}
            new_notif['name'] = servers_names[notif['server_id']]
            new_notif['service'] = notif['service']
            try:
                new_notif['date'] = notif['date']
            except: new_notif['date'] = None

            server = mongo.servers.find_one({'uuid':notif['server_id'],})
            if((datetime.datetime.now()-server['last_seen']).total_seconds()<20):
                active_notifs[notifs_type].append(new_notif)
                notifs_counter += 1


    notifs_counter += offline_servers_count


    return {
        'notifs_counter':notifs_counter,
        'active_service_statuses':active_service_statuses_data,
        'navbar_active_notifs':active_notifs,
        'notifs_types':notifs_types,
        'offline_servers':offline_servers,
    }
