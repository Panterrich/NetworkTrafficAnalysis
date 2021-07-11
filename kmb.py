"""
The simple client-server application.
The client part is able to send UDP or TCP requests,
to which the server part sends him the address and port of the client in the format <host>:<port>
"""

import sys
import socket
import logging


def client_tcp_interface(host, port):
    """
    The client part of the application that sends TCP requests
    In response to the request, it receives its address in the format <host>:<port>

    :param host: the host name or its IP address to send the request to
    :param port: the port number of the server to send the request to
    :return:
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
    client_socket.connect((host, port))
    logging.info('The client TCP socket was opened')

    data = client_socket.recv(4096)
    logging.info('The client received a message from the server %s:%d', host, port)
    print(data.decode())

    client_socket.close()
    logging.info('The client TCP socket was closed')


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
    logging.info('The client sent a request to the server %s:%d', host, port)

    data = client_socket.recvfrom(4096)
    logging.info('The client received a message from the server %s:%d', host, port)
    print(data[0].decode())

    client_socket.close()
    logging.info('The client UDP socket was closed')


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
    logging.info('The server is ready to receive')

    while 1:
        connection_socket, client_address = server_socket.accept()
        logging.info('The TCP connection to the client %s:%d has been set up',
                     client_address[0], client_address[1])

        answer = (str(client_address[0]) + ':' + str(client_address[1])).encode('utf-8')

        connection_socket.send(answer)
        logging.info('The server sent a message to the client %s:%d',
                     client_address[0], client_address[1])

        connection_socket.close()
        logging.info('The TCP connection socket was closed')


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
    logging.info('The server is ready to receive')

    while 1:
        data = server_socket.recvfrom(4096)
        client_address = data[1]
        logging.info('The server received a message from the client %s:%d',
                     client_address[0], client_address[1])

        answer = (str(client_address[0]) + ':' + str(client_address[1])).encode('utf-8')

        server_socket.sendto(answer, client_address)
        logging.info('The server sent a message to the client %s:%d',
                     client_address[0], client_address[1])


def check_address(str_host, str_port):
    """
    Checking the validity of the host name and port number

    :param str_host: a string containing the host name
    :param str_port: a string containing the port number
    :return: error
    """

    if str_port.isdigit():
        if int(str_port) < 0 or int(str_port) > 65536:
            logging.error("Invalid port! "
                          "The port number has exceeded the range of acceptable values \n"
                          "Please, run the program in the following format: \n"
                          "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
            return 0
    else:
        logging.error("Invalid port! "
                      "The port number doesn't consist of digits \n"
                      "Please, run the program in the following format: \n"
                      "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
        return 0

    if str_host[0] == '-':
        logging.error("Invalid host name \n"
                      "Please, run the program in the following format: \n"
                      "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
        return 0

    return 1


def config_connection(flags):
    """
    Analyzes command-line arguments

    :param flags: the rest of the command line arguments
    :return: mask: 0 - client tcp
                   1 - server tcp
                   2 - client udp
                   3 - server udp
             different_protocols_flag - the flag is set if UDP and TCP are used at the same time.
    """

    mask = 0
    different_protocols_flag = 0

    if len(flags) == 0:
        return mask, different_protocols_flag

    if '-s' in flags:
        mask += 1

    if '-u' in flags:
        mask += 2

    if '-t' in flags and (mask & 0b10) >> 1:
        different_protocols_flag = 1
        logging.error("Invalid flags. The -t and -u flags are not supported at the same time \n"
                      "Please, run the program in the following format: \n"
                      "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")

    return mask, different_protocols_flag


def log_config():
    """
    Analyzes the flags and configures the logging format and the log output stream

    :return: logging is configured successfully or not
    """

    if '-f' in sys.argv:
        if '-o' in sys.argv:
            logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
            logging.error("Multiple output streams are used."
                          "Please, run the program in the following format: \n"
                          "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
            return 0

        logging.basicConfig(filename=sys.argv[sys.argv.index('-f') + 1],
                            level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
        return 1

    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    return 1


if __name__ == '__main__':
    if log_config():
        if len(sys.argv) < 3:
            logging.error("Incorrectly entered arguments when starting the program \n"
                          "Please, run the program in the following format: \n"
                          "python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>] \n")
        else:
            host_name = sys.argv[1]
            number_port = sys.argv[2]

            if check_address(host_name, number_port):

                flag = sys.argv[3:]
                mode, error = config_connection(flag)

                if not error:
                    config = {0: client_tcp_interface,
                              1: server_tcp_interface,
                              2: client_udp_interface,
                              3: server_udp_interface}

                    config.get(mode)(host_name, int(number_port))
