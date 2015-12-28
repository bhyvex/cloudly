#!flask/bin/python

import os
import sys
import socket
from pprint import pprint
import time, datetime

import django
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudly.settings")
django.setup()

from flask import Flask, jsonify, abort
from flask import render_template, request, url_for

app = Flask(__name__)

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

try:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)
except: pass

mongo = client.cloudly

for line in open('agent.py','rt').readlines():
    if('AGENT_VERSION' in line):
        AGENT_VERSION_CURRENT = line.split('"')[1]
        break


def _file_alert():
    return False

def _fire_notification():
    return False


@app.route('/test/', methods = ['GET'])
def test():
    return jsonify( { 'test': True } )


@app.route('/v10/activity/', methods = ['POST'])
def activity():

    data = request.json

    try:
        activity_log = {
            'secret': data['secret'],
            'server_id': data['server_id'],
            'activity_type': data['activity_type'],
            'data': data['data'],
            'date_created': datetime.datetime.now(),
        }
        activity_ = mongo.activity
        activity_.insert( activity_log )

        activity_log["type"] = "activity"
        historical_service_statuses = mongo.historical_service_statuses
        historical_service_statuses.insert(activity_log)

    except:
        return ("update", 201)

    return jsonify( { 'activity': True } )


@app.route('/v10/ping/', methods=['POST'])
def ping():

    data = request.json

    if not request.headers.getlist("X-Forwarded-For"):
        ip_remote = request.remote_addr
    else:
        ip_remote = request.headers.getlist("X-Forwarded-For")[0]

    uuid = data['uuid']
    ip = data['ip']
    ip_remote = ip_remote
    secret = data['secret']
    loadavg = data['loadavg']
    uptime = data['uptime']
    cpu_usage = data['cpu_usage']
    cpu_info = data['cpu_info']
    cpu_virtualization = data['cpu_virtualization']
    memory_usage = data['memory_usage']
    disks_usage = data['disks_usage']
    last_seen = datetime.datetime.now()
    hostname = data['hostname']
    distro = data['distro']
    networking = data['networking']
    network_connections = data['network_connections']
    agent_version = data['agent_version']

    processes = data['processes']
    processes = processes.replace('\t',' ')
    processes = processes.replace('  ',' ')
    processes = processes.split('\n')

    try:
        server = {
            'secret': secret,
            'agent_version': agent_version,
            'uuid': uuid,
            'ip': ip,
            'ip_remote': ip_remote,
            'hostname': hostname,
            'distro': distro,
            'processes': processes,
            'loadavg': loadavg['loadavg'],
            'uptime': uptime,
            'cpu_usage': cpu_usage['cpu_usage'],
            'cpu_info': cpu_info,
            'cpu_virtualization': cpu_virtualization,
            'memory_usage': memory_usage['memory_usage'],
            'disks_usage': disks_usage['disks_usage'],
            'last_seen': last_seen,
            'network_connections': network_connections,
        }
    except:
        error = "ERROR - outdated monitor agent!"
        print error
        return (error, 401)

    print 'API query from agent version', str(agent_version), uuid, 'IP', ip_remote+'/'+ ip, 'uptime '+uptime


    servers = mongo.servers
    server_ = servers.find_one({'secret':secret, 'uuid':uuid,})

    try:
        server['name'] = server_['name']
    except:
        server['name'] = hostname.replace(':','-')


    try:
        server['tags'] = server_['tags']
    except: pass

    if(server_):
        server_ = servers.update({'secret':secret, 'uuid':uuid}, server)
    else:
        servers.insert(server)


    cpu_usage_metrics = {
        'secret': secret,
        'agent_version': agent_version,
        'uuid': uuid,
        'cpu_usage': cpu_usage['cpu_usage'],
        'date_created': datetime.datetime.now(),
    }
    cpu_usage_service_report = cpu_usage['service_report']
    cpu_usage = cpu_usage['cpu_usage']

    cpu_usage_tsdb_cmd = "put " + \
        uuid.replace(':','-') + ".sys.cpu " + \
        str(int(time.time())) + " " + \
        str(cpu_usage['cpu_used']) + \
        " cpu=0" + \
        "\n"

    hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hbase.connect((settings.TSDB_HOST, settings.TSDB_PORT))
    hbase.send(cpu_usage_tsdb_cmd)
    hbase.close()

    loadavg_metrics = {
        'secret': secret,
        'agent_version': agent_version,
        'uuid': uuid,
        'loadavg': loadavg['loadavg'],
        'date_created': datetime.datetime.now(),
    }
    loadavg_service_report = loadavg['service_report']
    loadavg = loadavg['loadavg']

    loadavg_tsdb_cmd = "put " + \
        uuid.replace(':','-') + ".sys.loadavg " + \
        str(int(time.time())) + " " + \
        str(loadavg[0]) + \
        " avg=1-min" + \
        "\n"
    loadavg_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.loadavg " + \
        str(int(time.time())) + " " + \
        str(loadavg[1]) + \
        " avg=5-mins" + \
        "\n"
    loadavg_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.loadavg " + \
        str(int(time.time())) + " " + \
        str(loadavg[2]) + \
        " avg=15-mins" + \
        "\n"

    hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hbase.connect((settings.TSDB_HOST, settings.TSDB_PORT))
    hbase.send(loadavg_tsdb_cmd)
    hbase.close()


    memory_usage_metrics = {
        'secret': secret,
        'agent_version': agent_version,
        'uuid': uuid,
        'memory_usage': memory_usage['memory_usage'],
        'date_created': datetime.datetime.now(),
    }
    memory_usage_service_report = memory_usage['service_report']
    memory_usage = memory_usage['memory_usage']

    memory_tsdb_cmd = "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['memory_used']) + \
        " mm=memory_used" + \
        "\n"
    memory_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['swap_used']) + \
        " mm=swap_used" + \
        "\n"
    memory_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['memory_free']) + \
        " mm=memory_free" + \
        "\n"
    memory_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['swap_free']) + \
        " mm=swap_free" + \
        "\n"
    memory_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['memory_total']) + \
        " mm=memory_total" + \
        "\n"
    memory_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.memory " + \
        str(int(time.time())) + " " + \
        str(memory_usage['swap_total']) + \
        " mm=swap_total" + \
        "\n"

    hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hbase.connect((settings.TSDB_HOST, settings.TSDB_PORT))
    hbase.send(memory_tsdb_cmd)
    hbase.close()


    networking_metrics = {
        'secret': secret,
        'agent_version': agent_version,
        'uuid': uuid,
        'input_accept_packets': networking['input_accept_packets'],
        'input_accept_bytes': networking['input_accept_bytes'],
        'output_accept_packets': networking['output_accept_packets'],
        'output_accept_bytes': networking['output_accept_bytes'],
        'date_created': datetime.datetime.now(),
    }

    networking_tsdb_cmd = "put " + \
        uuid.replace(':','-') + ".sys.network " + \
        str(int(time.time())) + " " + \
        str(networking['input_accept_packets']) + \
        " mm=input_accept_packets" + \
        "\n"
    networking_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.network " + \
        str(int(time.time())) + " " + \
        str(networking['input_accept_bytes']) + \
        " mm=input_accept_bytes" + \
        "\n"
    networking_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.network " + \
        str(int(time.time())) + " " + \
        str(networking['output_accept_packets']) + \
        " mm=output_accept_packets" + \
        "\n"
    networking_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.network " + \
        str(int(time.time())) + " " + \
        str(networking['output_accept_bytes']) + \
        " mm=output_accept_bytes" + \
        "\n"

    hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hbase.connect((settings.TSDB_HOST, settings.TSDB_PORT))
    hbase.send(networking_tsdb_cmd)
    hbase.close()


    disks_usage_metrics = {
        'secret': secret,
        'agent_version': agent_version,
        'uuid': uuid,
        'disks_usage': disks_usage['disks_usage'],
        'date_created': datetime.datetime.now(),
    }
    disks_usage_service_report = disks_usage['service_report']
    disks_usage = disks_usage['disks_usage']


    for disk in disks_usage:

        mount_point = disk[5]
        disk_free = disk[3]
        disk_used = disk[2]
        disk_total = disk[1]
        disk_usage = disk[4]

        disks_tsdb_cmd = "put " + \
        uuid.replace(':','-') + ".sys.disks " + \
        str(int(time.time())) + " " + \
        str(disk_free) + \
        " mount_point=" + mount_point + \
        " mm=disk_free" + \
        "\n"
        disks_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.disks " + \
        str(int(time.time())) + " " + \
        str(disk_used) + \
        " mount_point=" + mount_point + \
        " mm=disk_used" + \
        "\n"
        disks_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.disks " + \
        str(int(time.time())) + " " + \
        str(disk_total) + \
        " mount_point=" + mount_point + \
        " mm=disk_total" + \
        "\n"
        disks_tsdb_cmd += "put " + \
        uuid.replace(':','-') + ".sys.disks " + \
        str(int(time.time())) + " " + \
        str(disk_usage) + \
        " mount_point=" + mount_point + \
        " mm=disk_usage" + \
        "\n"

        hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hbase.connect((settings.TSDB_HOST, settings.TSDB_PORT))
        hbase.send(disks_tsdb_cmd)
        hbase.close()


    service_statuses__to_process = [ \
        cpu_usage_service_report,
        loadavg_service_report,
        memory_usage_service_report,
        disks_usage_service_report,
    ]

    active_service_statuses = mongo.active_service_statuses
    historical_service_statuses = mongo.historical_service_statuses
    alertor_queue = mongo.alertor_queue


    for status_report in service_statuses__to_process:

        server_id = uuid
        detailed_service_status = status_report['service_status']
        service = detailed_service_status['service'].upper()
        current_overall_service_status = detailed_service_status['status'].upper()
        service_thresholds = status_report['service_thresholds']


        # Active Service Statuses...
        last_active_service_status = active_service_statuses.find_one({'server_id':uuid,'service':service})

        new_active_report = {
            'secret':secret,
            'server_id':uuid,
            'type':"status",
            'service':service,
            'current_overall_status':current_overall_service_status,
            'detailed_service_status':detailed_service_status,
        }

        if(not last_active_service_status):

            new_active_report['date'] = datetime.datetime.now()
            active_service_statuses.insert(new_active_report)
            historical_service_statuses.insert(new_active_report)

        else:
            if (not 'date' in last_active_service_status):
                new_active_report['date'] = datetime.datetime.now()

            active_service_statuses.update({'server_id':uuid,'service':service},{"$set":new_active_report})

            if( last_active_service_status['current_overall_status'] == current_overall_service_status ):

                print service, last_active_service_status['current_overall_status'], '=', current_overall_service_status, 'doing nothing...'
                continue


            try:
                min_alert_duration = service_thresholds[current_overall_service_status]['min_duration_in_seconds']
            except: min_alert_duration = 30


            try:
                current_alert_duration = (datetime.datetime.now()-last_active_service_status['date']).total_seconds()
            except:
                current_alert_duration = 0

            print '**', service, last_active_service_status['current_overall_status'], '--> (currently)', current_overall_service_status
            print '** current_alert_duration', current_alert_duration, 'min_alert_duration', min_alert_duration


            if( current_alert_duration > min_alert_duration):

                active_service_statuses.update({'server_id':uuid,'service':service}, new_active_report)

                new_active_report['date'] = datetime.datetime.now()
                new_active_report['agent_version'] = agent_version
                historical_service_statuses.insert(new_active_report)
                alertor_queue.insert(new_active_report)

            else:
                print 'waiting for the threshold to be reached....'

        print '*'*100


    if(agent_version != AGENT_VERSION_CURRENT):

        return ("update", 201)


    print '- all done','-'*100

    return ("thanks", 201)



if __name__ == '__main__':
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = 5001
    )
