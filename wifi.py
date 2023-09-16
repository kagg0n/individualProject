import network
import time
import socket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "Inetcom_265"
pw = "THfu87K*MHiCbG2%Nqn0eQ~5A"



wlan.connect(ssid, pw)
def waiting_connectionLED():
    led = machine.Pin("LED",machine.Pin.OUT)
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
def light_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.on();

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

temperature = 15
humidity = 69
led_status = 0

def send_data():
        encodeVar = str(temperature) + '/' + str(humidity) + '/' + str(led_status)
        conn.send(encodeVar.encode('utf-8'))
trigger = 0

def get_trigger():
    global trigger
    trigger = conn.recv(1024)
while True:
    s = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 3030))
        s.listen(1)
        conn, addr = s.accept()
        get_trigger()
    except:
        conn.close()
        continue
    if trigger.decode('utf-8') == '1':
        send_data()
        trigger = 0
