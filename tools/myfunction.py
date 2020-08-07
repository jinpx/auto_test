import struct, hashlib, re


class RC4(object):
    def __init__(self):
        self.perm = []
        self.index1 = 0
        self.index2 = 0
        self.key = None
        self.count = 0

    def Setkey(self, keybytes):
        self.key = keybytes
        self.perm = [0] * 256
        for i in range(256):
            self.perm[i] = i

        j = 0
        for i in range(256):
            j = (j + self.perm[i] + self.key[i % len(self.key)]) % 256
            self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

    def setCount(self, count):
        self.count = count

    def getCount(self):
        return self.count

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


def myMd5(msg):
    m = hashlib.md5()
    b = msg.encode('utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


def pack(data, s='iiiii'):
    s = struct.Struct(s)
    return s.pack(*data.values())


def unpack(data, s='iiiii'):
    return struct.unpack(s, data)


def c_to_fmt():
    import re
    path = 'D:\struck.txt'
    ft = {'int': 'i', 'INT': 'i', 'ULONG': 'L', 'UINT': 'I', 'bool': '?'}
    with open(path, 'r', encoding='utf-8')as f:
        datas = [i.split() for i in f.read().splitlines()]
    s = ''
    for i in datas:
        if len(i) < 2:
            continue
        if i[0] == 'int' or i[0] == 'INT':
            s += 'i'
        if i[0] == 'ULONG':
            s += 'L'
        if i[0] == 'UINT':
            s += 'I'
        if i[0] == 'bool':
            s += '?'
        if i[0] == 'char':
            l = str(re.search(r'.*\[(\d+)\];', i[1]).group(1)) + 's'
            s += l
        if i[0] == '__int64':
            s += 'q'
        if i[0] == 'DOUBLE':
            s += 'd'
        else:
            print('找不到类型', i[0])
    print(s)


def c_fmt():
    p = re.compile(r'\s?(?P<_type>\w+)\s+(?P<key>[^\[;]+)(\([?P<size>\d+)\])?.+')
    source = 'D:\struck.txt'

    def c():
        for m in p.finditer(source):
            if not m:
                continue
            yield m.groupdict()

    fields = tuple(c())
    f = ''.join(f'{field["size"] or ""}{d_type[field["_type"]]}' for field in fields)


if __name__ == '__main__':
    c_to_fmt()
