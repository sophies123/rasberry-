#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import json,os

def jsonWrite(data,tdate,name):
    pathfile = "web/data/"+ name + "/" + tdate +".json"
    if os.path.exists(pathfile):
      file =open(pathfile,"rb+")
      file.seek(-1,os.SEEK_END)
      file.truncate()
      file.write(",")
      json.dump(data,file)
      file.write("]")
      file.close()
    else:
      file =open(pathfile,"w")
      file.write("[")
      json.dump(data,file)
      file.write("]")
      file.close()
timecount = 0
while True:
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 26)
    if humidity is not None and temperature is not None:
        todaytime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        msg =  time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) + '\n' + str(format(temperature,".1f")) + ' C  ' + str(format(humidity,".1f")) + '%'
        i = {"time":time.strftime('%H:%M',time.localtime(time.time())),"tmp":format(temperature,".1f"),"hmt":format(humidity,".1f")}
        jsonWrite(i,todaytime,"min")
        print(msg)
    if(timecount >=60):
        timecount = 0
        jsonWrite(i,todaytime,"hour")
    time.sleep(60)
    timecount = timecount +1
