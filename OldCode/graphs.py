#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import time

count = 1
async = False

def me():
	global count
	while(async):
		time.sleep(1)
		print " 		hi"
		count = count + 1


def update_line(num, data, line):
	global count
	line.set_data(data[...,:count])
	#data = np.random.rand(2, i)
	#count = count + 1
	if(count > 100):
		plt.xlim(count - 100, count)
	else:
		plt.xlim(0, count)
	print count
	return line,


def main():
	fig1 = plt.figure()

	data = []
	data.append([])
	data.append([])
	data = np.zeros((2,1000))
	for i in range(1,1000):
		data[0][i] = i
		data[1][i] = (1 + np.sin(i/3.14))*127
 	#data = np.random.rand(2,10)

	print data[1][1]

	l, = plt.plot([], [], 'r-')
	plt.xlim(0, 1)
	plt.ylim(0, 255)
	plt.xlabel('Rx Number')
	plt.ylabel('Value')
	plt.title('Rx Data')

	global async
	async = True
	t = threading.Thread(target=me)
	t.start()
	line_ani = animation.FuncAnimation(fig1, update_line, fargs=(data, l), interval=200, blit=True, repeat=False)
	plt.show()
	async = False
	t.join()



if __name__ == "__main__":
	main()




class Graph:
	def __init__(self,w):
		self.width = w
		self.count = 0
		self.x = list()
		self.y = list()
		self.data = np.zeros((2,1000))

	def draw(self,title):
		fig=plt.figure()
		l, = plt.plot([], [])
		plt.axis([0,self.width,0,255])
		plt.xlabel('Number')
		plt.ylabel('Value')
		plt.title(title)
		for i in range(1,1000):
			self.data[0][i] = i
			self.data[1][i] = (1 + np.sin(i/3.14))*127
		line_ani = animation.FuncAnimation(fig, self.update_line, fargs=(self.data, l), interval=50, blit=True, repeat=False)
		plt.show()
		self.async = False

	def update_line(self, num, data, line):
		line.set_data(self.data[...,:self.count])
		#data = np.random.rand(2, i)
		if(self.count > self.width):
			plt.xlim(self.count - 100, self.count)
		else:
			plt.xlim(0, self.width)
		return line,



	def new(self,data):
		self.data[0][self.count] = self.count
		self.data[1][self.count] = data
		self.count = self.count + 1


	#def update(self):
	#	x_size = len(self.x)
	#	y_size = len(self.y)
	#	if(self.count > self.width):
	#		plt.axis([self.count-self.width,self.count,0,255])
	#	else:
	#		plt.axis([0,self.width,0,255])
	#	if(x_size < y_size):
	#		plt.scatter(self.x[:x_size],self.y[:x_size])
	#	else:
	#		plt.scatter(self.x[:y_size],self.y[:y_size])
	#	self.fig.canvas.draw()
	#	self.fig.show()

	def kill(self):
		plt.close()



