import socket

HOST = 'localhost' #Nome do Host
PORT = 5000 #Porta do host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Criando o objeto do socket (Utiliza SOCK_STREAM, para conexão tcp)

s.connect((HOST, PORT)) #Conecta o socket ao endereço do host e da porta
print("Conectado ao servidor")

s.sendall(str.encode("Hello World")) #Envia os dados para o servidor
data = s.recv(1024) #Recebe os dados do servidor
print("Recebido: ", data.decode()) #Mensagem ecoada