# Importa o módulo socket para comunicação em rede
import socket
import threading

def escutando_servidor(conexao_socket):
    while True:
        try:
            #Fica travado aqui esperando mensagem, mas SEM travar o resto do jogo
            mensagem = conexao_socket.recv(1024).decode()
            
            if not mensagem:
                print("\n[Aviso] Conexão encerrada pelo servidor.")
                break
                
            print(f"\n[SERVIDOR]: {mensagem}")
            
            #Aqui você pode adicionar lógica, ex: se mensagem for "Sua Vez", ativa uma variável
            
        except Exception as e:
            print(f"\n[Erro] Conexão perdida com o servidor: {e}")
            break

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

thread_conexao = threading.Thread(target=escutando_servidor, args=(s,))
thread_conexao.daemon = True
thread_conexao.start()

# --- LÓGICA DO JOGO (BATALHA NAVAL) ---

# Cria um tabuleiro 10x10 (inicializado com 0, representando água)
tabuleiro = [[0] * 10 for _ in range(10)]

# Lista dos tamanhos de barcos disponíveis para posicionar
barcos = [5, 4, 3, 3, 2]


# função para imprimir o tabuleiro bonitinho (lê o tabuleiro de baixo para cima para parecer um plano cartesiano)
def print_tabuleiro(tabuleiro):
    i = 9
    while i >= 0:
        print(tabuleiro[i])
        i -= 1


# Loop que posiciona cada barco enquanto houver barcos na lista
while barcos:
    for line in tabuleiro:
        print(line)
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
            for i in range(10):
                if (pocisao_iy <= i <= pocisao_fy) or (pocisao_iy >= i >= pocisao_fy):
                    for j in range(10):
                        if(pocisao_ix <= j <= pocisao_fx) or (pocisao_ix >= j >= pocisao_fx):
                            if tabuleiro[i][j] != 0:
                                pos_livre = False
                                break
                    if not pos_livre:
                        break

            # Se todas as posições estiverem livres, marca o barco no tabuleiro
            # (valor 1 representa parte de um barco)
            if pos_livre:
                for i in range(10):
                    if (pocisao_iy <= i <= pocisao_fy) or (pocisao_iy >= i >= pocisao_fy):
                        for j in range(10):
                            if (pocisao_ix <= j <= pocisao_fx) or (pocisao_ix >= j >= pocisao_fx):
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
while True:
    pass