#Define Imports
import mysql.connector
from time import sleep
import sys
import serial
import Adafruit_DHT

#Define Variables
DHTpin = 4

try:
    #Initialise reading from serial monitor
    ser=serial.Serial("/dev/ttyUSB0",9600)
    ser.baudrate=9600
    u='iotuser'
    pw='dmitiot';
    h='localhost'
    db='iotdatabase'
    #Start connection to DB
    cnx = mysql.connector.connect(user=u,password=pw,host=h,database=db) 
    cursor = cnx.cursor()
    print("Successfully connected to database!")
    
    update = True
    while update:
      try:
         sensor_value = ser.readline().split()
         gas_value = sensor_value[0]
         temp_value = sensor_value[1]
         hum_value = sensor_value[2]
         print("Gas value	:", gas_value)
         print("Temp value	:", temp_value)
         print("Humidity value	:", hum_value)
         sql = "INSERT INTO sensor (gas_levels, temperature, humidity) VALUES (%(gas)s, %(temp)s, %(hum)s)"
         #Store data from serial monitor into DB
         cursor.execute(sql, {'gas': gas_value, 'temp': temp_value, 'hum': hum_value })
         cnx.commit()
         print("Wait 3 sec before getting next gas values..")
         sleep(1)
      except mysql.connector.Error as err:
         print(err)
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