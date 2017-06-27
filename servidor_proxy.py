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

while True:
		flag_wh=0
		flag_bl=0
		flag_dt=0

		mensagem=objeto.recv(1024)
		if not mensagem: break 
		mensagem_sep=mensagem.split('\n')
		site=(mensagem_sep[1].split())[1]
		
	
    if site == "detectportal.firefox.com":
			objeto.shutdown(socket.SHUT_RD)
			break

		#print mensagem	
		#arq_log.write('%s solicitou %s\n' %(IP,mensagem_sep[0]))
		
		#VERIFICACAO DE TERMOS NA WHITELIST
		for whitesite in whitelist:
			flag_wh=string.find(whitesite,site)
			if flag_wh != -1:
			        data = time.strftime("%b, %d, %Y, %H:%M:%S")
				texto_log = '%s - acesso em %s - site na whitelist\n' %(site, data)
				arqlog(texto_log)
				enderecoIP_site=socket.gethostbyname(site) #Captura endereco IP do servidor http	
				tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Cria socket para conexao TCP	
				tcp.connect((enderecoIP_site,80)) #Servidor proxy conecta ao servidor http
				tcp.sendall(mensagem) #Servidor envia requisicao do browser
				while True:
					mensagem_resposta=tcp.recv(4194304) #Servidor proxy recebe resposta do servidor http
					print mensagem_resposta
					if not mensagem_resposta: 
						tcp.close() #Conexao com servidor http encerrada
						break 
					objeto.send(mensagem_resposta) #Envia resposta do servidor http para o browser caso ainda haja dados.
				break #Sai do loop 'for' procurando sites na whitelist
		if flag_wh!=-1:
			break # Quebra loop lidacliente para encerrar conexao com o browser para tal requisicao
				
		#VERIFICACAO DE SITES NA BLACKLIST
		for blacksite in blacklist:
			flag_bl=string.find(blacksite,site)
			if flag_bl!=-1:
				data = time.strftime("%b, %d, %Y, %H:%M:%S")
				texto_log = '%s - acesso em %s - site na blacklist\n' %(site, data)
				arqlog(texto_log)
				objeto.send(str.encode('HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Acesso Negado - WASTED</body></html>\n')) #Envia mensagem de erro caso o site esteja na blacklist
				break #Encerra loop 'for' procurando sites na blacklist
		if flag_bl!=-1:
				break #Quebra loop lidacliente para encerrar conexao com o browser para tal requisicao

				
def arqlog(site):
	arq_log = open('arq_log.txt','a') #Abre o arquivo. Se o arquivo nao existir, cria
	arq_log.writelines(site) #Imprime o site que foi tentado o acesso
	arq_log.close() #Fecha o arquivo

