










from machine import I2C, Pin
import DS3231
import time

i2c = I2C(0,pins=('P10', 'P11'))
i2c.init(I2C.MASTER,baudrate=20000)
ds = DS3231.DS3231(i2c)

#ds.Hour(12)

#ds.Time()
#ds.Time([12,10,0])

ds.DateTime([2020,12,10,1,14,11,0])

def temps():
  i2c = I2C(0,pins=('P10', 'P11'))
  i2c.init(I2C.MASTER,baudrate=20000)
  ds = DS3231.DS3231(i2c)
  

  
  liste_date=ds.DateTime()
  return liste_date






















