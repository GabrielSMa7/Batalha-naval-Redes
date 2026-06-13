import socket
import ast
import time
import threading

# Lock para proteger variável global 'vez'
vez_lock = threading.Lock()

# -- Lógica de thread --
def conexao_cliente(conn, ender):
    print("Conectando em ", ender)
    global vez
    oponente_conn = None

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

    try:
        conn.sendall(str.encode("Partida iniciada!!\n"))
    except Exception:
        return

    # Variável de controle para enviar o "INI_VEZ" apenas uma vez
    aviso_espera_enviado = False

    probe_buffer = b''
    while True:
        try:
            with vez_lock:
                minha_vez_atual = (vez == meu_id)
            
            if minha_vez_atual:
                conn.sendall(str.encode("SUA_VEZ\n"))

                # Inclui byte do probe se houver
                dados = probe_buffer + conn.recv(2056)
                probe_buffer = b''
                coordenada = dados.decode()
                if not coordenada:
                    if oponente_conn:
                        try:
                            oponente_conn.sendall(str.encode("OPONENTE_DESCONECTOU\n"))
                        except:
                            pass
                    break
                
                # Trata a mensagem recebida do tiro
                x, y = map(int, coordenada.split(","))

                tabuleiro_oponente = tabuleiros[oponente_conn]

                # CORREÇÃO 2: Ajustado de [x][y] para [y][x] (Linha/Y, Coluna/X)
                if tabuleiro_oponente[y][x] == "O":
                    tabuleiro_oponente[y][x] = "X"
                    conn.sendall(str.encode("ACERTO\n"))
                    oponente_conn.sendall(str.encode(f"ATINGIDO:{x},{y}\n"))
                    
                    # Verifica condicao de vitoria
                    if all("O" not in linha for linha in tabuleiro_oponente):
                        conn.sendall(str.encode("VENCEU\n"))
                        oponente_conn.sendall(str.encode("PERDEU\n"))
                        break
                else:
                    conn.sendall(str.encode("ERROU\n"))
                    oponente_conn.sendall(str.encode(f"OPONENTE_ERROU:{x},{y}\n"))
                
                # Passa a vez
                with vez_lock:
                    vez = 1 if meu_id == 0 else 0
                
                # Reseta o aviso do turno para que, na próxima vez dele, ele saiba esperar de novo
                aviso_espera_enviado = False
            
            else:
                # CORREÇÃO 1: Envia o aviso de espera UMA ÚNICA VEZ e dorme um pouco
                if not aviso_espera_enviado:
                    conn.sendall(str.encode("INI_VEZ\n"))
                    aviso_espera_enviado = True
                
                # Probe de conexão para detectar desconexão fora do turno
                try:
                    conn.settimeout(0.05)
                    data = conn.recv(1)
                    if not data:
                        if oponente_conn:
                            try:
                                oponente_conn.sendall(str.encode("OPONENTE_DESCONECTOU\n"))
                            except:
                                pass
                        break
                    elif data:
                        # Byte legítimo recebido — buffer para próxima leitura real
                        probe_buffer = data
                except socket.timeout:
                    pass
                except:
                    if oponente_conn:
                        try:
                            oponente_conn.sendall(str.encode("OPONENTE_DESCONECTOU\n"))
                        except:
                            pass
                    break
                finally:
                    conn.settimeout(None)
                
                time.sleep(0.1) # Alivia o processador enquanto espera a vez

        except Exception as e:
            print(f"\n[ERRO] Conexão com {ender} perdida: {e}")
            if oponente_conn:
                try:
                    oponente_conn.sendall(str.encode("OPONENTE_DESCONECTOU\n"))
                except:
                    pass
            break

# -- Lógica dos sockets --
HOST = 'localhost'  
PORT = 5000         

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Servidor de Batalha Naval aguardando conexões...")

while True:  # Loop eterno de partidas
    jogadores = []
    tabuleiros = {}
    with vez_lock:
        vez = 0
    threads_ativas = []
    
    print("\n=== Nova partida: aguardando 2 jogadores ===\n")
    
    # Aceita 2 jogadores
    while len(jogadores) < 2:
        conn, ender = s.accept()
        jogadores.append(conn)
        print(f"Jogador {len(jogadores) - 1} conectado de {ender}")
        
        thread_client = threading.Thread(target=conexao_cliente, args=(conn, ender))
        thread_client.daemon = False
        thread_client.start()
        threads_ativas.append(thread_client)
    
    # Aguarda AMBAS threads terminarem (jogo acabou)
    for t in threads_ativas:
        t.join()
    threads_ativas.clear()
    
    print("--- Partida encerrada. Nova partida disponível ---\n")