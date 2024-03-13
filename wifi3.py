import network
import time
import socket
import led
import gc
import os
from machine import Pin,UART
from time import sleep

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)


ssid = "Inetcom_265"
pw = "THfu87K*MHiCbG2%Nqn0eQ~5A"

decoded_trigger = ''
wlan.connect(ssid, pw)


trigger = '0'

temperature = "None"
humidity = "None"
led_status = "0"
light_measure = "None"
radar_measure = "None"


#----------------WIFI FUNCTIONS----------------
def get_trigger():
    
    global led_status
    global trigger
    
    trigger = conn.recv(1024)
    
def send_data():
    
        encodeVar = str(temperature) + '/' + str(humidity) + '/' + str(led_status) + '/' + str(light_measure) + '/' + str(radar_measure)
        cl.send(encodeVar.encode('utf-8'))

def waiting_connectionLED():
    
    led = machine.Pin("LED",machine.Pin.OUT)
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
    
def light_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.on();

#--------------UART FUNCTION------------------
def deviceVerif(rawString):
    verifVar = ""
    global temperature
    global light_measure
    global radar_measure
    global humidity
    
    for i in range(4):
        verifVar = verifVar + rawString[i]
        
    if verifVar == "temp":
        temperature = ""
        for i in range(len(rawString)-4):
            temperature = temperature + rawString[4+i]
            #print("Temp:",temperature)
            
    if verifVar == "humi":
        humidity = ""
        for i in range(len(rawString)-4):
            humidity = humidity + rawString[4+i]
            #print("Humidity:",humidity)
            
    if verifVar == "rada":
        radar = ""
        for i in range(len(rawString)-4):
            radar = radar + rawString[4+i]
            #print("Radar:",radar)
    
            
    if verifVar == "ligh":
        light = ""
        for i in range(len(rawString)-4):
            light = light + rawString[4+i]

timeout = 10

while timeout > 0:
    if wlan.status() >= 3:
        light_onboard_led()
        break
    else:
        waiting_connectionLED()
        
    timeout -= 1
    time.sleep(1)
wlan_status = wlan.status()

#-------SERVER START---------------
s = socket.socket()
s.bind(('',3030))
s.listen(1)

while True:
    
    b = None
    verifVar = ""
    
    if uart.any():
        b = uart.readline()
        #print(b)
        try:
            encoder = b.decode("unicode","ignore")
            #print(encoder)
            deviceVerif(encoder)
        except Exception as e:
            print(repr(e))
            
            
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        trigger = cl.recv(1024)
        if trigger.decode('utf-8') == "1":
            send_data()
        cl.close()
        
        if trigger.decode('utf-8') == "2":
            led_status = 1
            decoded_trigger = ''
        
        elif trigger.decode('utf-8') == "3":
            led_status = 0
            decoded_trigger = ''
        
        if led_status == 1:
            led.turnLightning()
        elif led_status == 0:
            led.clear()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
            