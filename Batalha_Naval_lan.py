# Importa os módulos necessários para comunicação em rede e concorrência
import socket
import threading
import sys
import time

minha_vez = False
jogo = True

# Inicializa as variáveis globais de tiro como inteiros padrão
tiro_x = 0
tiro_y = 0

def escutando_servidor(conexao_socket):
    # CORREÇÃO: Adicionado tiro_x e tiro_y no global para a thread ler o valor atualizado do input
    global jogo, minha_vez, itab, tabuleiro, tiro_x, tiro_y
    buffer = ""  

    while jogo:
        try:
            dados = conexao_socket.recv(1024).decode()
            
            if not dados:
                print("\n[Aviso] Conexão encerrada pelo servidor.")
                jogo = False
                break
            
            buffer += dados
            
            while "\n" in buffer:
                mensagem, buffer = buffer.split("\n", 1)
                
                if not mensagem:
                    continue
                
                if mensagem == "SUA_VEZ":
                    print("\nÉ sua vez! Prepare o ataque.")
                    print_itabuleiro(itab)
                    minha_vez = True

                elif mensagem == "ERROU":
                    print("Você errou o alvo (água)!")
                    # CORREÇÃO: tiro_y e tiro_x agora são inteiros válidos
                    itab[tiro_y][tiro_x] = 'X'
                    # CORREÇÃO: Substituído x, y por tiro_x, tiro_y que estão no escopo correto
                    print(f"\nVocê errou a posição do inimigo ({tiro_x}, {tiro_y})!")
                    print_itabuleiro(itab)
                
                elif mensagem == "ACERTO":
                    print("Você acertou o alvo!")
                    # CORREÇÃO: tiro_y e tiro_x agora são inteiros válidos
                    itab[tiro_y][tiro_x] = 'V'
                    # CORREÇÃO: Substituído x, y por tiro_x, tiro_y que estão no escopo correto
                    print(f"\nVocê bombardeou a posição do inimigo ({tiro_x}, {tiro_y})! (FOGO!)")
                    print_itabuleiro(itab)

                elif mensagem == "INI_VEZ":
                    print("Inimigo está escolhendo o alvo...")

                elif "OPONENTE_ERROU" in mensagem:
                    print("O inimigo errou o tiro!")

                elif "ATINGIDO" in mensagem:
                    coordenadas = mensagem.split(":")[1]
                    x, y = map(int, coordenadas.split(","))
                    
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


HOST = input("Endereço IPV4:") 
PORT = 5000  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conectado ao servidor com sucesso!")

# Inicializa a Thread para escutar o servidor em paralelo
thread_conexao = threading.Thread(target=escutando_servidor, args=(s,))
thread_conexao.daemon = True
thread_conexao.start()

# --- LÓGICA DO JOGO (BATALHA NAVAL) ---

tabuleiro = [["~"] * 10 for _ in range(10)]
barcos = [5, 4, 3, 3, 2]

# CORREÇÃO: Ajustado para usar o parâmetro tab_atual recebido na função
def print_tabuleiro(tab_atual):
    print("\n--- SEU TABULEIRO ---")
    print("  0 1 2 3 4 5 6 7 8 9")
    i = 9
    while i >= 0:
        print(i, " ".join(tab_atual[i]))
        i -= 1
    print("---------------------\n")

def print_itabuleiro(tab_atual):
    print("\n--- TABULEIRO INIMIGO ---")
    print(" 0 1 2 3 4 5 6 7 8 9")
    i = 9
    while i >= 0:
        print(i, " ".join(tab_atual[i]))
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

            for i in range(10):
                if (posicao_iy <= i <= posicao_fy) or (posicao_iy >= i >= posicao_fy):
                    for j in range(10):
                        if (posicao_ix <= j <= posicao_fx) or (posicao_ix >= j >= posicao_fx):
                            if tabuleiro[i][j] != "~":
                                pos_livre = False
                                break
                    if not pos_livre:
                        break

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

itab = [["?"] * 10 for _ in range(10)]
s.sendall(str.encode(str(tabuleiro)))
print("\nTabuleiro enviado! Aguardando início do jogo...")

# Loop Principal de Turnos da Partida
while jogo:
    try:
        if minha_vez:
            # CORREÇÃO DEFINITIVA: Força a entrada a ser um número inteiro (int) e valida os limites (0 a 9)
            try:
                tiro_x = int(input("\nEscolha coordenada de tiro X: "))
                tiro_y = int(input("Escolha coordenada de tiro Y: "))
                
                if tiro_x < 0 or tiro_x > 9 or tiro_y < 0 or tiro_y > 9:
                    print("Coordenadas inválidas! Escolha números de 0 a 9.")
                    continue
            except ValueError:
                print("Por favor, digite apenas números válidos!")
                continue

            coordenada_tiro = f"{tiro_x},{tiro_y}"
            s.sendall(str.encode(coordenada_tiro))
            
            minha_vez = False
        else:
            time.sleep(0.1)

    except Exception:
        break

print("\n🏁 Fim de jogo!")
s.close()
sys.exit()