
import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const

# delay between receiving a message and waiting for the next message
POLL_DELAY = const(15)
# Delay between receiving a message and sending the response
# (so that the other pico has time to listen)
SEND_DELAY = const(10)

# Pico pin definition:
myPins = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 5, "ce": 12}

# Addresses
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0","...","...")
# order: humidity and temperature, light, radar, receiver

csn = Pin(myPins["csn"], mode=Pin.OUT, value=1)
ce = Pin(myPins["ce"], mode=Pin.OUT, value=0)
nrf = NRF24L01(SPI(myPins["spi"]), csn, ce, payload_size=8)



print("nRF24L01 receiver; waiting for the first post...")

while True:
    for i in range(3):
        nrf.open_tx_pipe(pipes[i])
        nrf.open_rx_pipe(1, pipes[3])
        nrf.start_listening()
        if nrf.any(): # we received something
            while nrf.any():
                buf = nrf.recv()
                encVar = struct.unpack("i", buf)
                print("message received:", encVar)
                utime.sleep_ms(POLL_DELAY) # delay before next listening
                
            response = "success" # preparing the response

            utime.sleep_ms(SEND_DELAY) # Give the other Pico a brief time to listen
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("i", response))
            except OSError:
                pass
            print("reply sent:", response)
