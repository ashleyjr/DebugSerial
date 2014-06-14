#!/usr/bin/python

import time
import pylab as pl

class Graph:
	def __init__(self,w):
		self.fig=pl.figure()
		self.width = w
		self.count = 0
		pl.axis([0,w,0,255])
		pl.ion()
		pl.show()
		self.x = list()
		self.y = list()
		self.alive = True;
	def new(self,data):
		self.x.append(self.count)
		self.y.append(data)
		self.count = self.count + 1
		if(self.count > self.width):
			self.x.pop(0)
			self.y.pop(0)
	def update(self):
		while(self.alive):
			time.sleep(1)
			x_size = len(self.x)
			y_size = len(self.y)
			if(self.count > self.width):
				pl.axis([self.count-self.width,self.count,0,255])
			else:
				pl.axis([0,self.width,0,255])
			if(x_size < y_size):
				pl.scatter(self.x[:x_size],self.y[:x_size])
			else:
				pl.scatter(self.x[:y_size],self.y[:y_size])
			self.fig.canvas.draw()
	def kill(self):
		self.alive=False



