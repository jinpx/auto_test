import struct


class RC4(object):
    def __init__(self):
        self.perm = []
        self.index1 = 0
        self.index2 = 0
        self.key = None

    def Setkey(self, keybytes):
        self.key = keybytes
        self.perm = [0] * 256
        for i in range(256):
            self.perm[i] = i

        j = 0
        for i in range(256):
            j = (j + self.perm[i] + self.key[i % len(self.key)]) % 256
            self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

    def Process(self, _data):

        j = 0
        output = [0] * len(_data)
        for i in range(len(_data)):
            self.index1 = (self.index1 + 1) % 256
            self.index2 = (self.index2 + self.perm[self.index1]) % 256
            self.perm[self.index1], self.perm[self.index2] = self.perm[self.index2], self.perm[self.index1]

            j = (self.perm[self.index1] + self.perm[self.index2]) % 256
            output[i] = _data[i] ^ self.perm[j]
        return output

    def ReadProcess(self, _data, _len):
        j = 0
        output = [0] * _len
        for i in range(_len):
            self.perm[self.index1], self.perm[self.index2] = self.perm[self.index2], self.perm[self.index1]

            j = (self.perm[self.index1] + self.perm[self.index2]) % 256
            output[i] = _data[i] ^ self.perm[j]
        return output

    def ReverseBytes(self, _Pointer, _Length):
        Temp = _Pointer
        for i in range(_Length):
            _Pointer[i] = Temp[_Length - i - 1]


def pack_head(data,s='iiiii'):
    s = struct.Struct(s)
    return s.pack(data['uMessageSize'], data['bMainID'], data['bAssistantID'], data['bHandleCode'],
                  data['bReserve'])


def unpack(data, s='iiiii'):
    return struct.unpack(s, data)


