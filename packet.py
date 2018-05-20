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
from function_def import Function

TYPE = 0x17
PACKET_LENGTH = 64


class AT8000UDPPacket:
    def __init__(self, device_sn, function_id, data: bytes, serial_number=0):
        assert 0 <= device_sn <= 0xFFFFFFFF
        assert 0 <= function_id <= 0xFF
        assert len(data) <= 32
        assert 0 <= serial_number <= 0xFFFFFFFF
        self.device_sn = device_sn
        self.function_id = function_id
        self.data = data + bytes(32 - len(data))
        self.serial_number = serial_number
        self._bytes = b''

    def get_bytes(self) -> bytes:
        if not self._bytes:
            pkt_array = [0] * PACKET_LENGTH
            pkt_array[0] = TYPE
            pkt_array[1] = self.function_id
            pkt_array[4:8] = [(self.device_sn >> (8 * i)) & 0xFF for i in range(4)]
            pkt_array[8:40] = list(self.data)
            pkt_array[40:44] = [(self.serial_number >> (8 * i)) & 0xFF for i in range(4)]
            self._bytes = bytes(pkt_array)
        return self._bytes
