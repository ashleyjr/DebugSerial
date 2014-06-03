#!/usr/bin/python
from random import randrange
import DS_strings

import time
import numpy as np
import matplotlib.pyplot as plt




fig=plt.figure()
plt.axis([0,100,0,255])

x=list()
y=list()

plt.ion()
plt.show()

DS_strings.radixHeader();
for i in range(1,200):
	dummyData = randrange(0,255,1)
	if(i > 100):
		plt.axis([i-100,i,0,255])
	DS_strings.radix(dummyData)
	temp_y=np.random.random()
	x.append(i)
	y.append(dummyData)
	plt.scatter(i,dummyData)
	plt.draw()
	time.sleep(0.05)



