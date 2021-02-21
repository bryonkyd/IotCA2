# Home Pet Feeder
IotCA2 Repo for Dextor and Bryon. Team DB

![alt text](https://github.com/Zerolegacy/IotCA2/blob/main/Picture1.png?raw=true)

Quick Start Guide:

1)	First connect hardware as in Section 2 of the step by step tutorial.
2)	Install all dependencies as in Section 3 of the step by step tutorial.
3)	For Alexa and Live Stream, one of the RaspberryPis has to be Version 10 and the appropriate setting up is required.
4)	Git clone https://github.com/Zerolegacy/IotCA2
5)	Transfer the website folder to your ec2 instance
6)	Install dependencies by running apt-get install -r requirements.txt
7)	Update the aws credentials in ~/.aws/credentials in ec2 and both RaspberryPi
8)	Then run the run.py file for the web server. Run.py can be found in the website folder
9)	Transfer the RaspberryPi folder to your RaspberryPi(non-Version 10).
10)	Update certificate.pem.crt, private.pem.key, public.pem.key, rootca.pem in website folder with your own certs and details. 
11)	Update certificate.pem.crt, private.pem.key, public.pem.key, rootca.pem in RaspberryPi folder with your own certs and details. 
12)	Update your Endpoint API link inside store_sens.py, text_rekognition.py and pubsub.py.
13)	Run python3 store_sens.py to start getting values from the sensors to the pi.
14)	Run python checkbowl.py to start monitor if the foodbowl is empty.
15)	Run python pubsub.py to start listening to topics with MQTT for actuator commands.
16)	Install Amazon Kinesis following https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp
17)	Create a credential file with the format “CREDENTIALS <aws_access_key> <session to end> <aws_secret_access_key> <aws_session_token>”
18)	In the other RaspberryPi (Version 10), run the following command for livestream to start:

gst-launch-1/0 v412src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! Video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! Kvssink stream-name=”<stream name>” credential-path=”<credentials file path from step 16>” aws-region=”us-east-1

19)	Integrate Alexa using the docummentations from the following: https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi.html
20)	In the other RaspberryPi (Version 10), run the following command for Alexa to start:

cd /home/pi/sdk-folder/sdk-build PA_ALSA_PLUGHW=1 ./SampleApp/src/SampleApp ./Integration/AlexaClientSDKConfig.json ../third-party/alexa-rpi/models

