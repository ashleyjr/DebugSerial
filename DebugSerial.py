#!/usr/bin/python

# Why not ?
print("______     _                 _____           _       _" )
print("|  _  \   | |               /  ___|         (_)     | |")
print("| | | |___| |__  _   _  __ _\ `--.  ___ _ __ _  __ _| |")
print("| | | / _ \ '_ \| | | |/ _` |`--. \/ _ \ '__| |/ _` | |")
print("| |/ /  __/ |_) | |_| | (_| /\__/ /  __/ |  | | (_| | |")
print("|___/ \___|_.__/ \__,_|\__, \____/ \___|_|  |_|\__,_|_|")
print("                        __/ |                          ")
print("                       |___/                           ")
print("------- Ashley J. Robinson ----- ajrobinson.org -------")

from threading import Thread
from random import randrange
import time
import DS_strings
from DS_graphs import Graph
from DS_serials import Serial

def main():
	u = Serial()
	g = Graph(100)
	t1 = Thread(target=g.update)
	t1.start()
	for i in range(1,150):
		time.sleep(0.05)
		u.Send(randrange(0,255))
		data = u.Get()
		DS_strings.radix(data)
		g.newXY(i,data)
	g.kill()
	t1.join()
	print 'Finished'


if __name__ == "__main__":
	main()

