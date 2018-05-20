import socket


def send_packet_and_get_response(ip, port, packet_data) -> bytes:
    """
    send a single packet and return the response
    :param ip:
    :param port:
    :param packet_data:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet_data, (ip, port))
    return sock.recv(1024)


class UDPClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
