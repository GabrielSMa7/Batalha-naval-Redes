# Importa o módulo socket para comunicação em rede
import socket

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

# Aceita uma conexão de um cliente.
# conn  -> novo socket dedicado para comunicação com este cliente
# ender -> endereço (IP e porta) do cliente conectado
conn, ender = s.accept()

print("Conectando em ", ender)

# Loop infinito para manter a comunicação com o cliente conectado
while True:
    # Recebe até 1024 bytes de dados enviados pelo cliente
    data = conn.recv(1024)
    # Se não receber dados, o cliente encerrou a conexão
    if not data:
        break
    # Exibe os dados recebidos (decodificando de bytes para string)
    print("Recebido: ", data.decode())
    # Envia os dados de volta para o cliente (eco)
    conn.sendall(data)