

# main.py -- put your code here!
import mfrc522
from os import uname
import pycom
import time
from machine import Pin,I2C,Timer,PWM
import re




def Buzzer(duree):

  pwm = PWM(0, frequency=3500)  # use PWM timer 0, with a frequency of 5KHz
  # create pwm channel on pin P22 with a duty cycle of 50%
  pwm_c = pwm.channel(0, pin='P21', duty_cycle=0.5)

  pwm_c.duty_cycle(0.5) # change the duty cycle to 30%

  time.sleep(duree)
  pwm_c.duty_cycle(0) # change the duty cycle to 30%
  # eh oui ca a change ici



def Beep_long():
  Buzzer(0.5)
  #beeper=Pin('P21',Pin.OUT)
  #beeper.value(1)            #Set led turn on
  #time.sleep(1)
  #beeper.value(0)            #Set led turn off
  time.sleep(0.5)
  pycom.rgbled(0x7f7f00) # jaune
  time.sleep(0.2)




def Beep_court():
  Buzzer(0.5)
  # beeper=Pin('P21',Pin.OUT)
  #beeper.value(1)            #Set led turn on
  #time.sleep(0.4)
  #beeper.value(0)            #Set led turn off
  time.sleep(0.5)
  pycom.rgbled(0x7f7f00) # jaune
  time.sleep(0.2)
  
'''
chronometre = Timer.Chrono() # ca va etre le chronometre

i2c = I2C(0,pins=('P10', 'P9'))
i2c.init(I2C.MASTER,baudrate=20000)
ds = DS3231.DS3231(i2c)

'''

def lecture_temps(): # Lecture de l'horloge temps r茅el
  i2c = I2C(0,pins=('P10', 'P9'))
  i2c.init(I2C.MASTER,baudrate=20000)
  ds = DS3231.DS3231(i2c)
  #ds.DateTime([2020,10,8,4,11,53,0])
  liste_date=ds.DateTime()
  return liste_date



def do_read_unique():

	if uname()[0] == 'WiPy':
    #                     SCK   MOSI   MISO   RST  CS=SDA
		rdr = mfrc522.MFRC522("P5", "P11", "P6", "P7", "P8")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	compteur=0

	try:
    
		while (compteur<8):
			compteur=compteur+1

			if (compteur==8):
		
				raw_uid=[0,0,0,0,0]
				return raw_uid
      

			(stat, tag_type) = rdr.request(rdr.REQIDL)


			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
          
					badge=1
					return raw_uid
                    


	except KeyboardInterrupt:
		print("Bye")



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




def LectureFichierUID(): # Stocke tous les uid_enregistres dans un fichier : liste_uid
  file=open('uid_autorises.txt','r')
  lines=file.readlines()
  file.close()
  # on prepare la liste des uid au bon format : liste_uid[(125,251,12,23,54)]

  #liste_uid=[]
  position2points=[]
  # on detecte d'abord la position des ":" dans tout le fichier : qu'on met dans la liste position2points
  for j in range(len(lines[0])):
    if (lines[0][j]==':'):
      position2points.append(j)
  # Lecture de tous les uid :
  for i in range (len(position2points)-1):

    positiontirets=[]    

    # Lecture du premier uid : jusqu'脿 15 caracteres, c'est e dire 5 tuples
    for j in range (position2points[i],position2points[i+1]):

      # detection des tirets
      if lines[0][j]=='-':
        positiontirets.append(j)
    
    # premier nombre
    if (positiontirets[1]-positiontirets[0]==4):
      premier_nombre=100*int(lines[0][positiontirets[0]+1])+10*int(lines[0][positiontirets[0]+2])+1*int(lines[0][positiontirets[0]+3])
    if (positiontirets[1]-positiontirets[0]==3):
      premier_nombre=10*int(lines[0][positiontirets[0]+1])+1*int(lines[0][positiontirets[0]+2])
    if (positiontirets[1]-positiontirets[0]==2):
      premier_nombre=1*int(lines[0][positiontirets[0]+1])
  
    # deuxieme nombre
    if (positiontirets[2]-positiontirets[1]==4):
      deuxieme_nombre=100*int(lines[0][positiontirets[1]+1])+10*int(lines[0][positiontirets[1]+2])+1*int(lines[0][positiontirets[1]+3])
    if (positiontirets[2]-positiontirets[1]==3):
      deuxieme_nombre=10*int(lines[0][positiontirets[1]+1])+1*int(lines[0][positiontirets[1]+2])
    if (positiontirets[2]-positiontirets[1]==2):
      deuxieme_nombre=1*int(lines[0][positiontirets[1]+1])
  
    # troisieme nombre
    if (positiontirets[3]-positiontirets[2]==4):
      troisieme_nombre=100*int(lines[0][positiontirets[2]+1])+10*int(lines[0][positiontirets[2]+2])+1*int(lines[0][positiontirets[2]+3])
    if (positiontirets[3]-positiontirets[2]==3):
      troisieme_nombre=10*int(lines[0][positiontirets[2]+1])+1*int(lines[0][positiontirets[2]+2])
    if (positiontirets[3]-positiontirets[2]==2):
      troisieme_nombre=1*int(lines[0][positiontirets[2]+1])
  
    # quatrieme nombre
    if (positiontirets[4]-positiontirets[3]==4):
      quatrieme_nombre=100*int(lines[0][positiontirets[3]+1])+10*int(lines[0][positiontirets[3]+2])+1*int(lines[0][positiontirets[3]+3])
    if (positiontirets[4]-positiontirets[3]==3):

      quatrieme_nombre=10*int(lines[0][positiontirets[3]+1])+1*int(lines[0][positiontirets[3]+2])
    if (positiontirets[4]-positiontirets[3]==2):
      quatrieme_nombre=1*int(lines[0][positiontirets[3]+1])
  
    # cinquieme nombre
    if (positiontirets[5]-positiontirets[4]==4):
      cinquieme_nombre=100*int(lines[0][positiontirets[4]+1])+10*int(lines[0][positiontirets[4]+2])+1*int(lines[0][positiontirets[4]+3])
    if (positiontirets[5]-positiontirets[4]==3):
      cinquieme_nombre=10*int(lines[0][positiontirets[4]+1])+1*int(lines[0][positiontirets[4]+2])
    if (positiontirets[5]-positiontirets[4]==2):
      cinquieme_nombre=1*int(lines[0][positiontirets[4]+1])


    liste_uid.append((premier_nombre,deuxieme_nombre,troisieme_nombre,quatrieme_nombre,cinquieme_nombre))
  return liste_uid











  
""" -----------------------------------  """ 
"""        DEBUT PROGRAMME               """
""" -----------------------------------  """
# Lecture de tous les uid autorises dans le fichier adequat  
liste_uid=[]
liste_uid=LectureFichierUID()  
chronometre.start()

""" Relais OFF """

relais.value(0)
Relai='OFF'
MACHINE_EN_FONCTIONNEMENT=0



liste_id=[0,0,0,0,0]
liste_date=lecture_temps()

""" LECTURE CONSIGNATION ou NON  """
# Voici la liste des id qui permettent de consigner une machine
id_de_consignation1=[4,207,252,156,171]
id_de_consignation2=[103,240,200,181,234]

# Voici la liste des id qui permettent de deconsigner une machine
id_de_deconsignation1=[103,145,181,100,39]

id_de_deconsignation2=[167,55,186,100,78]

# A Faire : est ce que la machine est consignee d enmblee ou pas
machine_consignee=0 # ca veut dire que la machine n est pas consignee

print("etape 1")



x1,y1,z1=x,y,z
x,y,z=LireDataXYZ()  # Mesure de l acceleration (vibrations)
DeltaX,DeltaY,DeltaZ=abs(abs(x)-abs(x1)),abs(abs(y)-abs(y1)),abs(abs(z)-abs(z1))
print(LireDataXYZ())

""" Tant que (Tag pas bon ET machine non consignee) """ # a completer

liste_id=[0,0,0,0,0]
BON_UID=0
TAG_CONNU='Faux'
print("etape 2")



    ###########################################################################################
    #                                                                                         #
    #                                                                                         #
    #                                 SI LE BADGE N'EST PAS BON                               #
    #                                                                                         #
    #                                                                                         #
    ###########################################################################################
while(True):
  while (BON_UID==0) and (machine_consignee==0): # Tant que c'est pas le Tag autorise et machine non Consignee
    print(lecture_temps())
    liste_id=do_read_unique()
    bon_id=liste_id

    for i in range(len(liste_uid)): 
      if (liste_uid[i]==(liste_id[0],liste_id[1],liste_id[2],liste_id[3],liste_id[4])):
        BON_UID=1
        TAG_CONNU='Vrai'
        Relais='ON'
        relais.value(1)
        pycom.rgbled(0x002f00)
        Beep_court()
        time.sleep(2)
        pycom.rgbled(0x000000)
        """  dans le cas ou c'est bien un tag mais non autorise: devra beeper """
    if (TAG_CONNU=='Faux'):
      if (liste_id!=[0,0,0,0,0]):
        pycom.rgbled(0x2f0000) # On allume la LED rouge
        #PWM_P21.Buzzer() # s'il est present sur la carte principale 
        Beep_long()

        pycom.rgbled(0x000000)
        liste_id=[0,0,0,0,0]  


  print("etape 3")


      ###########################################################################################
      #                                                                                         #
      #                                                                                         #
      #                                 SI LE BADGE EST BON                                     #
      #                                                                                         #
      #                                                                                         #
      ###########################################################################################
    
    
  chronometre.reset()  
  while (BON_UID==1): # Tant que c'est pas le Tag autorise et machine non Consignee
    #print(lecture_temps())
    liste_id=do_read_unique()
     
    if (liste_id==bon_id):
      pycom.rgbled(0x2f1f00)
      BON_UID=0
      TAG_CONNU='Vrais'
      Beep_court()
      relais.value(0)
      time.sleep(2)
      Relais='OFF'
      pycom.rgbled(0x000000)
      """  dans le cas ou c'est bien un tag mais non autorise: devra beeper """
    if (TAG_CONNU=='Faux'):
      if (liste_id==[0,0,0,0,0]):
        pycom.rgbled(0x2f0000) # On allume la LED rouge
        #PWM_P21.Buzzer() # s'il est present sur la carte principale 
        Beep_long()

        pycom.rgbled(0x000000)
        liste_id=[0,0,0,0,0]   
    x,y,z=LireDataXYZ()  # Mesure de l acceleration (vibrations)
    DeltaX,DeltaY,DeltaZ=abs(abs(x)-abs(x1)),abs(abs(y)-abs(y1)),abs(abs(z)-abs(z1))
    if ((DeltaX>valeur_capteur_deplacement) or (DeltaY>valeur_capteur_deplacement) or (DeltaZ>valeur_capteur_deplacement)):
      print('Moteur tourne')
      chronometre.reset()
      chronometre.start()

      
    if (chronometre.read()>300):  # duree de 300 secondes
      pycom.rgbled(0x2f1f00)
      BON_UID=0
      TAG_CONNU='Vrais'
      Beep_court()
      relais.value(0)
      time.sleep(2)
      Relais='OFF'
      pycom.rgbled(0x000000)
        
        










