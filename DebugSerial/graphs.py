#!/usr/bin/python

import time
import pylab as pl

class Graph:
	def __init__(self,w):
		self.fig=pl.figure()
		self.width = w
		pl.axis([0,w,0,255])
		pl.ion()
		pl.show()
		self.x = list()
		self.y = list()
		self.alive = True;
	def newXY(self,new_x,new_y):
		self.x.append(new_x)
		self.y.append(new_y)
	def update(self):
		while(self.alive):
			time.sleep(0)
			x_size = len(self.x)
			y_size = len(self.y)
			if(x_size < y_size):
				pl.scatter(self.x[:x_size],self.y[:x_size])
				if(x_size > self.width):
					pl.axis([x_size-self.width,x_size,0,255])
			else:
				pl.scatter(self.x[:y_size],self.y[:y_size])
				if(y_size > self.width):
					pl.axis([y_size-self.width,y_size,0,255])
			self.fig.canvas.draw()

	def kill(self):
		self.alive=False
		pl.show(block=True)



