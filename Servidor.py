import cpuinfo
import os
import pickle
import psutil
import socket

#region Metodos

# Definição das Funções
def cpu_info(socket_cliente):  # Função que armazena as informações da CPU
    infos = cpuinfo.get_cpu_info()
    dados_enviados = pickle.dumps(infos)
    socket_cliente.send(dados_enviados)


def uso_cpu_ram(socket_cliente):  # Função que armazena uso de CPU e RAM
    # Gera a lista de resposta
    lista = []
    lista.append(psutil.cpu_percent())
    mem_virtual = psutil.virtual_memory()
    mem_percent = mem_virtual.used / mem_virtual.total
    lista.append(mem_percent)
    # Prepara a lista para o envio
    bytes_resposta = pickle.dumps(lista)
    # Envia os dados
    socket_cliente.send(bytes_resposta)  # Envia mensagem


def info_disco(socket_cliente):  # Função que armazena as informações de disco
    infodisco = psutil.disk_usage('.')
    dadosenviados = pickle.dumps(infodisco)
    socket_cliente.send(dadosenviados)


def processador_info(socket_cliente):  # Função que armazena informações do processador
    cpu_percent = psutil.cpu_count()  # % de cpu por núcleos
    frequencia_cpu = psutil.cpu_freq().current  # frequencia total
    nucleos = psutil.cpu_count(logical=False)  # nº de núcleos e Threads
    dados_cpu_percent = pickle.dumps(cpu_percent)
    dados_frequencia_cpu = pickle.dumps(frequencia_cpu)
    dados_nucleos = pickle.dumps(nucleos)
    socket_cliente.send(dados_cpu_percent)
    socket_cliente.send(dados_frequencia_cpu)
    socket_cliente.send(dados_nucleos)


def diretorios_arquivos(socket_cliente):  # Função para armazenar arquivos e diretórios
    # obtém lista de arquivos e diretórios
    lista = os.listdir()
    # Cria um dicionário
    dic = {}
    for i in lista:  # varia na lista dos arquivos e diretórios
        if os.path.isfile(i):  # checa se é um arquivo
            dic[i] = []
            dic[i].append(os.stat(i).st_size)  # tamanho
            dic[i].append(os.stat(i).st_atime)  # tempo de criação
            dic[i].append(os.stat(i).st_mtime)  # Tempo de Modificação
    resposta = pickle.dumps(dic)
    # Envia os dados
    socket_cliente.send(resposta)  # Envia mensagem


def processos_em_atividade(socket_cliente):  # Função que armazena processos em atividades na máquina
    dic = psutil.pids()
    resposta = pickle.dumps(dic)
    socket_cliente.send(resposta)  # Envia mensagem


def redes_info(socket_cliente):  # Função que retorna os endereços de rede
    interfaces_dic = psutil.net_if_addrs()
    resposta = pickle.dumps(interfaces_dic)
    socket_cliente.send(resposta)  # Envia mensagem


def sair_da_conexao(socket_cliente):  # Função que encerra a conexão
    info = ('Conexão Encerrada!')
    socket_cliente.send(info.encode('utf-8'))
    print("Fechando Conexão com", str(addr), "...")
    socket_cliente.shutdown(socket.SHUT_RDWR)
    socket_cliente.close()

#endregion

projetoDeBloco = ("\n ██▓███   ██▀███   ▒█████   ▄▄▄██▀▀▀▓█████▄▄▄█████▓ ▒█████     ▓█████▄ ▓█████     ▄▄▄▄    ██▓     ▒█████   ▄████▄   ▒█████  "
      "\n▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒   ▒██   ▓█   ▀▓  ██▒ ▓▒▒██▒  ██▒   ▒██▀ ██▌▓█   ▀    ▓█████▄ ▓██▒    ▒██▒  ██▒▒██▀ ▀█  ▒██▒  ██▒"
      "\n▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒   ░██   ▒███  ▒ ▓██░ ▒░▒██░  ██▒   ░██   █▌▒███      ▒██▒ ▄██▒██░    ▒██░  ██▒▒▓█    ▄ ▒██░  ██▒"
        "\n▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░▓██▄██▓  ▒▓█  ▄░ ▓██▓ ░ ▒██   ██░   ░▓█▄   ▌▒▓█  ▄    ▒██░█▀  ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▒██   ██░"
        "\n▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░ ▓███▒   ░▒████▒ ▒██▒ ░ ░ ████▓▒░   ░▒████▓ ░▒████▒   ░▓█  ▀█▓░██████▒░ ████▓▒░▒ ▓███▀ ░░ ████▓▒░"
        "\n▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░  ▒▓▒▒░   ░░ ▒░ ░ ▒ ░░   ░ ▒░▒░▒░     ▒▒▓  ▒ ░░ ▒░ ░   ░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░░ ▒░▒░▒░ "
        "\n░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░  ▒ ░▒░    ░ ░  ░   ░      ░ ▒ ▒░     ░ ▒  ▒  ░ ░  ░   ▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒     ░ ▒ ▒░ "
        "\n░░         ░░   ░ ░ ░ ░ ▒   ░ ░ ░      ░    ░      ░ ░ ░ ▒      ░ ░  ░    ░       ░    ░   ░ ░   ░ ░ ░ ▒  ░        ░ ░ ░ ▒  "
                    "\n░         ░ ░   ░   ░      ░  ░            ░ ░        ░       ░  ░    ░          ░  ░    ░ ░  ░ ░          ░ ░  "
                                                                        "\n░                      ░                  ░                 ")

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# pega o nome da máquina
host = socket.gethostname()
porta = 9997

# Associa a porta
socket_servidor.bind((host, porta))

# Escuta a porta
socket_servidor.listen()
print("Servidor", host, "esperando conexão na porta", porta)

# Aceita a conexão
(socket_cliente, addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

# Declaração do Menu
info = ("\n ***********************MENU******************************"
        "\n *************1 - Informações da Máquina *****************"
        "\n *************2- Informações de Arquivos *****************"
        "\n *************3- Informações Processos Ativos ************"
        "\n *************4 -Informações de Redes ********************"
        "\n *************5- Sair ************************************"
        "\n *********************************************************")
socket_cliente.send(info.encode('utf-8'))  # Envia resposta


while True:
    # Decodifica mensagem em UTF-8:
    msg = socket_cliente.recv(1024)

    if '1' == msg.decode('utf-8'):  # se for 1 executar isso
        uso_cpu_ram(socket_cliente)
        cpu_info(socket_cliente)
        processador_info(socket_cliente)
        info_disco(socket_cliente)
        print('O Usuário Solicitou Informações sobre a Máquina.')

    elif '2' == msg.decode('utf-8'):  # se for 2 executar isso
        diretorios_arquivos(socket_cliente)
        print('O Usuário Solicitou Informações sobre Arquivos.')

    elif '3' == msg.decode('utf-8'):  # se for 3 executar isso
        processos_em_atividade(socket_cliente)
        print('O usuário solicitou informações sobre processos.')

    elif '4' == msg.decode('utf-8'):  # se for 4 executar isso
        redes_info(socket_cliente)
        print('O Usuário solicitou informações de redes')

    elif '5' == msg.decode('utf-8'):  # se for 5 executar isso
        sair_da_conexao(socket_cliente)
        break

    else:
        print('O usuário Digitou opções invalidas.')


class Server:
    """
        Classe referente ao lado do servidor
    """

    def __init__(self):
        """
            Ao instanciar a classe, associa o socket na porta e ao endereço
        """
        self.info = ''
        self.socket_client = ''
        self.endereco_cliente = ''
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endereco = socket.gethostname()
        self.porta = 9997
        self.socket_server.bind((self.endereco, self.porta))
        print('Servidor iniciado')

    def waitConection(self):
        """
            Começa a esperar uma conexão de um cliente
        :return:
        """
        print('Esperando conexão do cliente...')
        self.socket_server.listen()
        (self.socket_client, self.endereco_cliente) = self.socket_server.accept()
        print(f'Cliente conectado!: {self.endereco_cliente}')









