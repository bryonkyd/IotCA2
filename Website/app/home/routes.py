# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
#Imports
from app.home import blueprint
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from flask import render_template, redirect, url_for, request, jsonify, Response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import json
import numpy
import datetime
from decimal import Decimal
import sys
import time
import threading
import boto3
from boto3.dynamodb.conditions import Key, Attr

#Define Variables
session = boto3.Session()
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
session_token = credentials.token

host = "aw3nvob3lstxq-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("PubSub-p1828290")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(20)  # 10 sec
my_rpi.configureMQTTOperationTimeout(20)  # 5 sec
my_rpi.connect()

#Define Classes
#Class for Dashboard
class GenericEncoder(json.JSONEncoder):
    
    def default(self, obj):  
        if isinstance(obj, numpy.generic):
            return numpy.asscalar(obj) 
        elif isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 

#Define Functions
#Functions for converting data into json format 
class GenericEncoder(json.JSONEncoder):
    def default(self, obj):  
        if isinstance(obj, numpy.generic):
            return numpy.asscalar(obj)
        elif isinstance(obj, Decimal):
            return str(obj) 
        elif isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        elif isinstance(obj, Decimal):
            return float(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 

def data_to_json(data):
    json_data = json.dumps(data,cls=GenericEncoder)
    return json_data

#Function for retrieving data from dynamodb
def get_data_from_dynamodb(n):
    try:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('iot-sensor')
            response = table.query(
                KeyConditionExpression=Key('deviceid').eq('deviceid_bryon'),
                ScanIndexForward=False
            )
            items = response['Items']
            data = items[:n]
            data_reversed = data[::-1]
            return data_reversed
    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

#Define Blueprint Routes
@blueprint.route('/index')
@login_required
def index():
    datetimeid = datetime.datetime.now().isoformat() 
    return render_template('index.html', segment='index', datetime=datetimeid)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'
        # Detect the current page
        segment = get_segment( request )
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment    
    except:
        return None  

@blueprint.route("/api/getdata",methods = ['POST', 'GET'])
def apidata_getdata():
    if request.method == 'POST':
        try:
            data = {'chart_data': data_to_json(get_data_from_dynamodb(10)), 
             'title': "IOT Data"}
            print(data)
            return jsonify(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return None

@blueprint.route("/writePump/<status>")
def checkPump(status):
	out = ""
	if status == "On":
		out = "The Pump is On"
		my_rpi.publish("pump", status, 1)
	else:
		out = "The Pump is Off"
		my_rpi.publish("pump", status, 1)
	return out

@blueprint.route("/writeServo/<status>")
def checkServo(status):
    out = ""
    if status == "On":
        message = {}
        out = "The Servo is On"
        my_rpi.publish("servo", "-1", 1)
        now = datetime.datetime.now()
        message['fed_time'] = now.isoformat() 
        my_rpi.publish("feed", json.dumps(message), 1)
    else:
        out = "The Servo is Off"
        my_rpi.publish("servo", "0", 1)
    return out

@blueprint.route("/streamServo/<status>")
def moveServo(status):
    out = ""
    if status == "Up":
        my_rpi.publish("servoY", "1", 1)
    elif status == "Left":
        my_rpi.publish("servoX", "1", 1)
    elif status == "Center":
        my_rpi.publish("servoX", "0", 1)
        my_rpi.publish("servoY", "0", 1)
    elif status == "Right":
        my_rpi.publish("servoX", "-1", 1)
    elif status == "Down":
        my_rpi.publish("servoY", "-1", 1)
    return out

@blueprint.route("/camera")
def cameraModule():
	global access_key,secret_key,session_token
	print(access_key,secret_key,session_token)
	return render_template("camera.html", akey=access_key, skey=secret_key, stoken=session_token)
	
