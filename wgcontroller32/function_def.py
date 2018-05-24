from enum import IntEnum, unique


@unique
class ControllerFunctions(IntEnum):
    SEARCH_CONTROLLER = 0x94
    SET_CONTROLLER_IP = 0x96
    QUERY_CONTROLLER_STATUS = 0x20
    READ_DATETIME = 0x32
    SET_DATETIME = 0x30
    GET_RECORD_BY_INDEX = 0xb0
    SET_READ_INDEX = 0xb2
    GET_READ_INDEX = 0xb4
    REMOTE_OPEN_DOOR = 0x40
    ADD_OR_UPDATE_PRIVILEGE = 0x50
    DROP_SINGLE_PRIVILEGE = 0x52
    DROP_ALL_PRIVILEGES = 0x54
    READ_ALL_PRIVILEGES = 0x58
    QUERY_PRIVILEGES = 0x5a
    GET_PRIVILEGE_BY_INDEX = 0x5c
    SET_DOOR_CONTROL_PARAM = 0x80
    GET_DOOR_CONTROL_PARAM = 0x82
    SET_RECV_SERVER_IP_PORT = 0x90
    GET_RECV_SERVER_IP_PORT = 0x92
    ADD_PRIVILEGE_SMALL_TO_LARGE = 0x56

    def __repr__(self):
        return '<Controller Function {}: {}>'.format(self._name_, hex(self.value))


def lookup_by_number(value: int):
    """
    lookup function enum object by function id
    :param value: function id
    :return: Function object
    """
    if type(value) is ControllerFunctions:
        return value
    for name, member in ControllerFunctions.__members__.items():
        if member.value == value:
            return member
    raise ValueError('Function id {} does not exist'.format(hex(value)))
