#!/usr/bin/env python
import sys, re, string, crypt, random, threading, thread

def mktripcode(pw):
    pw = pw.decode('utf_8', 'ignore') \
        .encode('shift_jis', 'ignore')    \
        .replace('"', '&quot;')      \
        .replace("'", '')           \
        .replace('<', '&lt;')        \
        .replace('>', '&gt;')        \
        .replace(',', ',')
    salt = (pw + '...')[1:3]
    salt = re.compile('[^\.-z]').sub('.', salt)
    salt = salt.translate(string.maketrans(':;<=>?@[\\]^_`', 'ABCDEFGabcdef'))
    trip = crypt.crypt(pw, salt)[-10:]
    return trip

class BruteThread(threading.Thread):
	def run(self):
		while True:
			x = randomString(8)
			y = mktripcode(x)
			z = 5
			if y.count('/') >= z or y.count('.') >= z:
				global lock
				lock.acquire()
				print x + ' -> ' + y
				fil = open("trips.htm", 'a')
				output = ""
				shouldEndTag = False
				if y.count('/') == z+1 or y.count('.') == z+1:
					output += "<b>"
					shouldEndTag = True
				output += x + " -> " + y + " " + str(y.count('.')) + "/" + str(y.count('/'));
				if shouldEndTag:
					output += "</b>"
				output += "<br>\n"
				fil.write(output)
				fil.close()
				lock.release()

def randomString(length):
	alphabet = string.lowercase + string.uppercase + "1234567890!@$%^&*()_-+="
	rand = ''
	for i in range(length+1):
		rand += random.choice(alphabet)
	return rand

global lock
lock = threading.Lock()
for i in range(0,50):
	BruteThread().start()
