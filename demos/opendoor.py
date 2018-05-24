from wgcontroller32 import UDPClient, ControllerFunctions


def main():
    client = UDPClient(input('Controller IP:'), int(input('Port:')), int(input('Device SN:')))
    doorno = int(input('Enter door number(1-4):'))
    resp = client.request(ControllerFunctions.REMOTE_OPEN_DOOR, bytes([doorno]))
    if resp.data[0] == 0x01:
        print('Success!')
    else:
        print('Oops, request failed. Check your input.')


if __name__ == '__main__':
    main()
