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


class UniSensor(object):
    # attributes
    Position = 0
    
    def __init__ (self, StartValue=0, MaxValue=100, MinValue=-100, VectorMax=15, VectorExtreme=55, ExtremeFreq=23, Name='UniSensor'):
        # set default value
        self.StartValue = StartValue
        self.MaxValue = MaxValue
        self.MinValue = MinValue
        self.VectorMax = VectorMax
        self.VectorExtreme = VectorExtreme
        self.ExtremeFreq = ExtremeFreq
        self.Value = self.StartValue
        self.ExtremePos = random.randint(1,self.ExtremeFreq)
        self.Name = Name
    
    # actions
    def read_data(self):
        if self.Position==self.ExtremePos:
            ExtremeDirection = random.randrange(-1,2,1)
            self.Value=ExtremeDirection*self.VectorExtreme
            self.ExtremePos = self.Position+random.randint(1,self.ExtremeFreq)
        else:
            #AdditionValue = random.randrange(-self.VectorMax, self.VectorMax)
            AdditionValue = random.triangular(-self.VectorMax, self.VectorMax,0)
            self.Value+=AdditionValue
        self.Value = self.MaxValue if self.Value>self.MaxValue else self.Value
        self.Value = self.MinValue if self.Value<self.MinValue else self.Value
        self.Position+=1
        return self.Value


class MQTT_comm(object):
    
    
    def __init__ (self, MQQTConfig, HeaderM='booomy'):
        self.HeaderMsg = HeaderM
        self.MQTTServer = MQQTConfig["Server"]
        self.MQTTPort = MQQTConfig["Port"]
        self.MQTTUser = MQQTConfig["User"]
        self.MQTTPasswd = MQQTConfig["Passwd"]
        self.MQTTClientID = "MyMQTTClient1"
        # cls.mqqt_connect()
        pass
    
    # act
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")
        
    def mqtt_connect(self):
        self.client = mqtt.Client(client_id=self.MQTTClientID)
        self.client.on_connect = self.on_connect
        #client.on_message = on_message
        
        self.client.username_pw_set(self.MQTTUser, password=None)
        self.client.connect(self.MQTTServer, self.MQTTPort, 60)        
        pass
    
    def send_data(self,name,data):
        headerMsg=self.HeaderMsg+"/"+name
        self.client.publish(headerMsg, data)

    
# ........................................

#create my sensor and generator
Sensor1 = UniSensor()

# config MQTT client
mqttConfig={}
mqttConfig["Server"]='mqtt.flespi.io'
mqttConfig["Port"]=1883
flespi_token='C5mgGM7FtPBRtPM7aOHeHYr1CvDx8uSyq2DUFAqWdRDwwduwR1ymNObd9EB7Zhud'
mqttConfig["User"]=flespi_token
mqttConfig["Passwd"]=''

# create mqtt connection
MyMQTT = MQTT_comm(mqttConfig)
MyMQTT.mqtt_connect()
#MyMQTT.send_data(Sensor1.Name,10)

# generate data
Freq=1
while True:
    payloadS=Sensor1.read_data()
    print(payloadS)
    time.sleep(Freq)
    MyMQTT.send_data(Sensor1.Name,payloadS)
pass



    
    