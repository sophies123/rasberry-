#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import json,os
import smtplib  
import string
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# timecount = 0 时间标志设置为0

while True:
    sensor = Adafruit_DHT.DHT11 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 26)  #利用 Adafruit_DHT读取DHT11得温度和湿度

    # 邮箱设置
    HOST = "smtp.163.com" #定义smtp主机
    SUBJECT = "test" #定义邮件主题
    TO = "827507534@qq.com" #定义邮件收件人
    FROM = "zh827507534@163.com" #定义邮件发件人
    BODY=string.join(( #组装sendmail方法的邮件主体内容，各段以"\r\n"进行分隔
    "From:%s" %FROM,
    "To:%s" %TO,
    "Subject:%s"%SUBJECT,
    "",
    "\n当前温度： " + str(temperature) + "°C\n当前湿度： " + str(humidity) + " %\n\n天气变化,\n注意感冒"
    "text",
    ),"\r\n")

    # 向网页端显示温湿度
    if humidity is not None and temperature is not None:
        todaytime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        msg =  time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) + '\n' + str(temperature) + ' C  ' + str(humidity) + '%'
        i = {"time":time.strftime('%H:%M',time.localtime(time.time())),"tmp":temperature,"hmt":humidity}
        jsonWrite(i,todaytime,"min") #向网页写入时间和温湿度
        print(msg) #输出当前温度

    # 判断温度发送邮件报警

    if (int (sring(temperature))>=35 and int (sring(temperature))<=10):
      server = smtplib.SMTP() #创建一个SMTP对象
      server.connect(HOST,"25") #通过connect方法连接smtp主机
      server.starttls() #启动安全传输模式
      server.login("zh827507534@163.com","zh1997163") #邮件账户登录校验
      server.sendmail(FROM,TO,BODY) #邮件发送
      server.quit() #断开smtp连接
      pass

    # 时间判断每一分钟检测一次状态
    if(timecount >=60):
        timecount = 0
        jsonWrite(i,todaytime,"hour")
    time.sleep(60)
timecount = timecount +1
