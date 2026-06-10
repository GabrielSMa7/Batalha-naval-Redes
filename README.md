# Batalha Naval em Rede Local (LAN)

## Descrição

Este projeto consiste em uma implementação do jogo **Batalha Naval** em Python com suporte para **dois jogadores conectados na mesma rede local (LAN)**.

Cada jogador posiciona seus navios em um tabuleiro 10x10 e, em seguida, os jogadores alternam turnos realizando ataques às coordenadas do adversário até o fim da partida.

A comunicação entre os jogadores é realizada através de **sockets TCP**, utilizando uma arquitetura cliente-servidor.

---

## Requisitos

* Python 3.10 ou superior
* Dois computadores conectados à mesma rede local (LAN)

Bibliotecas utilizadas:

```python
socket
threading
time
sys
ast
```

Todas fazem parte da biblioteca padrão do Python, portanto não é necessário instalar dependências adicionais.

---

## Estrutura dos Arquivos

```text
server_lan.py          -> Servidor para partidas em rede local
Batalha_Naval_lan.py   -> Cliente para jogar via LAN

server.py              -> Versão local do servidor
Batalha_Naval.py       -> Versão local do cliente
```

---

## Como Executar uma Partida em LAN

### Passo 1 – Descobrir o endereço IP do computador servidor

No computador que hospedará a partida:

#### Windows

Abra o Prompt de Comando e execute:

```bash
ipconfig
```

Procure pelo campo:

```text
Endereço IPv4
```

Exemplo:

```text
192.168.1.15
```

Anote esse endereço.

---

### Passo 2 – Iniciar o servidor

No computador servidor:

```bash
python server_lan.py
```

A seguinte mensagem deverá aparecer:

```text
Servidor de Batalha Naval aguardando conexões...
```

Mantenha esta janela aberta.

---

### Passo 3 – Conectar o Jogador 1

No primeiro computador jogador:

```bash
python Batalha_Naval_lan.py
```

Quando solicitado:

```text
Endereço IPV4:
```

Digite o endereço IP do computador servidor.

Exemplo:

```text
192.168.1.15
```

---

### Passo 4 – Conectar o Jogador 2

No segundo computador jogador:

```bash
python Batalha_Naval_lan.py
```

Digite o mesmo endereço IP do servidor.

Exemplo:

```text
192.168.1.15
```

---

### Passo 5 – Posicionar os Navios

Cada jogador deverá posicionar os seguintes navios:

```text
Tamanho 5
Tamanho 4
Tamanho 3
Tamanho 3
Tamanho 2
```

Para cada navio serão solicitadas:

```text
Coordenada inicial (X,Y)
Coordenada final (X,Y)
```

Os navios devem ser posicionados:

* Horizontalmente ou verticalmente;
* Dentro do tabuleiro;
* Sem sobrepor outros navios.

---

### Passo 6 – Início da Partida

Após os dois jogadores enviarem seus tabuleiros, o jogo será iniciado automaticamente.

O jogador da vez receberá a mensagem:

```text
É sua vez! Prepare o ataque.
```

---

### Passo 7 – Realizar Ataques

Quando for sua vez, informe:

```text
Escolha coordenada de tiro X:
Escolha coordenada de tiro Y:
```

Exemplo:

```text
X = 4
Y = 7
```

O sistema informará:

```text
Você acertou o alvo!
```

ou

```text
Você errou o alvo!
```

---

## Representação do Tabuleiro

### Seu Tabuleiro

```text
O -> Navio
X -> Navio atingido
~ -> Água
```

### Tabuleiro do Inimigo

```text
? -> Posição desconhecida
V -> Acerto
X -> Tiro na água
```

---

## Observações

* O servidor utiliza a porta TCP 5000.
* Caso o firewall bloqueie a conexão, permita o acesso do Python à rede.
* Todos os jogadores devem estar conectados à mesma rede local.
* O servidor deve ser iniciado antes dos clientes.

---

## Autores

Projeto desenvolvido para a disciplina de Redes de Computadores utilizando Python, sockets TCP e programação concorrente com threads.
