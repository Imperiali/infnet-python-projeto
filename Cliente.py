import pickle
import psutil
import socket
import time
import pprint


msgInicial = ("\n ██▓███   ██▀███   ▒█████   ▄▄▄██▀▀▀▓█████▄▄▄█████▓ ▒█████     ▓█████▄ ▓█████     ▄▄▄▄    ██▓     ▒█████   ▄████▄   ▒█████  "
      "\n▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒   ▒██   ▓█   ▀▓  ██▒ ▓▒▒██▒  ██▒   ▒██▀ ██▌▓█   ▀    ▓█████▄ ▓██▒    ▒██▒  ██▒▒██▀ ▀█  ▒██▒  ██▒"
      "\n▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒   ░██   ▒███  ▒ ▓██░ ▒░▒██░  ██▒   ░██   █▌▒███      ▒██▒ ▄██▒██░    ▒██░  ██▒▒▓█    ▄ ▒██░  ██▒"
        "\n▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░▓██▄██▓  ▒▓█  ▄░ ▓██▓ ░ ▒██   ██░   ░▓█▄   ▌▒▓█  ▄    ▒██░█▀  ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▒██   ██░"
        "\n▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░ ▓███▒   ░▒████▒ ▒██▒ ░ ░ ████▓▒░   ░▒████▓ ░▒████▒   ░▓█  ▀█▓░██████▒░ ████▓▒░▒ ▓███▀ ░░ ████▓▒░"
        "\n▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░  ▒▓▒▒░   ░░ ▒░ ░ ▒ ░░   ░ ▒░▒░▒░     ▒▒▓  ▒ ░░ ▒░ ░   ░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░░ ▒░▒░▒░ "
        "\n░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░  ▒ ░▒░    ░ ░  ░   ░      ░ ▒ ▒░     ░ ▒  ▒  ░ ░  ░   ▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒     ░ ▒ ▒░ "
        "\n░░         ░░   ░ ░ ░ ░ ▒   ░ ░ ░      ░    ░      ░ ░ ░ ▒      ░ ░  ░    ░       ░    ░   ░ ░   ░ ░ ░ ▒  ░        ░ ░ ░ ▒  "
                    "\n░         ░ ░   ░   ░      ░  ░            ░ ░        ░       ░  ░    ░          ░  ░    ░ ░  ░ ░          ░ ░  "
                                                                        "\n░                      ░                  ░                 ")

info = ("\n -----------------------MENU------------------------------"
        "\n 1 - Informações da Máquina "
        "\n 2 - Informações de Arquivos "
        "\n 3 - Informações Processos Ativos "
        "\n 4 - Informações de Redes "
        "\n 5 - Sub Rede "
        "\n 6 - Sair "
        "\n ---------------------------------------------------------")


class Client:

    """
       Classe responsavel pelo lado do cliente
   """

    def __init__(self):
        """
            Instanciando o cliente, conecta ele ao servidor
        """
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endereco = socket.gethostname()
        self.porta = 9997
        self.socket_client.connect((self.endereco, self.porta))
        self.menu = info
        self.apresentacao = msgInicial
        print('Cliente iniciado')

    def formatar_cpu_mem(self, lista):
        """
            Função que imprime a lista formatada
        :return:
        """
        texto = ''
        for i in lista:
            texto = texto + f'{round(i, 2)}'
        print(texto)

    def formatar_processos_titulo(self):
        """
            Função que formata titulo dos processos
        :return:
        """
        titulo = f'{" "*2}PID {" "*6}Mem.(%) Executável'

        print(titulo)

    def formatar_processos_texto(self, pid):
        """
            função que formata processos
        :return:
        """
        try:
            p = psutil.Process(pid)
            texto = f'{pid:6d}'
            vms = p.memory_info().vms / 1024 / 1024
            texto = texto + f'{vms:10.2f} MB'
            texto = texto + " " + p.exe()
            print(texto)
        except:
            pass

    def redes_formatada(self):
        """
            # Função que formata Redes
        :return:
        """
        titulo = '{:21}'.format("Ip")
        titulo = titulo + '{:27}'.format("Netmask")
        titulo = titulo + '{:27}'.format("MAC")
        print(titulo)

    def opcao1(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        msg = ' '
        # print('{:>8}'.format('%CPU') + '{:>8}'.format('%MEM'))


        recv = self.socket_client.recv(2048)

        lista = pickle.loads(recv)

        print('%CPU:', lista['cpu_ram'][0])
        print('%MEM:', lista['cpu_ram'][1])
        # self.formatar_cpu_mem(lista['cpu_ram'])

        load = lista['cpu_info']

        print('Processador: ', load['brand'])
        print('Arquitetura: ', load['arch'])
        print('Bits: ', load['bits'])

        nucleos = lista['proc_info']

        print('Núcleos Lógicos:', nucleos[0])

        print('%CPU por Núcleo', nucleos[1])

        print('Frequência:', nucleos[2])

        print('Núcleos Físicos:', nucleos[3])


        disco = lista['disc_info']

        print(" % de Disco Usado:", disco.percent, '%')

    def opcao2(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        recv = self.socket_client.recv(2048)
        lista2 = pickle.loads(recv)
        titulo = '{:11}'.format("Tamanho")
        titulo = titulo + '{:27}'.format("Data de Modificação")
        titulo = titulo + '{:27}'.format("Data de Criação")
        titulo = titulo + "Nome"
        print(titulo)
        for i in lista2:
            kb = lista2[i][0] / 1000
            tamanho = '{:10}'.format(str('{:.2f}'.format(kb) + ' KB'))
            print(tamanho, time.ctime(lista2[i][2]), " ", time.ctime(lista2[i][1]), " ", i)
        time.sleep(1)

    def opcao3(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        recv = self.socket_client.recv(1024)
        dic = pickle.loads(recv)
        lista = psutil.pids()
        self.formatar_processos_titulo()
        for i in lista:
            self.formatar_processos_texto(i)
        time.sleep(2)

    def opcao4(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        recv = self.socket_client.recv(2048)
        dic_redes = pickle.loads(recv)
        self.redes_formatada()

        ethernet = []

        for key in dic_redes:
            if key.startswith('Ethernet'):
                ethernet.append(key)

        ip = dic_redes[ethernet[0]][1].address
        netmask = dic_redes[ethernet[0]][1].netmask
        mac = dic_redes[ethernet[0]][0].address
        print(ip, '      ', netmask, '              ', mac)
        time.sleep(2)

    def opcao5(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        ip_complete = input('Digite o Ip para verificar as portas: ')

        portasInput = input('Deseja verificar as portas?[S/n]')

        ipPortas = {}

        while True:

            if portasInput.lower() == 's' or portasInput == '':
                ipPortas['portas'] = True
                break
            elif portasInput.lower() == 'n':
                ipPortas['portas'] = False
                break
            else:
                print('Por favor, digite S ou N')
                portasInput = input('Deseja verificar as portas?[S/n]')

        info_incomplete = ip_complete.split('.')
        info = ".".join(info_incomplete[0:3]) + '.'

        # LOADING ...
        ipPortas['ip'] = info

        info_complete = pickle.dumps(ipPortas)
        self.socket_client.send(info_complete)

        recv = self.socket_client.recv(100000000)

        sub_net = pickle.loads(recv)

        print("O teste será feito na sub rede: ", info)
        print('\n Os host válidos são:')
        pprint.pprint(sub_net)

    def opcao6(self, msg1):
        self.socket_client.send(msg1.encode('utf-8'))
        bytes = self.socket_client.recv(1024)
        self.socket_client.shutdown(socket.SHUT_RDWR)
        self.socket_client.close()


def main():

    cliente = Client()

    print(cliente.apresentacao)
    while True:
        print(cliente.menu)
        msg1 = input('digite a opção desejada: ')
        if msg1 == '1':
            cliente.opcao1(msg1)

        elif msg1 == '2':
            cliente.opcao2(msg1)

        elif msg1 == '3':
            cliente.opcao3(msg1)

        elif msg1 == '4':
            cliente.opcao4(msg1)

        elif msg1 == '5':
            cliente.opcao5(msg1)

        elif msg1 == '6':
            cliente.opcao6(msg1)
            break
        else:
            print('Opção Inválida')


if __name__ == '__main__':
    main()
