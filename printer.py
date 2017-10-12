from PIL import Image

import serial
import time
from easygui import *

print("1")

ser = serial.Serial('/dev/ttyUSB0', 57600)
ser.write(b"\xF6")
rep = ser.read(2);

print("go")

reply='bho'
if rep == b'\xff\t' :
	choices = ["Convert Image","Load Converted Image","Preview","Print","Set Burning Time","Send Laser Home", "Reset Printer","Pause","Quit","Up", "Stop"]

	while (reply != 'Quit'):
		reply = choicebox("What would you like to do?", choices=choices)

		if reply == choices[0] :

			file_path = fileopenbox()
			im = Image.open(file_path)

			im = im.resize((512,512), Image.NEAREST)
			im = im.convert('1').transpose(Image.FLIP_TOP_BOTTOM)


			im.save('converted.bmp')
			msgbox("Check converted.bmp for a (Vertically flipped) preview")
		elif reply == choices[1]:
				print('Sending converted.bmp to machine, please wait')
				ser.write(b"\xFF\x06\x01\x00")
				time.sleep(3)
				print('.')
				ser.write(open("converted.bmp","rb").read())
				print('.')
				time.sleep(3)
				print('Done!')

				ser.write(b"\xF3")
		elif reply == choices[2]:
			ser.write(b"\xF4")
		elif reply == choices[3]:
			ser.write(b"\xF1")
		elif reply == choices[4]:
			#burnTime=int(input("Enter burning time (1-240) : "))
			burnTime=integerbox(msg='Enter Burning time', title='Set Burning Time', default=20, lowerbound=1, upperbound=240)
		#ser.write(b"\x10")
			if burnTime != None :
				ser.write(bytes([burnTime]))
		elif reply == choices[5]:
			ser.write(b"\xF3")
		elif reply == choices[6]:
			print("U")
			ser.write(b"\xFF\x03\x01\x00")
		elif reply == choices[7]:
			ser.write(b"\xF2")
		elif reply == "Up":
			print("p")
			ser.write(b"\xFF\x01\x01\x00")
		elif reply == "Stop":
			print("p")
			ser.write(b"\xFF\x01\x02\x00")


else :
	print('Printer not connected')
