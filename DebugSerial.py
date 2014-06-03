#!/usr/bin/python
from threading import Thread
from random import randrange
import time
import DS_strings
from DS_graphs import Graph
from DS_serials import Serial

def main():
	u = Serial()
	#g = Graph(100)
	#t1 = Thread(target=g.update)
	#t1.start()
	#for i in range(1,150):
	#	time.sleep(0.05)
	#	dummyData = randrange(0,255,1)
	#	DS_strings.radix(dummyData)
	#	g.newXY(i,dummyData)
	#g.kill()
	#t1.join()
	#print 'Finished'


def connect(com,baudrate):
	try:
		return serial.Serial(com,baudrate,bytesize=8,timeout=1,parity=serial.PARITY_NONE,rtscts=0)
	except serial.serialutil.SerialException:
		print('Error: Connecting to serial port, exiting...')
		sys.exit(0)

if __name__ == "__main__":
	main()

