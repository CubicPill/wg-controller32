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
    def __init__(self, ip, port, device_sn, timeout=4, serial=0):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(timeout)
        self._ip = ip
        self._port = port
        self._device_sn = device_sn
        self._serial = serial

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def device_sn(self):
        return self._device_sn

    @property
    def serial(self):
        return self._serial

    @property
    def timeout(self):
        return self._socket.gettimeout()

    @timeout.setter
    def timeout(self, timeout):
        self._socket.settimeout(timeout)

    def _request(self, packet_data):
        self._socket.sendto(packet_data, (self._ip, self._port))
        return self._socket.recv(1024)
