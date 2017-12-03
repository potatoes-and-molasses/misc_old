import socket
import random
import binascii
TARGET = ('127.0.0.1',5666)
def xor(st1,st2):
    return ''.join(chr(ord(st1[i]) ^ ord(st2[i%len(st2)])) for i in range(len(st1)))
def nrpe(data):
    a=socket.socket()
    a.connect(TARGET)
    a.send(data)
    return a.recv(1000000)
def getrandom(l):
    return ''.join(chr(random.randint(0,255)) for i in range(l))


def sendcmd(cmd):
    head = '\x00\x02'
    typee = '\x00\x01' #02 for response
    chksum = '\x00'*4
    whatevs = '\x00'*2
    data = cmd + (1026-len(cmd))*'\x00'
    
    chksum=hex(binascii.crc32(head+typee+chksum+whatevs+data) & 0xffffffff)[2:].replace('L','')
    print chksum
    chksum = '0'*(8-len(chksum))+chksum
    chksum = ''.join(chr(int(chksum[i:i+2],16)) for i in range(0,len(chksum),2))
    
    return nrpe(head+typee+chksum+whatevs+data)






while 1:
    print sendcmd(raw_input('>>'))







        
