# Importa o módulo socket para comunicação em rede
import socket
import threading

#--Lógica de thread--
def conexao_cliente(conn, ender):
    print("Conectando em ", ender)

    while True:
        try:
            #Recebe dados do cliente
            data = conn.recv(1024)

            #Se n receber dados corta conxão
            if not data:
                break

            #print oq recebeu
            print(f"Cliente{ender} enviou {data.decode()}")
            conn.sendall(data)

        except Exception as e:
            print(f"\n[ERRO] Conexão com {ender} perdida")
            break


#--Lógica dos sockets--
# Endereço e porta em que o servidor irá escutar por conexões
HOST = 'localhost'  # Nome do Host (escuta apenas localmente)
PORT = 5000         # Porta do host

# Cria um objeto socket:
#   AF_INET    -> indica que usaremos IPv4
#   SOCK_STREAM -> indica que usaremos TCP (protocolo orientado a conexão)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa (bind) o socket ao endereço e porta especificados
s.bind((HOST, PORT))
# Coloca o socket em modo de escuta, aguardando conexões de clientes
s.listen()

print("Aguardando conexão")

# Loop infinito para manter a comunicação com o cliente conectado
while True:
    # Aceita uma conexão de um cliente.
    # conn  -> novo socket dedicado para comunicação com este cliente
    # ender -> endereço (IP e porta) do cliente conectado
    conn, ender = s.accept()

    thread_client = threading.Thread(target=conexao_cliente, args=(conn, ender))
    thread_client.daemon = True
    thread_client.start()