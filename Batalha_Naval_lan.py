# Importa os módulos necessários para comunicação em rede e concorrência
import socket
import threading
import sys
import time

minha_vez = False
jogo = True

def escutando_servidor(conexao_socket):
    global jogo, minha_vez
    buffer = ""  # CORREÇÃO DEFINITIVA: Armazena fragmentos de texto da rede

    while jogo:
        try:
            # Fica travado aqui esperando dados da rede
            dados = conexao_socket.recv(1024).decode()
            
            if not dados:
                print("\n[Aviso] Conexão encerrada pelo servidor.")
                jogo = False
                break
            
            # Acumula o que chegou no buffer
            buffer += dados
            
            # Processa todas as mensagens completas terminadas em \n
            while "\n" in buffer:
                mensagem, buffer = buffer.split("\n", 1)
                
                if not mensagem:
                    continue
                
                # Protocolo de checagem seguro contra pacotes colados
                if mensagem == "SUA_VEZ":
                    print("\nÉ sua vez! Prepare o ataque.")
                    minha_vez = True

                elif mensagem == "ERROU":
                    print("Você errou o alvo (água)!")
                
                elif mensagem == "ACERTO":
                    print("Você acertou o alvo!")

                elif mensagem == "INI_VEZ":
                    print("Inimigo está escolhendo o alvo...")

                elif "OPONENTE_ERROU" in mensagem:
                    print("O inimigo errou o tiro!")

                elif "ATINGIDO" in mensagem:
                    coordenadas = mensagem.split(":")[1]
                    x, y = map(int, coordenadas.split(","))
                    
                    # CORREÇÃO: Alinhado para [y][x] para casar com a estrutura de linhas do tabuleiro
                    tabuleiro[y][x] = 'X'
                    print(f"\nO inimigo bombardeou sua posição ({x}, {y})!")
                    print_tabuleiro(tabuleiro)

                else:
                    print(f"\n[SERVIDOR]: {mensagem}")
            
        except Exception as e:
            print(f"\n[Erro] Conexão perdida com o servidor: {e}")
            jogo = False
            break

# Endereço e porta do servidor
HOST = "localhost" #endereço do IPV4 do servidor   
PORT = 5000  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conectado ao servidor com sucesso!")

# Inicializa a Thread para escutar o servidor em paralelo
thread_conexao = threading.Thread(target=escutando_servidor, args=(s,))
thread_conexao.daemon = True
thread_conexao.start()

# --- LÓGICA DO JOGO (BATALHA NAVAL) ---

# Cria um tabuleiro 10x10 (inicializado com "~", representando água)
tabuleiro = [["~"] * 10 for _ in range(10)]
barcos = [5, 4, 3, 3, 2]

# Função para imprimir o tabuleiro de baixo para cima (plano cartesiano)
def print_tabuleiro(tab_atual):
    print("\n--- SEU TABULEIRO ---")
    i = 9
    while i >= 0:
        print(" ".join(tab_atual[i]))
        i -= 1
    print("---------------------\n")

# Loop que posiciona cada barco
while barcos:
    print_tabuleiro(tabuleiro)
    print("Barcos disponíveis para posicionar (tamanhos):", barcos)

    try:
        posicao_ix = int(input("Escolha coordenada INICIAL do barco:\nX: "))
        posicao_iy = int(input("Y: "))
        posicao_fx = int(input("Escolha coordenada FINAL do barco:\nX: "))
        posicao_fy = int(input("Y: "))
    except ValueError:
        print("Por favor, insira apenas números inteiros!")
        continue

    coordenadas = [posicao_fx, posicao_fy, posicao_ix, posicao_iy]
    fora_tabuleiro = any(c < 0 or c > 9 for c in coordenadas)
    
    if (posicao_ix != posicao_fx and posicao_iy != posicao_fy) or fora_tabuleiro:
        print("Posição inválida!")
    else:
        x = posicao_fx - posicao_ix
        y = posicao_fy - posicao_iy
        tam = abs(x) + abs(y) + 1

        if tam in barcos:
            pos_livre = True

            # Verifica se todas as posições estão livres
            for i in range(10):
                if (posicao_iy <= i <= posicao_fy) or (posicao_iy >= i >= posicao_fy):
                    for j in range(10):
                        if (posicao_ix <= j <= posicao_fx) or (posicao_ix >= j >= posicao_fx):
                            if tabuleiro[i][j] != "~":
                                pos_livre = False
                                break
                    if not pos_livre:
                        break

            # Se livre, posiciona marcando com "O"
            if pos_livre:
                for i in range(10):
                    if (posicao_iy <= i <= posicao_fy) or (posicao_iy >= i >= posicao_fy):
                        for j in range(10):
                            if (posicao_ix <= j <= posicao_fx) or (posicao_ix >= j >= posicao_fx):
                                tabuleiro[i][j] = "O"
                barcos.remove(tam)
            else:
                print("Posição indisponível!")
        else:
            print(f"Você não tem um barco de tamanho {tam}.")

# Envia o tabuleiro finalizado para o servidor iniciar a partida
s.sendall(str.encode(str(tabuleiro)))
print("\nTabuleiro enviado! Aguardando início do jogo...")

# Loop Principal de Turnos da Partida
while jogo:
    try:
        if minha_vez:
            tiro_x = input("\nEscolha coordenada de tiro X: ")
            tiro_y = input("Escolha coordenada de tiro Y: ")

            coordenada_tiro = f"{tiro_x},{tiro_y}"
            s.sendall(str.encode(coordenada_tiro))
            
            minha_vez = False
        else:
            # CORREÇÃO: Evita que o programa gaste 100% da sua CPU rodando em vazio
            time.sleep(0.1)

    except Exception:
        break

print("\n🏁 Fim de jogo!")
s.close()
sys.exit()