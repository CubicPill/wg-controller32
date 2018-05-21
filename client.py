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
    def __init__(self, ip, port, device_sn):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._ip = ip
        self._port = port
        self._device_sn = device_sn
        self._serial = 0

    def connect(self):
        pass
