import socket
from wgcontroller32.packet import ControllerUDPPacket
from wgcontroller32.function_def import ControllerFunctions


def main():
    ip = input('Input subnet broadcast address: ')
    port = int(input('Input controller port: '))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 0))
    sock.settimeout(10)
    packet = ControllerUDPPacket(0, ControllerFunctions.SEARCH_CONTROLLER, b'').get_bytes()
    print('----------Finding controllers via broadcast...----------')
    sock.sendto(packet, (ip, port))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            packet = ControllerUDPPacket.from_bytes(data)
            print(addr[0], packet.device_sn)
        except socket.timeout:
            break

    print('----------Done!----------')

if __name__ == '__main__':
    main()
