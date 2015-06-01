#!flask/bin/python

import os
import sys
import socket
import time, datetime

from flask import Flask, jsonify, abort
from flask import render_template, request, url_for

app = Flask(__name__)

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly

@app.route('/test/', methods = ['GET'])
def test():
	return jsonify( { 'test': True } )


@app.route('/v10/activity/', methods = ['POST'])
def activity():

	data = request.json
	
	activity_log = {
		'secret': data['secret'],
		'uuid': data['uuid'],
		'agent_version': data['agent_version'],
		'activity': data['activity'],
		'date_created': datetime.datetime.utcnow(),
	}
	activity_ = mongo.activity
	activity_.insert( activity_log )

	return jsonify( { 'test': True } )


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
	agent_version = data['agent_version']
	last_seen = datetime.datetime.utcnow()
	hostname = data['hostname']
	distro = data['distro']
	networking = data['networking']
	
	processes = data['processes']
	processes = processes.replace('\t',' ')
	processes = processes.replace('  ',' ')
	processes = processes.split('\n')

	server = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'ip': ip,
		'ip_remote': ip_remote,
		'hostname': hostname,
		'distro': distro,
		'processes': processes,
		'loadavg': loadavg,
		'uptime': uptime,
		'cpu_usage': cpu_usage,
		'cpu_info': cpu_info,
		'cpu_virtualization': cpu_virtualization,
		'memory_usage': memory_usage,
		'disks_usage': disks_usage,
		'last_seen': last_seen,
	}

	print ' API query from agent version', str(agent_version), uuid, 'IP', ip_remote+'/'+ ip, 'uptime '+uptime+''

	servers = mongo.servers
	server_ = servers.find_one({'secret':secret, 'uuid':uuid,})

	if(server_): 
		server_ = servers.update({'secret':secret, 'uuid':uuid}, server)
	else:
		servers.insert(server)

	
	cpu_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'cpu_usage': cpu_usage,
		'date_created': datetime.datetime.utcnow(),
	}
	cpu_usage_ = mongo.cpu_usage
	cpu_usage_.insert( cpu_usage_metrics )

	cpu_usage_tsdb_cmd = "put " + \
		uuid.replace(':','-') + ".sys.cpu " + \
		str(int(time.time())) + " " + \
		str(cpu_usage['cpu_used']) + \
		" cpu=0" + \
		"\n"
	
	hbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hbase.connect(("hbase", 4242))
	hbase.send(cpu_usage_tsdb_cmd)
	hbase.close()
	
		
	loadavg_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'loadavg': loadavg,
		'date_created': datetime.datetime.utcnow(),
	}
	loadavg_ = mongo.loadavg
	loadavg_.insert( loadavg_metrics )

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
	hbase.connect(("hbase", 4242))
	hbase.send(loadavg_tsdb_cmd)
	hbase.close()



	memory_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'memory_usage': memory_usage,
		'date_created': datetime.datetime.utcnow(),
	}
	memory_usage_ = mongo.memory_usage
	memory_usage_.insert( memory_usage_metrics )

	disks_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'disks_usage': disks_usage,
		'date_created': datetime.datetime.utcnow(),
	}
	disks_usage_ = mongo.disks_usage
	disks_usage_.insert( disks_usage_metrics )

	networking_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'input_accept_packets': networking['input_accept_packets'],
		'input_accept_bytes': networking['input_accept_bytes'],
		'output_accept_packets': networking['output_accept_packets'],
		'output_accept_bytes': networking['output_accept_bytes'],
		'date_created': datetime.datetime.utcnow(),
	}
	networking_ = mongo.networking
	networking_.insert( networking_metrics )

	return ("thanks", 201)



if __name__ == '__main__':
	app.run(
		debug = True,
		host = "0.0.0.0",
		port = 5001
	)
