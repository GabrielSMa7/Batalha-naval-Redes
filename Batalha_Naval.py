# Importa o módulo socket para comunicação em rede
import socket

# Endereço e porta do servidor ao qual o cliente irá se conectar
HOST = "localhost"  # Nome do Host (servidor local)
PORT = 5000  # Porta do host

# Cria um objeto socket:
#   AF_INET    -> IPv4
#   SOCK_STREAM -> TCP (protocolo orientado a conexão)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket ao servidor no endereço e porta especificados
s.connect((HOST, PORT))
print("Conectado ao servidor")

# Envia uma mensagem codificada em bytes para o servidor
s.sendall(str.encode("Hello World"))
# Aguarda e recebe até 1024 bytes de resposta do servidor
data = s.recv(1024)
# Exibe a mensagem recebida (decodificando de bytes para string)
print("Recebido: ", data.decode())

# --- LÓGICA DO JOGO (BATALHA NAVAL) ---

# Cria um tabuleiro 10x10 (inicializado com 0, representando água)
tabuleiro = [[0] * 10 for _ in range(10)]

# Lista dos tamanhos de barcos disponíveis para posicionar
barcos = [5, 4, 3, 3, 2]


# função para imprimir o tabuleiro bonitinho
def print_tabuleiro(tabuleiro):
    i = 9
    while i >= 0:
        print(tabuleiro[i])
        i -= 1


# Loop que posiciona cada barco enquanto houver barcos na lista
while barcos:
    print_tabuleiro(tabuleiro)
    print("Barcos disponivéis:", barcos)

    # Lê as coordenadas iniciais e finais do barco (via terminal)
    pocisao_ix = int(input("Escolha coordendas inicial do barco:\nX: "))
    pocisao_iy = int(input("Y: "))
    pocisao_fx = int(input("Escolha coordendas final do barco:\nX: "))
    pocisao_fy = int(input("Y: "))

    # Se ambas as coordenadas X e Y forem diferentes, a posição é inválida
    # (o barco deve estar na horizontal OU na vertical, não diagonal)
    if pocisao_ix != pocisao_fx and pocisao_iy != pocisao_fy:
        print("Pocisão invalida")

    else:
        # Calcula o tamanho do barco com base na diferença das coordenadas
        x = pocisao_fx - pocisao_ix
        y = pocisao_fy - pocisao_iy
        tam = abs(x) + abs(y) + 1

        # Verifica se o tamanho do barco está na lista de barcos disponíveis
        if tam in barcos:
            pos_livre = True

            # Verifica se todas as posições do tabuleiro entre as coordenadas
            # inicial e final estão livres (valor 0)
            for i in range(9):
                for j in range(9):
                    if (pocisao_ix <= i <= pocisao_fx) and (
                        pocisao_iy <= j <= pocisao_fy
                    ):
                        if tabuleiro[i][j] != 0:
                            pos_livre = False
                            break
                if not pos_livre:
                    break

            # Se todas as posições estiverem livres, marca o barco no tabuleiro
            # (valor 1 representa parte de um barco)
            if pos_livre:
                for i in range(9):
                    for j in range(9):
                        if (pocisao_ix <= i <= pocisao_fx) and (
                            pocisao_iy <= j <= pocisao_fy
                        ):
                            tabuleiro[i][j] = 1

                # Remove o tamanho do barco da lista de disponíveis
                barcos.remove(tam)
            else:
                print("Posição indisponivél")
        else:
            print("Barco indisponivél \nBarcos disponivéis:", barcos)

# Envia o tabuleiro (como string codificada) para o servidor
s.sendall(str.encode(str(tabuleiro)))
# Recebe a resposta do servidor
data = s.recv(1024)
