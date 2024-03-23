import neopixel
import machine
import time
from random import *
import network
import socket

p = machine.Pin(28)
np = neopixel.NeoPixel(p, 256)
np.brightness = 0.03
n = 256



wait = 20

r = 200
b = 235
g = 0

rawData = 0
def wheel(pos):

  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def rainbow():
    for j in range(256):
        for i in range(n):
            np[i] = wheel(((i * 256 // n) + j) & 255)
        np.write()
        time.sleep_ms(wait)
        

def turnLightning():
    for i in range(n):
        np[i] = (20,20,20)
        np.write()
        
def clear():
    for i in range(n):
        np[i] = (0,0,0)
        np.write()
        
def cycle(r, g, b, wait):
  for i in range(n):
    for j in range(n):
      np[j] = (0, 0, 0)
    np[i % n] = (r, g, b)
    np.write()

    #time.sleep_ms(wait)
    
#while True:
    #cycle(250,0,0,1)