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


# config MQTT client
mqttConfig={}
mqttConfig["Server"]='mqtt.flespi.io'
mqttConfig["Port"]=1883
flespi_token='C5mgGM7FtPBRtPM7aOHeHYr1CvDx8uSyq2DUFAqWdRDwwduwR1ymNObd9EB7Zhud'
mqttConfig["User"]=flespi_token
mqttConfig["Passwd"]=''


# config sensor data

# config is bellow close to init class
StartValueSensor=7 
MaxValueSensor=45
MinValueSensor=-18
VectorMaxSensor=5
VectorExtremeSensor=55
ExtremeMinPosSensor=20
ExtremeFreqSensor=0 #30
TrendPlanSensor = {10:-1, 20:1, 30:0.1, 35:-1}
EndTrendBlockSensor = 50
NameSensor='UniSensor1'

# ###############################################

class UniSensor(object):
    # attributes
    Position = 0
    PosIter = 0
    CurrentTrend = 0
    TrendPos = []
    TrendTrend = []
    
    def __init__ (self, StartValue=StartValueSensor, MaxValue=MaxValueSensor, MinValue=MinValueSensor, VectorMax=VectorMaxSensor, VectorExtreme=VectorExtremeSensor, ExtremeFreq=ExtremeFreqSensor, ExtremeMinPos=ExtremeMinPosSensor, Name=NameSensor, TrendPlan=TrendPlanSensor, EndTrendBlock=EndTrendBlockSensor):
        # set default value
        self.StartValue = StartValue
        self.MaxValue = MaxValue
        self.MinValue = MinValue
        self.VectorMax = VectorMax
        self.VectorExtreme = VectorExtreme
        self.ExtremeFreq = ExtremeFreq
        self.ExtremeMinPos = ExtremeMinPos
        self.Value = self.StartValue
        self.ExtremePos = random.randint(self.ExtremeMinPos,self.ExtremeFreq) if self.ExtremeFreq!=0 else 0 #position of extreme value
        self.Name = Name
        self.EndTrendBlock=EndTrendBlock
        self.TrendPlan=TrendPlan
        
        for _tmp1 in self.TrendPlan:
            self.TrendPos.append(_tmp1)
            self.TrendTrend.append(self.TrendPlan[_tmp1])
        
    
    # actions
    def read_data(self):
        
        first_used_trend_pos = 0
        positionCurrentTrendPlan = 0
        _i = 0
        for _tmp1 in self.TrendPos:
            if self.PosIter<_tmp1 and first_used_trend_pos>_tmp1: 
                first_used_trend_pos=_tmp1 # ze jsem v intervalu a mam new hodnotu
                positionCurrentTrendPlan = _i
            if self.PosIter<_tmp1 and first_used_trend_pos==0: 
                first_used_trend_pos=_tmp1 # ze jsem v intervalu a mam new hodnotu
                positionCurrentTrendPlan = _i            
            _i+=1
        
        self.CurrentTrend=self.TrendTrend[positionCurrentTrendPlan]
        
        
        if self.ExtremePos!=0 and self.Position==self.ExtremePos:
            ExtremeDirection = self.CurrentTrend # random.randrange(-1,2,1)
            self.Value=ExtremeDirection*self.VectorExtreme
            self.ExtremePos = self.Position+random.randint(1,self.ExtremeFreq)
        else:
            #AdditionValue = random.randrange(-self.VectorMax, self.VectorMax)
            AdditionValue = random.triangular(0, self.CurrentTrend*self.VectorMax,1/3*self.VectorMax)
            self.Value+=AdditionValue
        
        # oriznuti
        self.Value = self.MaxValue if self.Value>self.MaxValue else self.Value
        self.Value = self.MinValue if self.Value<self.MinValue else self.Value
        self.Position+=1
        
        if self.PosIter==self.EndTrendBlock:
            self.PosIter=0
        else:
            self.PosIter+=1
        
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

StartValueSensor=7 
MaxValueSensor=45
MinValueSensor=-18
VectorMaxSensor=5
VectorExtremeSensor=55
ExtremeMinPosSensor=20
ExtremeFreqSensor=0 #30
TrendPlanSensor = {10:-1, 20:1, 30:0.1, 35:-1}
EndTrendBlockSensor = 50
NameSensor='SensorTemp1'

Sensor1 = UniSensor(StartValueSensor, MaxValueSensor, MinValueSensor, VectorMaxSensor, VectorExtremeSensor, ExtremeFreqSensor, ExtremeMinPosSensor, NameSensor, TrendPlanSensor, EndTrendBlockSensor)

StartValueSensor=0 
MaxValueSensor=60
MinValueSensor=-20
VectorMaxSensor=10
VectorExtremeSensor=55
ExtremeMinPosSensor=20
ExtremeFreqSensor=0 #30
TrendPlanSensor = {10:-0.5, 20:0.5, 30:-0.01, 35:-0.9}
EndTrendBlockSensor = 50
NameSensor='SensorTemp2'

Sensor2 = UniSensor(StartValueSensor, MaxValueSensor, MinValueSensor, VectorMaxSensor, VectorExtremeSensor, ExtremeFreqSensor, ExtremeMinPosSensor, NameSensor, TrendPlanSensor, EndTrendBlockSensor)


# create mqtt connection
MyMQTT = MQTT_comm(mqttConfig)
MyMQTT.mqtt_connect()

# generate data
Freq=1 # count of sec
while True:
    payloadS=Sensor1.read_data() # read data z generatoru :-) 
    print(Sensor1.Name, ":", Sensor1.PosIter, " ... ", Sensor1.CurrentTrend, " ... ", payloadS)
    MyMQTT.send_data(Sensor1.Name,payloadS) # send via MQTT

    payloadS=Sensor2.read_data() # read data z generatoru :-) 
    print(Sensor2.Name, ":", Sensor2.PosIter, " ... ", Sensor2.CurrentTrend, " ... ", payloadS)
    MyMQTT.send_data(Sensor2.Name,payloadS) # send via MQTT

    time.sleep(Freq) # pausa

pass



    
    