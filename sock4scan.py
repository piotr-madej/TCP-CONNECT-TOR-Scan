# full range TCP scan using TOR proxy
# usage: python sock4scan.py x.x.x.x
import socket
import sys
import struct
import resource
from thread import start_new_thread
from time import sleep, ctime

#no optimal code / bypass cpu usage limitation for this script
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

#host to scan
HOST = sys.argv[1] #ipv4 address format

#configure
SOCK4_HOST = '192.168.88.130'
SOCK4_PORT = 9100     

#logs
sys.stdout = open(HOST + ".log", 'w', 0)

#sock4 protocol description
HELLO = '\x04\x01'
PORT = struct.pack(">H",88)
IP = socket.inet_aton(HOST)
END = '\x00'

num_threads = 0
def scan(i):
	global num_threads
	num_threads += 1
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(150)
		s.connect((SOCK4_HOST, SOCK4_PORT))
		PORT = struct.pack(">H",i)
		s.send(HELLO + PORT + IP + END)
		s.settimeout(150)
		buff = s.recv(1024)
		if buff == '\x00\x5a\x00\x00\x00\x00\x00\x00':
			print str(i) + " OPEN"
		elif buff == '\x00\x5b\x00\x00\x00\x00\x00\x00':
			print str(i) + " CLOSED"
		else:
			print str(i) + " ERROR"
	except:
		print str(i) + " ERROR"
	num_threads -= 1


print HOST
print ctime()

for i in range(1,65536):
	start_new_thread(scan, (i,))
	sleep(125.0/1350)
	while num_threads > 1350:
		pass

print ctime()

sleep(160)

print ctime()
print 'END'