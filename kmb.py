"""
The simple client-server application.
The client part is able to send UDP or TCP requests,
to which the server part sends him the address and port of the client in the format <host>:<port>
"""

import sys
import socket


def client_tcp_interface(host, port):
    """
    The client part of the application that sends TCP requests
    In response to the request, it receives its address in the format <host>:<port>

    :param host: the host name or its IP address to send the request to
    :param port: the port number of the server to send the request to
    :return:
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = client_socket.recv(4096)
    print(data.decode())

    client_socket.close()


def client_udp_interface(host, port):
    """
    The client part of the application that sends UDP requests
    In response to the request, it receives its address in the format <host>:<port>

    :param host: the host name or its IP address to send the request to
    :param port: the port number of the server to send the request to
    :return:
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket

    client_socket.sendto(''.encode("utf-8"), (host, port))  # send message to server

    data = client_socket.recvfrom(4096)
    print(data[0].decode())

    client_socket.close()


def server_tcp_interface(address, port):
    """
     The server part of the application running on the TCP
     The server receives the request, sends the sender's address in response

     :param address: the host name or its IP-address on which the server is running
     :param port:    the number of the port to which the clients will connect
     :return:
     """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(1)

    print("The server is ready to receive")

    while 1:
        connection_socket, client_address = server_socket.accept()

        answer = (str(client_address[0]) + ':' + str(client_address[1])).encode('utf-8')

        connection_socket.send(answer)
        connection_socket.close()


def server_udp_interface(address, port):
    """
    The server part of the application running on the UDP
    The server receives the request, sends the sender's address in response

    :param address: the host name or its IP-address on which the server is running
    :param port:    the number of the port to which the clients will connect
    :return:
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((address, port))

    print("The server is ready to receive")

    while 1:
        data = server_socket.recvfrom(4096)
        client_address = data[1]

        answer = (str(client_address[0]) + ':' + str(client_address[1])).encode('utf-8')

        server_socket.sendto(answer, client_address)


def check_address(str_host, str_port):
    """
    Checking the validity of the host name and port number

    :param str_host: a string containing the host name
    :param str_port: a string containing the port number
    :return:
    """

    if str_port.isdigit():
        if int(str_port) < 0 or int(str_port) > 65536:
            sys.exit("ERROR, invalid port \n"
                     "Please, run the program in the following format: \n"
                     "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
    else:
        sys.exit("ERROR, invalid port \n"
                 "Please, run the program in the following format: \n"
                 "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")

    if str_host[0] == '-':
        sys.exit("ERROR, invalid host name \n"
                 "Please, run the program in the following format: \n"
                 "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")


def config_connection(flags):
    """
    Analyzes command-line arguments

    :param flags: the rest of the command line arguments
    :return: 0 - client tcp
             1 - server tcp
             2 - client udp
             3 - server udp
    """

    mask = 0

    if len(flags) == 0:
        return mask

    if '-s' in flags:
        mask += 1

    if '-u' in flags:
        mask += 2

    if '-t' in flags and (mask & 0b10) >> 1:
        sys.exit("ERROR, invalid flags. The -t and -u flags are not supported at the same time \n"
                 "Please, run the program in the following format: \n"
                 "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
    return mask


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("ERROR, incorrectly entered arguments when starting the program \n"
                 "Please, run the program in the following format: \n"
                 "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
    else:
        host_name = sys.argv[1]
        number_port = sys.argv[2]

        check_address(host_name, number_port)

        flag = sys.argv[3:]

        config = {0: client_tcp_interface,
                  1: server_tcp_interface,
                  2: client_udp_interface,
                  3: server_udp_interface}

        config.get(config_connection(flag))(host_name, int(number_port))
