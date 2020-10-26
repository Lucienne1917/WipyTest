














# boot.py -- run on boot-up

from network import WLAN
from machine import Pin
import pycom
wlan = WLAN(mode=WLAN.STA)



relais=Pin('P23',Pin.OUT)
relais.value(0)
pycom.rgbled(0x00002f)


nets = wlan.scan()
for net in nets:
    if net.ssid == 'Orange Airbox-947F':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '20727416'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

















