







from machine import I2C, Pin

import time

"""
//--------------------- Acc茅l茅rometre MMA8452 -----------------//

// definition des principaux registres du composant permettant //
// sa mise en oeuvre simplifi茅e. D'autres registres existent   //
// pour exploiter les fonctionnalit茅s avanc茅es du composant,   //
// pour cela se r茅f茅rer 脿 la documentation.                    //
//-------------------------------------------------------------//
#define STATUS 0x00
#define OUT_X_MSB 0x01
#define OUT_X_LSB 0x02
#define OUT_Y_MSB 0x03
#define OUT_Y_LSB 0x04
#define OUT_Z_MSB 0x05
#define OUT_Z_LSB 0x06


#define SYSMOD 0x0B

#define CTRL_REG1 0x2A
#define CTRL_REG2 0x2B
#define CTRL_REG3 0x2C
#define CTRL_REG4 0x2D
#define CTRL_REG5 0x2E

#define XYZ_DATA_CONFIG 0x0E

#define HP_FILTER_CUTOFF 0x0F

#define INT_SOURCE 0x0C
#define TRANSCIENT_CFG 0x1D
#define TRANSCIENT_SRC 0x1E
#define TRANSCIENT_THS 0x1F
#define TRANSCIENT_COUNT 0x20

#define PULSE_CFG 0x21
#define PULSE_SRC 0x22
#define PULSE_THSX 0x23
#define PULSE_THSY 0x24
#define PULSE_THSZ 0x25
#define PULSE_TMLT 0x26
#define PULSE_LTCY 0x27
#define PULSE_WIND 0x28

#define ASLP_COUNT 0x29

#define OFF_X 0x2F
#define OFF_Y 0x30
#define OFF_Z 0x31

"""

i2c = I2C(0,pins=('P10', 'P9'))
i2c.init(I2C.MASTER,baudrate=20000)


def StandByMode():
  i2c.writeto_mem(0x1D,0x2A,0x00)

  
def ActiveMode():
  i2c.writeto_mem(0x1D,0x2A,0x01)
  

def ConfigurationRegister():
  i2c.writeto_mem(0x1D,0x0E,0x00)
  

def LireDataXYZ():
  i2c = I2C(0,pins=('P10', 'P9'))
  i2c.init(I2C.MASTER,baudrate=20000)
  StandByMode()
  ActiveMode()
  ConfigurationRegister()
  data=i2c.readfrom_mem(0x1D,0x00,7)
  StandByMode()
    
  xAccl = (data[1] * 256 + data[2]) / 16
  if xAccl > 2047 :
    xAccl -= 4096 
  yAccl = (data[3] * 256 + data[4]) / 16
  if yAccl > 2047 :

    yAccl -= 4096   
  zAccl = (data[5] * 256 + data[6]) / 16
  if zAccl > 2047 :
    zAccl -= 4096  
  return xAccl,yAccl,zAccl

 
 

x1,y1,z1=0,0,0
x,y,z=0,0,0
for i in range(100):
  x1,y1,z1=x,y,z
  x,y,z=LireDataXYZ()
  
  DeltaX,DeltaY,DeltaZ=abs(abs(x)-abs(x1)),abs(abs(y)-abs(y1)),abs(abs(z)-abs(z1))
  #print(LireDataXYZ())
  print(DeltaX,DeltaY,DeltaZ)
  time.sleep(1)












