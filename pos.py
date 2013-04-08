#!/usr/bin/python
import serial
from time import sleep
from random import randrange
import os
import pickle

p = '/dev/tty.usbserial-AFV7FKBE'
HEADER = """
	.___        __                        .__    .___            
	|   | _____/  |________   ____ ______ |__| __| _/_ __  ______
	|   |/    \   __\_  __ \_/ __ \\__ __ \|  |/ __ |  |  \/  ___/
	|   |   |  \  |  |  | \/\  ___/|  |_> >  / /_/ |  |  /\___ \ 
	|___|___|  /__|  |__|    \___  >   __/|__\____ |____//____  >
	         \/                  \/|__|           \/          \/ 
"""
fake = False
ser = serial.Serial(p, 19200)

def do_prologue():
	print "connecting to com port.."
	sleep(0.25)
	print "we have an open port.."
	sleep(0.25)
	print "on %s...\n" % p
	sleep(0.20)
	print "try baud rates..."
	sleep(0.10)
	print "Baud rate found. Using > 9000\n"
	sleep(0.35)
	print "Don't try this at home. \nBegin awesome GUI.\n\n"
	sleep(0.75)
	print HEADER
	print "COMM open. Please tap card...\n"

do_prologue()

if fake:
	db = pickle.load( open( "chase.p", "rb" ) )
else:
	db = []

if not fake:
	for x in range(0,6):
		c = ""
		s = ""
			
		while c != "?":
			c = ser.read(1)
			s += c
			
		s = s.replace('myccnumber', 'xxxxxxxx')
		
		if not (x % 2):
			if s[0] != "B":
				s = s.split("B")[1]

		s = s.replace(';','')
		s = s.replace('?','')
		s = s.strip()
		
		print s
		db.append(s)
		
		s = ""
		if x % 2:
			print ""

ser.close()

if not fake:
	i = randrange(1,10000)
	pickle.dump( db, open( "db-%s.p" % repr(i), "wb" ) )

evens = []
for idx,val in enumerate(db):
	if idx % 2 == 0:
		evens.append(val)

tmp_mask = [ord(a) ^ ord(b) for a,b in zip(evens[0],evens[1])]
tmp_mask2 = [ord(a) ^ ord(b) for a,b in zip(evens[1],evens[2])]
even_mask = [a | b for a,b in zip(tmp_mask,tmp_mask2)]

output = [""]*len(evens)
for idx in range(1,len(even_mask)):
	if even_mask[idx] != 0:
		if even_mask[idx-1] == 0:
			for idy in range(0,len(output)):
				output[idy] += " "
		for idy in range(0,len(output)):
			output[idy] += evens[idy][idx]

print "PAN: %s\n" % evens[0][:16].replace('^','')
for line in output:
	print "DCSC:%s" % line
