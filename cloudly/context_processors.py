# content processor functions

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
    if (request.user.is_anonymous()):
        return {}

    user = request.user
    profile = Profile.objects.get(user=request.user)
    secret = profile.secret

    servers = mongo.servers.find({'secret':profile.secret},{'uuid':1,'name':1}).sort('_id',-1);

    serversNames = {}
    for server in servers:
        serversNames[server['uuid']] = server['name']

    notifs_counter = 0
    active_service_statuses = mongo.active_service_statuses
    active_service_statuses_data = active_service_statuses.find({"$and":[{"secret": secret},{"current_overall_status":{"$ne":"OK"}}]})
    notifs_counter = active_service_statuses_data.count()

    active_notifs = {}
    notifs_types = ["CRITICAL","WARNING","UNKNOWN",]
    for notifs_type in notifs_types:
        active_notifs[notifs_type] = []
        notifs = active_service_statuses.find({"secret":secret,"current_overall_status":notifs_type})
        for notif in notifs:
            newNotif = {}
            newNotif['name'] = serversNames[notif['server_id']]
            newNotif['service'] = notif['service']
            newNotif['date'] = notif['date']
            active_notifs[notifs_type].append(newNotif)

    return {
        'notifs_counter':notifs_counter,
        'active_service_statuses':active_service_statuses_data,
        'navbar_active_notifs':active_notifs,
        'notifs_types':notifs_types,
    }
