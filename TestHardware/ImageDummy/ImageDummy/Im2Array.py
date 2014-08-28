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
	options, remainder = parser.parse_args()
	if(options.size and options.image):
		# Convert options
		size = int(options.size)
		image = options.image

		# Check size
		if(size > 200):
			print("\nSize must be 150 x 150 or less")
			sys.exit(0)

		# Resize, B&W and save new image
		im = Image.open(image)
		name,ext = image.split('.')
		im = im.convert('L')
		im = im.resize((size,size),Image.ANTIALIAS)
		new = name + "New." + ext
		im.save(new)
		print ("\nNew image: %s" % str(new))


		# Save a C 2D array
		IM = numpy.asarray(im)
		print ("\nMatrix size: %s" % str(IM.shape))

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

	else:
		print("\nPlease specify image (-i) and size (-s)")
