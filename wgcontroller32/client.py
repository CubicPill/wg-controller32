import socket
from wgcontroller32.packet import ControllerUDPPacket, parse_packet
from wgcontroller32.function_def import ControllerFunctions


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


def get_device_sn(ip, port):
    """
    query device for SN with ip and port
    :param ip:
    :param port:
    :return: device sn
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = ControllerUDPPacket(0, ControllerFunctions.SEARCH_CONTROLLER, b'').get_bytes()
    sock.sendto(packet, (ip, port))
    _type, device_sn, function_id, data, serial_number = parse_packet(sock.recv(1024))
    return device_sn


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

    def _request(self, packet_data, recv):
        self._socket.sendto(packet_data, (self._ip, self._port))
        if recv:
            returned_data = self._socket.recv(1024)
            return returned_data
        return None

    def request(self, function_id, data, recv=True):
        """
        send request to controller
        :param function_id:
        :param data: bytes, will be automatically zero-filled to 32 bytes
        :param recv: if wait for the response
        :return: a ControllerUDPPacket object containing response data or None
        """
        assert len(data) <= 32
        data += bytes(32 - len(data))
        packet = ControllerUDPPacket(self._device_sn, function_id, data, serial_number=self._serial)
        returned_data = self.request_raw(packet.get_bytes(), recv)
        if recv:
            return ControllerUDPPacket.from_bytes(returned_data)
        return returned_data

    def request_raw(self, packet_data, recv=True):
        """
        send request with given packet, packet length should be 64 bytes
        :param packet_data:
        :param recv:
        :return: packet bytes
        """
        assert len(packet_data) == 64
        returned_data = self._request(packet_data, recv)
        self._serial += 1
        return returned_data
