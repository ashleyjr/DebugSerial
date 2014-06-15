#!/usr/bin/python
import sys

# Cross platform grab character
class Getch:
	def __init__(self):
		try:				self.impl = GetchWindows()
		except ImportError:	self.impl = GetchUnix()
	def __call__(self):
		return self.impl()
class GetchUnix:
	def __init__(self):
		import tty
	def __call__(self):
		import tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
class GetchWindows:
	def __init__(self):
		import msvcrt
	def __call__(self):
		import msvcrt
		return msvcrt.getch()

# Yes no questions
def yesno(output):
	char = Getch()
	while(1):
		sys.stdout.write(output)
		sys.stdout.write("[y/n]: ")
		user = char()
		print(user)
		if((user == 'y') or (user == 'Y')):
			return True
		if((user == 'n') or (user == 'N')):
			return False


def zeroPad(s,length):
	while(len(s) < length):
		s = "0" + s
	return(s)

def humanRead(char,text):
	data = ord(char)
	if((data > 255) or (data < 0)):
		print("Invalid!")
		sys.exit(0)
	elif(data == 0):
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
		if(text):
			return "\n\r"
		else:
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
		if(text):
			return " "
		else:
			return "<Space>"
	elif(data == 127):
		if(text):
			return "\b"
		else:
			return "<back>"
	else:
		return char




