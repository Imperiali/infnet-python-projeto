import cpuinfo
import os
import pickle
import psutil
import socket


# region Metodos


# endregion

# # Cria o socket
# socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # pega o nome da máquina
# host = socket.gethostname()
# porta = 9997
#
# # Associa a porta
# socket_servidor.bind((host, porta))
#
# # Escuta a porta
# socket_servidor.listen()
# print("Servidor", host, "esperando conexão na porta", porta)
#
# # Aceita a conexão
# (socket_cliente, addr) = socket_servidor.accept()
# print("Conectado a:", str(addr))

# # Declaração do Menu
# info = ("\n ***********************MENU******************************"
#         "\n *************1 - Informações da Máquina *****************"
#         "\n *************2- Informações de Arquivos *****************"
#         "\n *************3- Informações Processos Ativos ************"
#         "\n *************4 -Informações de Redes ********************"
#         "\n *************5- Sair ************************************"
#         "\n *********************************************************")
# socket_cliente.send(info.encode('utf-8'))  # Envia resposta


def main():
    """
        Metodo para fazer toda a aplicação rodar
    :return:
    """
    server = Server()
    server.waitConection()
    while True:
        msg = server.socket_client.recv(1024)

        if '1' == msg.decode('utf-8'):
            server.uso_cpu_ram()
            server.cpu_info()
            server.processador_info()
            server.info_disco()
            print('O Usuário Solicitou Informações sobre a Máquina.')

        elif '2' == msg.decode('utf-8'):
            server.diretorios_arquivos()
            print('O Usuário Solicitou Informações sobre Arquivos.')

        elif '3' == msg.decode('utf-8'):
            server.processos_em_atividade()
            print('O usuário solicitou informações sobre processos.')

        elif '4' == msg.decode('utf-8'):
            server.redes_info()
            print('O Usuário solicitou informações de redes')

        elif '5' == msg.decode('utf-8'):
            server.sair_da_conexao()
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

    def cpu_info(self):
        """
            Função que armazena as informações da CPU
        :return:
        """
        infos = cpuinfo.get_cpu_info()
        self.envia_infos(infos)

    def uso_cpu_ram(self):
        """
            Função que armazena uso de CPU e RAM
        :return:
        """
        lista = []
        lista.append(psutil.cpu_percent())
        mem_virtual = psutil.virtual_memory()
        mem_percent = mem_virtual.used / mem_virtual.total
        lista.append(mem_percent)
        self.envia_infos(lista)

    def info_disco(self):
        """
            Função que armazena as informações de disco
        :return:
        """
        infodisco = psutil.disk_usage('.')
        self.envia_infos(infodisco)

    def processador_info(self):
        """
            Função que armazena informações do processador
        :return:
        """
        cpu_percent = psutil.cpu_count()
        frequencia_cpu = psutil.cpu_freq().current
        nucleos = psutil.cpu_count(logical=False)
        self.envia_infos(cpu_percent)
        self.envia_infos(frequencia_cpu)
        self.envia_infos(nucleos)

    def diretorios_arquivos(self):
        """
            Função para armazenar arquivos e diretórios
        :return:
        """
        lista = os.listdir()
        dic = {}
        for i in lista:
            if os.path.isfile(i):
                dic[i] = []
                dic[i].append(os.stat(i).st_size)
                dic[i].append(os.stat(i).st_atime)
                dic[i].append(os.stat(i).st_mtime)
        self.envia_infos(dic)

    def processos_em_atividade(self):
        """
            Função que armazena processos em atividades na máquina
        :return:
        """
        dic = psutil.pids()
        self.envia_infos(dic)

    def redes_info(self):
        """
            Função que retorna os endereços de rede
        :return:
        """
        interfaces_dic = psutil.net_if_addrs()
        self.envia_infos(interfaces_dic)

    def envia_infos(self, info):
        resposta = pickle.dumps(info)
        self.socket_client.send(resposta)

    def sair_da_conexao(self):
        """
            Função que encerra a conexão
        :return:
        """
        info = 'Conexão Encerrada!'
        self.socket_client.send(info.encode('utf-8'))
        print("Fechando Conexão com", str(self.endereco_cliente), "...")
        self.socket_client.shutdown(socket.SHUT_RDWR)
        self.socket_client.close()

    def closeConection(self):
        self.socket_server.close()


if __name__ == '__main__':
    main()
