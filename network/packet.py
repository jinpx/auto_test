import struct

class KK_packet:
    def __init__(self) :
        self.m_data  = []

    def addChar(self, _data) :
        struct.pack('c', _data)

        
    def addString(self, _data, _size) :
        struct.pack('c', _data)

    def addUint(self, _data) :  # 4bit
        self.m_data.append(_data)

    def to_bytes(self):
        data = str(self.m_data).encode()
        print(data)
