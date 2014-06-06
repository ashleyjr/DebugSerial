#!/usr/bin/python
import sys

class Test:
	def __init__(self,testFile):
		try:
			test = testFile + ".csv"
			f = open(test, 'r')
			self.send = list()
			self.get = list()
			print('Loading %s' % test)
			num = 1
			for line in f:
				data = line.split(',')
				print data
				if(num == 1):
					if((len(data) != 3) or (data[0] != "<DS")):
						print('\nInvalid .csv file: %s' % data)
						raise NameError
					data[1] = data[1].strip('Num=')
					if(data[1] == 'True'):
						numbers=True
					elif(data[1] == 'False'):
						numbers=False
					else:
						print('\nInvalid boolean option for Num: %s' % data[1])
						raise NameError
					print('Numbers: %s' % data[1])
				else:
					if((len(data) != 2)):													# Two entrie per line
						print('\nInvalid number of entries on line %s: %s' % (num,line))
						raise NameError
					self.send.append(data[0])
					self.get.append(data[1].strip('\n'))
				num = num + 1
			f.close()
			print self.send
			print self.get
		except NameError:
			print('Failed to load test vectors, exiting...')
			sys.exit(0)


