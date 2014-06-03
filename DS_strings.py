#!/usr/bin/python

def zeroPad(s,length):
	while(len(s) < length):
		s = "0" + s
	return(s)

def nonPrint(data):
	if(data == 0):
		return "<Null char>"
	elif(data == 1):
		return "<datatart of Heading>"
	elif(data == 2):
		return "<Start of Text>"
	elif(data == 3):
		return "<End of Text>"
	elif(data == 4):
		return "<End of Transmission>"
	elif(data == 5):
		return "<Enquiry>"
	elif(data == 6):
		return "<Acknowledgment>"
	elif(data == 7):
		return "<Bell>"
	elif(data == 8):
		return "<Back Space>"
	elif(data == 9):
		return "<Horizontal Tab>"
	elif(data == 10):
		return "<Line Feed>"
	elif(data == 11):
		return "<Vertical Tab>"
	elif(data == 12):
		return "<Form Feed>"
	elif(data == 13):
		return "<Carriage Return>"
	elif(data == 14):
		return "<Shift Out / X-On>"
	elif(data == 15):
		return "<Shift In / X-Off>"
	elif(data == 16):
		return "<Data Line Escape>"
	elif(data == 17):
		return "<Device Control 1 (oft. XON)>"
	elif(data == 18):
		return "<Device Control 2>"
	elif(data == 19):
		return "<Device Control 3 (oft. XOFF)>"
	elif(data == 20):
		return "<Device Control 4>"
	elif(data == 21):
		return "<Negative Acknowledgement>"
	elif(data == 22):
		return "<Synchronous Idle>"
	elif(data == 23):
		return "<End of Transmit Block>"
	elif(data == 24):
		return "<Cancel>"
	elif(data == 25):
		return "<End of Medium>"
	elif(data == 26):
		return "<Substitute>"
	elif(data == 27):
		return "<Escape>"
	elif(data == 28):
		return "<File Separator>"
	elif(data == 29):
		return "<Group Separator>"
	elif(data == 30):
		return "<Record Separator>"
	elif(data == 31):
		return "<Unit Separator>"
	elif(data == 32):
		return "<Space>"
	else:
		return chr(data)

def radixHeader():
	print "DEC     HEX     BIN          ASCII"

def radix(data):
	s = "{0:d}".format(data)
	s = zeroPad(s,3)
	h = "{0:x}".format(data)
	h = zeroPad(h,2)
	s = s + "   	" + h.upper()
	b = "{0:b}".format(data)
	b = zeroPad(b,8)
	s = s + "      " + b + "     " + nonPrint(data)
	print s

