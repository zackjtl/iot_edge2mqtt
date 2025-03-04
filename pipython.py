import time
import paho.mqtt.client as mqtt
import ssl
import json
import threading
import random
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a1wtqwg27jb8xg-ats.iot.us-east-1.amazonaws.com", 8883, 60) #Taken from REST API endpoint - Use your own. 



def intrusionDetector(Dummy):

    while (1):   
        rand_val = random.randint(0, 100)
        x=GPIO.input(21)
        if (x==0): 
            print("Just Awesome {}".format(rand_val))
            client.publish("device/data", payload=\
"{{\n\
\t\"deviceId\": \"raspi-3-001\",\n\
\t\"data\": {}\n\
}}\n\
".format(rand_val)\
        , qos=0, retain=False)
        time.sleep(5)

thread = threading.Thread(target=intrusionDetector, args=("Create istrusion Thread",))
thread.start()
    
client.loop_forever()
