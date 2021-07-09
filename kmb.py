"""
The simple client-server application.
The client side is able to send UDP or TCP requests,
to which the server side sends him the address and port of the client in the format <host>:<port>
"""

# import sys
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


if __name__ == '__main__':
    client_udp_interface('192.168.1.21', 12000)
