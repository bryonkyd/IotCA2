# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from gpiozero import MCP3008, Servo
import json
import random
import RPi.GPIO as GPIO

servo = Servo(26)
servox = Servo(19)
servoy = Servo(13)
RELAY = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setwarnings(False)

# Custom MQTT message callback
def servocustomCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	servo.value = int(message.payload)
	sleep(1)
	servo.value = None
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

def servoXcustomCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	servox.value = int(message.payload)
	sleep(1)
	servox.value = None
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

def servoYcustomCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	servoy.value = int(message.payload)
	sleep(1)
	servoy.value = None
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

def pumpcustomCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	status = str(message.payload)
	if "On" in status:
		print("On")
		GPIO.output(RELAY, GPIO.HIGH)
	else:
		GPIO.output(RELAY, GPIO.LOW)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	
host = "ADD IN ENDPOINT API"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("PubSub-p1828331")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("servo", 1, servocustomCallback)
my_rpi.subscribe("servoX", 1, servoXcustomCallback)
my_rpi.subscribe("servoY", 1, servoYcustomCallback)
my_rpi.subscribe("pump", 1, pumpcustomCallback)

sleep(2)

while True:
	print("listening")
	sleep(5)

sleep(5)

