import os
import time
import serial

'''
Version 1.0 by Gabriele Gaggini
RPM acquisition from Arduino
Based on 1 signal per revolution sensor
Update continuosly global variable rpm and rpm_is_ctc (is connected = 1 else 0)
'''

def getRPM(rate=30, comp=3):
	global rpm
	global rpm_is_ctc
	rpm_is_ctc = 0
	 
	if rate > 30:
		rate = 30
     
	timestep = 1/float(rate)

	try:
		'''
		First line is for Mac. Second line for Win.
		'''
		ser = serial.Serial(port='/dev/tty.usbmodem1421',baudrate=115200)
#	    ser = serial.Serial(port='COM'+str(comp),baudrate=115200)
	except serial.SerialException:
	    rpm_is_ctc = 0
	    return None
	except TypeError as e:
		rpm_is_ctc = 0
		ser.close()
		return None
	else:
	    rpm_is_ctc = 1

	f = open('/Users/ggaggio19/Desktop/logger.dat','w')

	time1 = time.time()

	rpm_all = ''

	while rpm_is_ctc == 1:	

		if (time.time() - time1) > timestep:
			try:
				rpm_all = ser.read(ser.inWaiting())
				print rpm_all
				if '\n' in rpm_all:	
					rpm_list = rpm_all.split('\n') # Guaranteed to have at least 2 entries
				else:
					rpm_list = [0, 0]
				rpm = rpm_list[-2]
#				rpm = ser.readline()  Not robust: keep waiting
				try:
					rpm = float(rpm)
					print('RPM ' + str(rpm))
					print('Time: ' + str(time1))
					f.write(str(rpm) + ',' + str(time1) + '\n')
				except ValueError as e:
					rpm = 0
			except serial.SerialException:
				rpm_is_ctc = 0
			except TypeError as e:
				ser.close()
				rpm_is_ctc = 0
			except IOError as e:
				ser.close()
				rpm_is_ctc = 0
			else:
				rpm_is_ctc = 1

			time1 = time.time()

	f.close()
	
getRPM(30,3)
print(rpm_is_ctc)