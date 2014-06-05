#!/usr/bin/python


class Test:
	def __init__(self,testFile):
		test = testFile + ".csv"
		f = open(test, 'r')
		for line in f:
			data = line.split(',')
			if((len(data) != 2)):
				print('Invalid test vector')
				break
			self.send.append(data[0])
		f.close()

