





















import mfrc522
from os import uname


def do_read_simple():

	if uname()[0] == 'WiPy':
    #                     SCK   MOSI   MISO   RST  CS=SDA
		rdr = mfrc522.MFRC522("P5", "P11", "P6", "P7", "P8")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Placer la carte devant RFID : read from address 0x08")
	print("")
	badge=0
	

	try:
    
		while (badge==0):


			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
          
					badge=1
					return raw_uid
                    

  

	except KeyboardInterrupt:
		print("Bye")

 
 

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



list_id = do_read_simple()

print(list_id[0])
print('.')
print(list_id[1])
print('.')
print(list_id[2])
print('.')
print(list_id[3])
print('.')
print(list_id[4])

























