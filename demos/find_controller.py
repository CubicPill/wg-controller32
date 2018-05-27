from wgcontroller32.function_def import ControllerFunctions
from wgcontroller32.client import send_packet_and_get_response
from wgcontroller32.packet import ControllerUDPPacket, parse_packet


def main():
    ip = input('Input controller IP: ')
    port = int(input('Input controller port: '))
    _type, device_sn, function_id, data, serial_number = parse_packet(
        send_packet_and_get_response(ip, port,
                                     ControllerUDPPacket(0, ControllerFunctions.SEARCH_CONTROLLER, b'').get_bytes()))
    print('Device SN:', device_sn)


if __name__ == '__main__':
    main()
