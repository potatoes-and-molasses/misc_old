

def bitstohex(bits):

        return chr(int(bits,2))

def hextobits(hexstr):
        
	a=bin(ord(hexstr))[2:]
	
	return (8-len(a))*'0'+a

def hide(picture,msg):

        LENGTH_HEADER=23#=1mb max, although size still shouldn't be bigger than approx. picture_size/8 bytes.

        txt=open(picture, 'r').read()
        sneaky=open(msg,'r').read()
        header = txt[:54]
        bytess = map(hextobits, txt[54:])
        messagebits = ''.join([hextobits(i) for i in sneaky])
        lengthbits = bin(len(messagebits))[2:]
        for i,j in enumerate('0'*(LENGTH_HEADER-len(lengthbits))+lengthbits+messagebits):
                bytess[i]=bytess[i][:7]+j

        q=open(picture, 'w')
        q.write(header+''.join([bitstohex(i) for i in bytess]))
        q.close()
        
        return 1

def unhide(picture):

        LENGTH_HEADER=23
        
        txt=open(picture, 'r').read()

        l = int('0b'+''.join(hextobits(i)[7] for i in txt[54:54+LENGTH_HEADER]),2)
        msgbits = ''.join(hextobits(i)[7] for i in txt[54+LENGTH_HEADER:54+LENGTH_HEADER+l])

        return ''.join([bitstohex(msgbits[i*8:i*8+8]) for i in range(len(msgbits)/8)])
        



