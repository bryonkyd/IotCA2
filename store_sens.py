import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import sys
import datetime as datetime
import json

host = "ADD IN ENDPOINT API"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("p1828331-PubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

my_rpi.connect()

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    print("Successfully connected to database!")
    
    update = True
    while update:
      try:
         line = ser.readline()
         sensorvalues = line.split()
         tempvalue=sensorvalues[0]
         humidvalue=sensorvalues[1]
         motionvalue=sensorvalues[2]
         print("Temperature value:", tempvalue)
         print("Humidityvalue:", humidvalue)
         print("Motion value:", motionvalue)
         print("Wait 2 secs before getting next values..")
         message = {}
         message["deviceid"] = "deviceid_bryon"
         now = datetime.datetime.now()
         message["datetimeid"] = now.isoformat()
         message["temperature"] = tempvalue
         message["motion"] = motionvalue
         my_rpi.publish("sensors", json.dumps(message), 1)
         sleep(5)
      except KeyboardInterrupt:
         update = False
         cursor.close()
         cnx.close()
      except:
         print("Error while inserting data...")
         print(sys.exc_info()[0])
         print(sys.exc_info()[1])
except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    
