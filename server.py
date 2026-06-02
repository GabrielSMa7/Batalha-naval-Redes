import socket

HOST = 'localhost' #Nome do Host
PORT = 5000 #Porta do host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Criando o objeto do socket (Utiliza SOCK_STREAM, para conexão tcp)
s.bind((HOST, PORT)) #Adiciona o endereço do host e da porta no socket
s.listen() #Coloca o socket em modo de escuta

print("Aguardando conexão")

conn, ender = s.accept() #Conexão e endereço

print("Conectando em ", ender)

while True:
    data = conn.recv(1024) #Recebe os dados do cliente
    if not data:
        break
    print("Recebido: ", data.decode()) #Exibe os dados recebidos
    conn.sendall(data) #Envia os dados de volta para o cliente