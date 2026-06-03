import socket

HOST = 'localhost' #Nome do Host
PORT = 5000 #Porta do host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Criando o objeto do socket (Utiliza SOCK_STREAM, para conexão tcp)

s.connect((HOST, PORT)) #Conecta o socket ao endereço do host e da porta
print("Conectado ao servidor")

s.sendall(str.encode("Hello World")) #Envia os dados para o servidor
data = s.recv(1024) #Recebe os dados do servidor
print("Recebido: ", data.decode()) #Mensagem ecoada

tabuleiro = [[0] * 9 for _ in range(9)] #Criação do tabuleiro
barcos = [5, 4, 3, 3, 2]

while barcos:
    print("Barcos disponivéis:", barcos)
    pocisao_ix = int(input("Escolha coordendas inicial do barco:\nX: "))
    pocisao_iy = int(input("Y: "))
    pocisao_fx = int(input("Escolha coordendas final do barco:\nX: "))
    pocisao_fy = int(input("Y: "))

    if pocisao_ix != pocisao_fx and pocisao_iy != pocisao_fy:
        print("Pocisão invalida")

    else:
        x = pocisao_fx - pocisao_ix
        y  = pocisao_fy - pocisao_iy
        tam = abs(x) + abs(y)
        
        if tam in barcos:
            pos_livre = True

            for i in range(9):
                for j in range(9):
                    if (pocisao_ix <= i <= pocisao_fx) and (pocisao_iy <= j <= pocisao_fy):
                        if tabuleiro[i][j] != 0:
                            pos_livre = False
                            break
                if not pos_livre:
                    break
            if pos_livre:
                for i in range(9):
                    for j in range(9):
                        if (pocisao_ix <= i <= pocisao_fx) and (pocisao_iy <= j <= pocisao_fy):
                            tabuleiro[i][j] = 1
                
                barcos.remove(tam)
                print("Barcos disponivéis:", barcos)
            else:
                print("Posição indisponivél")
        else:
            print("Barco indisponivél \nBarcos disponivéis:", barcos)