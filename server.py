import socket
import ast
import time
import threading

# -- Lógica de thread --
def conexao_cliente(conn, ender):
    print("Conectando em ", ender)
    global vez

    try:
        # Recebe dados do cliente
        data = conn.recv(1024)
        if not data:
            return

        tabuleiro_recebido = ast.literal_eval(data.decode())
        tabuleiros[conn] = tabuleiro_recebido
        print(f"[TABULEIRO] Recebido de {ender}")

    except Exception as e:
        print(f"Erro ao receber tabuleiro {ender}: {e}")
        return
    
    conn.sendall(str.encode("Aguardando jogadores preencher tabuleiro\n"))
    
    # CORREÇÃO 3: time.sleep para não derreter a CPU esperando o outro jogador
    while len(tabuleiros) < 2:
        time.sleep(0.2)

    meu_id = jogadores.index(conn)
    oponente_conn = jogadores[1] if meu_id == 0 else jogadores[0]

    conn.sendall(str.encode("Partida iniciada!!\n"))

    # Variável de controle para enviar o "INI_VEZ" apenas uma vez
    aviso_espera_enviado = False

    while True:
        try:
            if vez == meu_id:
                conn.sendall(str.encode("SUA_VEZ\n"))

                coordenada = conn.recv(2056).decode()
                if not coordenada:
                    break
                
                # Trata a mensagem recebida do tiro
                x, y = map(int, coordenada.split(","))

                tabuleiro_oponente = tabuleiros[oponente_conn]

                # CORREÇÃO 2: Ajustado de [x][y] para [y][x] (Linha/Y, Coluna/X)
                if tabuleiro_oponente[y][x] == "O":
                    tabuleiro_oponente[y][x] = "X"
                    conn.sendall(str.encode("ACERTO\n"))
                    oponente_conn.sendall(str.encode(f"ATINGIDO:{x},{y}\n"))
                else:
                    conn.sendall(str.encode("ERROU\n"))
                    oponente_conn.sendall(str.encode(f"OPONENTE_ERROU:{x},{y}\n"))
                
                # Passa a vez
                vez = 1 if meu_id == 0 else 0
                
                # Reseta o aviso do turno para que, na próxima vez dele, ele saiba esperar de novo
                aviso_espera_enviado = False
            
            else:
                # CORREÇÃO 1: Envia o aviso de espera UMA ÚNICA VEZ e dorme um pouco
                if not aviso_espera_enviado:
                    conn.sendall(str.encode("INI_VEZ\n"))
                    aviso_espera_enviado = True
                
                time.sleep(0.1) # Alivia o processador enquanto espera a vez

        except Exception as e:
            print(f"\n[ERRO] Conexão com {ender} perdida: {e}")
            break

# -- Lógica dos sockets --
HOST = 'localhost'  
PORT = 5000         

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

jogadores = []
tabuleiros = {}
vez = 0

print("Servidor de Batalha Naval aguardando conexões...")

while len(jogadores) < 2:
    conn, ender = s.accept()
    jogadores.append(conn)
    print(f"Jogador {len(jogadores) - 1} conectado de {ender}") # Mostra ID 0 e ID 1 corretamente

    thread_client = threading.Thread(target=conexao_cliente, args=(conn, ender))
    thread_client.daemon = True
    thread_client.start()

# CORREÇÃO 3: Evita consumo de 100% de CPU no encerramento do script principal
while True:
    time.sleep(1)