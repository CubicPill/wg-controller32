"""
typedef struct struPacketShort {
    unsigned char      type;                  //类型
    unsigned char      functionID;            //功能号
    unsigned short     reserved;              //保留
    unsigned int       iDevSn;                //设备序列号 4字节
    unsigned char      data[32];              //32字节的数据
    unsigned int       sequenceId;            //数据包流水号
    unsigned char      extern_data[20];       //第二版本 扩展20字节
} *pPacketShort, PacketShort;    //报文
"""
from function_def import Function, lookup_by_number

TYPE = 0x17
PACKET_LENGTH = 64


def parse_packet(packet_bytes: bytes):
    """
    parse packet
    :param packet_bytes: must be 64 bytes
    :return: type of packet (typically 0x17), device serial, function, data, serial number of packet
    """
    assert len(packet_bytes) == PACKET_LENGTH
    _type = packet_bytes[0]
    function_id = lookup_by_number(packet_bytes[1])
    device_sn = sum([v << (8 * i) for i, v in enumerate(packet_bytes[4:8])])
    data = packet_bytes[8:40]
    serial_number = sum([v << (8 * i) for i, v in enumerate(packet_bytes[40:44])])
    return _type, device_sn, function_id, data, serial_number


class ControllerUDPPacket:
    def __init__(self, device_sn: int, function_id: Function or int, data: bytes, serial_number: int = 0):
        assert 0 <= device_sn <= 0xFFFFFFFF
        assert 0 <= function_id <= 0xFF
        assert len(data) == 32
        assert 0 <= serial_number <= 0xFFFFFFFF
        self._device_sn = device_sn
        self._function = lookup_by_number(function_id)
        self._data = data
        self._serial_number = serial_number
        self._bytes = b''

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        assert len(value) == 32 and type(value) is bytes
        self._data = value

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, value):
        assert 0 <= value <= 0xFF
        self._function = value

    @property
    def device_sn(self):
        return self._device_sn

    @device_sn.setter
    def device_sn(self, value):
        assert 0 <= value <= 0xFFFFFFFF
        self._device_sn = value

    @property
    def serial_number(self):
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value):
        assert 0 <= value <= 0xFFFFFFFF
        self._serial_number = value

    @staticmethod
    def from_bytes(packet_bytes: bytes):
        _type, device_sn, function_id, data, serial_number = parse_packet(packet_bytes)
        return ControllerUDPPacket(device_sn, function_id, data, serial_number)

    def get_bytes(self) -> bytes:
        if not self._bytes:
            pkt_array = [0] * PACKET_LENGTH
            pkt_array[0] = TYPE
            pkt_array[1] = self._function
            pkt_array[4:8] = [(self._device_sn >> (8 * i)) & 0xFF for i in range(4)]
            pkt_array[8:40] = list(self._data)
            pkt_array[40:44] = [(self._serial_number >> (8 * i)) & 0xFF for i in range(4)]
            self._bytes = bytes(pkt_array)
        return self._bytes
