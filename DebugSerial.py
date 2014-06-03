#!/usr/bin/python
from threading import Thread
from random import randrange
import DS_strings

import time
import numpy as np
import matplotlib.pyplot as plt

i = 0
exit = 0
x=list()
y=list()

def updateGraph():
	while(exit == 0):
		plt.scatter(x,y)
		plt.draw()
		time.sleep(0.1)


fig=plt.figure()
plt.axis([0,100,0,255])

plt.ion()
plt.show()

DS_strings.radixHeader();


thread = Thread(target=updateGraph,args=[])
thread.start()
while(i < 20):
	i = i + 1
	dummyData = randrange(0,255,1)
	if(i > 100):
		plt.axis([i-100,i,0,255])
	DS_strings.radix(dummyData)
	temp_y=np.random.random()
	x.append(i)
	y.append(dummyData)
	#plt.scatter(x,y)
	#plt.draw()
	#time.sleep(0.01)
exit = 1
thread.join()


