import socket, thread, string, binascii, time

IP='127.0.0.1' 
PORTA_SRC=50020

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

arq_white=open('whitelist.txt','r')
arq_black=open('blacklist.txt','r')
arq_dt=open('denyterms.txt','r')
whitelist=arq_white.readlines()
blacklist=arq_black.readlines()
denyterms=arq_dt.readlines()
arq_white.close()
arq_black.close()
arq_dt.close()

server.bind((IP,PORTA_SRC))

server.listen(5)

print 'Listening on %s %s' %(IP,PORTA_SRC)



