import pickle
import psutil
import socket
import time


# Função que imprime a lista formatada
def formatar_cpu_mem(l):
    texto = ''
    for i in l:
        texto = texto + '{:>8.2f}'.format(i)
    print(texto)


# Função que formata processos
def formatar_processos_titulo():
    titulo = '{:^7}'.format("PID")
    titulo = titulo + '{:^11}'.format("# Threads")
    titulo = titulo + '{:^26}'.format("Criação")
    titulo = titulo + '{:^9}'.format("T. Usu.")
    titulo = titulo + '{:^9}'.format("T. Sis.")
    titulo = titulo + '{:^12}'.format("Mem. (%)")
    titulo = titulo + '{:^12}'.format("RSS")
    titulo = titulo + '{:^12}'.format("VMS")
    titulo = titulo + " Executável"
    print(titulo)


# função que formata processos
def formatar_processos_texto(pid):
    try:
        p = psutil.Process(pid)
        texto = '{:6}'.format(pid)
        texto = texto + '{:11}'.format(p.num_threads())
        texto = texto + " " + time.ctime(p.create_time()) + " "
        texto = texto + '{:8.2f}'.format(p.cpu_times().user)
        texto = texto + '{:8.2f}'.format(p.cpu_times().system)
        texto = texto + '{:10.2f}'.format(p.memory_percent()) + " MB"
        rss = p.memory_info().rss / 1024 / 1024
        texto = texto + '{:10.2f}'.format(rss) + " MB"
        vms = p.memory_info().vms / 1024 / 1024
        texto = texto + '{:10.2f}'.format(vms) + " MB"
        texto = texto + " " + p.exe()
        print(texto)
    except:
        pass


# Função que formata Redes
def redes_formatada(l):
    titulo = '{:21}'.format("Ip")
    titulo = titulo + '{:27}'.format("Netmask")
    titulo = titulo + '{:27}'.format("MAC")
    print(titulo)


# Cria o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Tenta se conectar ao servidor
cliente.connect((socket.gethostname(), 9997))

menu = cliente.recv(1024)
while True:
    # menu = s.recv(1024)
    print(menu.decode('utf-8'))
    msg1 = input('digite a opção desejada: ')
    if msg1 == '1':
        for i in range(1):  # Se for 1 faça isso
            cliente.send(msg1.encode('utf-8'))
            msg = ' '
            print('{:>8}'.format('%CPU') + '{:>8}'.format('%MEM'))
            # recebimento de informações
            recv = cliente.recv(1024)
            # conversão de dados
            lista = pickle.loads(recv)
            # CPU e memória
            formatar_cpu_mem(lista)
            info_cpu = cliente.recv(1024)
            load = pickle.loads(info_cpu)
            # prints do processador
            print('Processador: ', load['brand'])
            print('Arquitetura: ', load['arch'])
            print('Bits: ', load['bits'])
            nucleo = cliente.recv(1024)
            nucleos = pickle.loads(nucleo)
            print('Núcleos Lógicos:', nucleos)
            freq = cliente.recv(1024)
            frequencia = pickle.loads(freq)
            print('Frequência:', frequencia)
            nucleos_fisicos = cliente.recv(1024)
            nucleos = pickle.loads(nucleos_fisicos)
            print('Núcleos Físicos:', nucleos)
            disco_recv = cliente.recv(1024)
            disco = pickle.loads(disco_recv)
            print(" % de Disco Usado:", disco.percent, '%')
    elif msg1 == '2':  # Se for 2 faça isso
        cliente.send(msg1.encode('utf-8'))
        recv = cliente.recv(2048)
        lista2 = pickle.loads(recv)
        titulo = '{:11}'.format("Tamanho")  # 10 caracteres + 1 de espaço
        # Concatenar com 25 caracteres + 2 de espaços
        titulo = titulo + '{:27}'.format("Data de Modificação")
        # Concatenar com 25 caracteres + 2 de espaços
        titulo = titulo + '{:27}'.format("Data de Criação")
        titulo = titulo + "Nome"
        print(titulo)
        for i in lista2:
            kb = lista2[i][0] / 1000
            tamanho = '{:10}'.format(str('{:.2f}'.format(kb) + ' KB'))
            print(tamanho, time.ctime(lista2[i][2]), " ", time.ctime(lista2[i][1]), " ", i)
        time.sleep(1)
    elif msg1 == '3':  # Se for 3 faça isso
        cliente.send(msg1.encode('utf-8'))
        recv = cliente.recv(1024)
        dic = pickle.loads(recv)
        lista = psutil.pids()
        formatar_processos_titulo()
        for i in lista:
            formatar_processos_texto(i)
        time.sleep(2)
    elif msg1 == '4':  # Se for 4 faça isso
        cliente.send(msg1.encode('utf-8'))
        recv = cliente.recv(2048)
        dic_redes = pickle.loads(recv)
        l = ' '
        redes_formatada(l)
        ip = dic_redes['Ethernet 4'][1].address
        netmask = dic_redes['Ethernet 4'][1].netmask
        mac = dic_redes['Ethernet 4'][0].address
        print(ip, '      ', netmask, '              ', mac)
        time.sleep(2)
    elif msg1 == '5':  # Se for 5 faça isso
        cliente.send(msg1.encode('utf-8'))
        bytes = cliente.recv(1024)
        cliente.shutdown(socket.SHUT_RDWR)
        cliente.close()
        break
    else:
        print('Opção Inválida')
