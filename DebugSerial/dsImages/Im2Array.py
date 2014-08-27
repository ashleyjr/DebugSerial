#!/usr/bin/python

from PIL import Image

path = "Lenna.png"
if __name__ == "__main__":
	im = Image.open(path)
	im = im.resize((160,300),Image.ANTIALIAS)
	im.save(path)

