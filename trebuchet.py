#!/usr/bin/env python

import socket
import sys

if len(sys.argv) != 3 or sys.argv[1].lower() not in ("send","recv"):
    print "Usage: ./trebuchet.py (send|recv) [filename]"
    sys.exit(64) #EX_USAGE, can't use constant due to cross-platform
command = sys.argv[1].lower()
filename = sys.argv[2]

PORT  = 8228
BROADCAST = ('<broadcast>',PORT)
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(1)

s.bind(('',PORT))

if command == "send":
    while True:
        s.sendto(filename,BROADCAST)
        try:
            data,host = s.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            pass #just retry over and over in event of timeout
        else:
            if (data == "ready"):
                print data,host
                sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sendsock.connect(host)
                f = open(recvname,"rb")
                sendsock.send(f.read())
                sendsock.close()
                f.close()
                break
elif command == "recv":
    recvname = None
    while recvname != filename:
        try:
            recvname,host = s.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            pass #retry over and over
    recvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recvsock.bind(host)
    recvsock.listen(1) 
    s.send('ready',host)
    conn,addr = recvsock.accept()
    f = open(recvname,"wb")
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        f.write(data)
    f.close()
    conn.close()
