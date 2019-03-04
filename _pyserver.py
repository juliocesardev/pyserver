#####################################
# 
#       autor: @juliocesar.dev
#       created: 02-3-2019
#
#####################################
# Lista de modules que perciso
# Socket    (ligacao)
# Sys       (sistema)
# _Thread   (trefas)
# DateTime  (Dias e segundos e ..)
# Time      (Tempo)
import socket, sys, _thread, time
#
from datetime import datetime
# Lista de data de cada cliente ligado
list_clients = []
# Metodo para criar servidor
# Inicio metodoCriarServidor
def createNewServer(server_host, server_port, max_connections = 2, max_connections_wait = 4, buffer_size = 1024):
    # Socket do servidor
    server_socket = None
    # Tenta criar socket
    try:
        # Socket
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        # Print
        print( "[{0}] Socket criado".format(datetime.fromtimestamp(int(time.time())).time()) )
    # Caso houver erro
    except:
        # Print
        print( "[{0}] Erro ao criar socket".format(datetime.fromtimestamp(int(time.time())).time()) )
        # Fecha apiclacao
        sys.exit(0)
    # Bind socket
    try:
        server_socket.bind(
            (server_host, server_port)
        )
        # Print
        address_ip_modif = server_host
        if not server_host:
            address_ip_modif = 'all'
        #
        print( "[{0}] Socket ligado a {1}:{2}.".format(datetime.fromtimestamp(int(time.time())).time(), address_ip_modif, server_port) )
        #
        print( "[{0}] Maximo de clientes: {1}".format(datetime.fromtimestamp(int(time.time())).time(), str(max_connections)) )
    # Caso houver erro
    except:
        # Print
        print( "[{0}] Ocorreu um erro ao tentar ligar em {1}:{2}.".format(datetime.fromtimestamp(int(time.time())).time(), server_host, server_port) )
        # Print
        print( "[{0}] Erro {1}".format(datetime.fromtimestamp(int(time.time())).time(), server_socket) )
        # Fecha apiclacao
        sys.exit(0)
    # Esperando clientes
    # Listen(argumento) o argumento e o numero de clientes em espera da negacao
    server_socket.listen(max_connections_wait)
    # Print
    print( "[{0}] Esperando clientes...".format(datetime.fromtimestamp(int(time.time())).time()) )
    # Loop para aceitar 
    while True:
        # Espera conexao
        # O accept() fica aqui parado a espera de alguma ligacao e nao sai daqui ate houver uma ligacao do cliente
        connection, address = server_socket.accept()
        # Print
        print( "[{0}] Cliente se ligou - {1}:{2}".format(datetime.fromtimestamp(int(time.time())).time(), address[0], address[1]) )
        # Criar nova tarefa
        _thread.start_new_thread(client_thread, (connection, address, buffer_size, max_connections))
    # Fecha o servidor
    server_socket.close()
# Fim metodoCriarServidor
#
# Metodo da Tarefa do cliente
# Inicio metodoTarefaCliente
def client_thread(connection, address, buffer_size, max_connections):
    # Caso o numero de ligacoes estiver no limite
    if len(list_clients) == max_connections:
        # Envia mensagem para o cliente quando servidor estiver cheio
        connection.send(b'Servidor esta cheio!')
        # Fecha o socket do cliente
        connection.close()
        # Sai do metodo
        return
    # Adiciona cliente a lista de clientes do servidor
    list_clients.append( ( address[0], address[1], len(list_clients), '0' ) )
    # Envia mensagem para o cliente quando se liga ao servidor
    connection.send(b'Bem-vindo ao servidor.')
    # Loop para receber e enviar
    while True:
        # Tentar receber mensagem
        try:
            # Esta variavel e o incio(tempo) de receber mensagem
            time_start_receive = time.time()
            # String
            string_ip_address = address[0] + ":" + str(address[1])
            # Mensagem do cliente
            client_mensage = connection.recv(buffer_size)
            # Caso nao houver mensagem, sai do loop
            if not client_mensage:
                break
            # Esta variavel e o fim(tempo) de receber mensagem
            time_end_receive = time.time()
            # Mensagem para cliente
            string_data = ""
            # Criar mensagem para cliente
            # Faz a listagem dos clientes ligado ao servidor
            for index_client in range(0, len(list_clients)):
                # Faz update cada cliente caso ip for igual
                if list_clients[index_client][0] == address[0]:
                    # Faz update cada cliente caso a porta for igual
                    if list_clients[index_client][1] == address[1]:
                        # Transforma tuple em list
                        client_list = list(list_clients[index_client])
                        # Substitui o valor
                        # Nota .decode() para transforma bytes em string
                        client_list[3] = client_mensage.decode("utf-8") 
                        # Transforma list em tuple
                        client_tuple = tuple(client_list)
                        # Substitui o tuple com novo valor
                        list_clients[index_client] = client_tuple
                # Cria a data
                string_data += "|{0}|{1}|{2}|{3}|{4}|".format(list_clients[index_client][0], str(list_clients[index_client][1]), str(len(list_clients)), "{0:0.1f}ms".format( (time_end_receive - time_start_receive)), str(list_clients[index_client][3]))
            # Print
            # print(string_data)
            # Cria uma mensage em bytes
            server_mensage = bytes(string_data, 'utf-8')
            # Envia mensagem para o cliente
            connection.sendall(server_mensage)
            # Print
            # print( "{0} com {1:0.1f}ms de atraso".format(string_ip_address, (time_end_receive - time_start_receive)) )
        # Caso houver erro
        except:
            # Print
            # Nenhuma ligação pôde ser feita porque o computador de destino as recusou ativamente
            print( "[{0}] Cliente desligou - {1}".format(datetime.fromtimestamp(int(time.time())).time(), string_ip_address) )
            # Procura o cliente que saiu do servidor
            for client in list_clients:
                if client[0] == address[0]:
                    if client[1] == address[1]:
                        # Remove o cliente que saiu
                        list_clients.remove(client)
            # Caso houver erro, sai do loop
            break
    # Fecha o socket do cliente
# Fim metodoTarefaCliente