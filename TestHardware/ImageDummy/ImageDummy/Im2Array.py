#!/usr/bin/python

import sys
import optparse
from PIL import Image
import numpy


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-s', '--size',
		dest="size"
	)
	parser.add_option('-i', '--image',
		dest="image"
	)
	parser.add_option('-c', '--colour',action="store_true",
		dest="colour"
	)

	options, remainder = parser.parse_args()

	if(options.colour):
		print "yes"

	if(options.size and options.image):
		# Convert options
		size = int(options.size)
		image = options.image
		colour = options.colour


		# Check size
		if(size > 200):
			print("\nSize must be 150 x 150 or less")
			sys.exit(0)

		if(colour):
			out = "\nColour image"

			# Resize, B&W and save new image
			im = Image.open(image)
			name,ext = image.split('.')
			im = im.resize((size,size),Image.ANTIALIAS)
			new = name + "New." + ext
			im.save(new)
			out = ("\nNew image: %s" % str(new))

			# Save as 3 RGB 2d arrays
			IM = numpy.asarray(im)
			out = out + "\nMatrix size: %s" % str(IM.shape)


			arr = "\n\n#define ROW " + str(size)
			arr = arr + "\n#define COL " + str(size)
			arr = arr + "\n#include <avr/pgmspace.h>"
			for k in range(0,3):
				arr = arr + "\nconst uint8_t " + name
				if(k == 0):
					arr = arr + "_R"
				elif(k == 1):
					arr = arr + "_G"
				else:
					arr = arr + "_B"
				arr = arr  + "[" + str(size) + "]" +  "[" + str(size) + "] PROGMEM= {"
				for i in range(0,size):
					arr = arr + "\n    {"
					for j in range(0,size):
						arr = arr + str(IM[i,j,k])
						if(j != (size-1)):
							arr = arr + ","
					arr = arr + "}"
					if(i != (size-1)):
						arr = arr + ","
				arr = arr + "\n};"

			f = open(name + ".h", 'w')
			f.write(arr)
			f.close()



		else:
			# Resize, B&W and save new image
			im = Image.open(image)
			name,ext = image.split('.')
			im = im.convert('L')
			im = im.resize((size,size),Image.ANTIALIAS)
			new = name + "New." + ext
			im.save(new)
			out = ("\nNew image: %s" % str(new))


			# Save a C 2D array
			IM = numpy.asarray(im)
			out = out + "\nMatrix size: %s" % str(IM.shape)

			arr = "\n\n#define ROW " + str(size)
			arr = arr + "\n#define COL " + str(size)
			arr = arr + "\n#include <avr/pgmspace.h>"
			arr = arr + "\nconst uint8_t " + name + "[" + str(size) + "]" +  "[" + str(size) + "] PROGMEM= {"
			for i in range(0,size):
				arr = arr + "\n    {"
				for j in range(0,size):
					arr = arr + str(IM[i,j])
					if(j != (size-1)):
						arr = arr + ","
				arr = arr + "}"
				if(i != (size-1)):
					arr = arr + ","
			arr = arr + "\n};"

			f = open(name + ".h", 'w')
			f.write(arr)
			f.close()

			print arr

		print out

	else:
		print("\nPlease specify at least image (-i) and size (-s)")
