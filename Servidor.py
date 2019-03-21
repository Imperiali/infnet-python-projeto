import cpuinfo
import os
import pickle
import psutil
import socket
import subprocess
import platform
import nmap
import pprint


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
            print('O Usuário Solicitou Informações sobre a Máquina.')
            cpu_ram = server.uso_cpu_ram()
            cpu_info = server.cpu_info()
            proc_info = server.processador_info()
            disc_info = server.info_disco()
            server.enviar(cpu_ram=cpu_ram, cpu_info=cpu_info, proc_info=proc_info, disc_info=disc_info)

        elif '2' == msg.decode('utf-8'):
            print('O Usuário Solicitou Informações sobre Arquivos.')
            server.diretorios_arquivos()

        elif '3' == msg.decode('utf-8'):
            print('O usuário solicitou informações sobre processos.')
            server.processos_em_atividade()

        elif '4' == msg.decode('utf-8'):
            print('O Usuário solicitou informações de redes')
            server.redes_info()

        elif '5' == msg.decode('utf-8'):
            print('O Usuário solicitou verificação de hosts de determinado IP.')
            server.sub_rede()
            print('Processo de sub rede finalizado')

        elif '6' == msg.decode('utf-8'):
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
        return infos

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
        return lista

    def info_disco(self):
        """
            Função que armazena as informações de disco
        :return:
        """
        infodisco = psutil.disk_usage('.')
        return infodisco

    def processador_info(self):
        """
            Função que armazena informações do processador
        :return:
        """
        cpu_percent = psutil.cpu_count()
        cpu_percent_per_core = psutil.cpu_percent(interval=None, percpu=True)
        frequencia_cpu = psutil.cpu_freq().current
        nucleos = psutil.cpu_count(logical=False)
        return [cpu_percent,cpu_percent_per_core, frequencia_cpu, nucleos]

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

    def enviar(self, **info):
        envio = {}
        for nome, valor in info.items():
            envio[nome] = valor
        self.envia_infos(envio)

    def sub_rede(self):

        info = self.socket_client.recv(100000000)
        rick = pickle.loads(info)
        ip = rick['ip']

        print('rickIP',ip )
        print('porta', rick['portas'])
        """
            Função que varre a subrede do ip escolhido e procura por todas as máquinas conectadas e descobríveis na sub rede
        :param info: ip digitado pelo cliente
        :return: Retorna os ips da subrede nas quais existem máquinas que respondem ao ping
        """
        def retorna_codigo_ping(hostname):
            """
                Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, em sistemas linux,
            que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3   milisegundos por uma
            resposta. Esta funcao retorna o codigo de   resposta do ping
            :param hostname:
            :return:
            """

            plataforma = platform.system()
            args = []
            if plataforma == "Windows":
                args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

            else:
                args = ['ping', '-c', '1', '-W', '1', hostname]

            ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
            return ret_cod

        def verifica_hosts(base_ip):
            """
                Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram
            resposta 0 (ativo)
            :param base_ip:
            :return:
            """

            print("Mapeando\r")
            host_validos = []
            return_codes = dict()
            for i in range(1, 255):

                return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
                if i % 20 == 0:
                    print(".", end="")
                if return_codes[base_ip + '{0}'.format(i)] == 0:
                    host_validos.append(base_ip + '{0}'.format(i))

            return host_validos

        def verifica_portas(host):

            nm = nmap.PortScanner()

            nm.scan(host)
            print(nm[host].hostname())
            port =[]

            print('nmhost')
            pprint.pprint(nm[host])
            for proto in nm[host]['tcp']:

                port.append(proto)
            return port

        final = verifica_hosts(ip)
        print('final', final)
        subredes = {}

        if rick['portas']:
            for ip in final:
                subredes[ip] = verifica_portas(ip)

            print('subrede',subredes)
            self.envia_infos(subredes)
        else:
            self.envia_infos(final)

    def closeConection(self):
        self.socket_server.close()


if __name__ == '__main__':
    main()
