'''
uni sensor:
- can generate value
- generation +/- value from vector with randomize value
- generate extreme value - random
- coomunicate via mqtt 


another test mqtt: test.mosquitto.org,broker.hivemq.com,iot.eclipse.org.
Used: flespi.io
'''

import random
import time
import paho.mqtt.client as mqtt


class MQTT_comm(object):
    
    
    def __init__ (self, MQQTConfig, HeaderM='booomy'):
        self.HeaderMsg = HeaderM
        self.MQTTServer = MQQTConfig["Server"]
        self.MQTTPort = MQQTConfig["Port"]
        self.MQTTUser = MQQTConfig["User"]
        self.MQTTPasswd = MQQTConfig["Passwd"]
        self.MQTTClientID = "MyMQTTClient2"
        # cls.mqqt_connect()
        pass
    
    # act
    def on_message(self, client, userdata, message):
        '''
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)    
        '''
        print("message received: " ,float(str(message.payload.decode("utf-8"))))
        
        
        
        
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.HeaderMsg+"/#")
        
        
    def mqtt_connect(self):
        self.client = mqtt.Client(client_id=self.MQTTClientID)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.MQTTUser, password=None)
        self.client.connect(self.MQTTServer, self.MQTTPort, 60)        
                
        # self.client.loop_forever()
        pass
    
    def send_data(self,name,data):
        headerMsg=self.HeaderMsg+"/"+name
        self.client.publish(headerMsg, data)


    
# ........................................


# config MQTT client
mqttConfig={}
mqttConfig["Server"]='mqtt.flespi.io'
mqttConfig["Port"]=1883
flespi_token='w0NmcKQuQDDUEObfEjB6AoHalAdJEz80nKdpkRK1ibJLOLQiUgcksHiD5lczI9oV'
mqttConfig["User"]=flespi_token
mqttConfig["Passwd"]=''


# create mqtt connection
MyMQTT = MQTT_comm(mqttConfig)
MyMQTT.mqtt_connect()
MyMQTT.client.loop_forever()



    
    