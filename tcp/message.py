import struct
from Crypto.Cipher import ARC4


# 加密
def encrypt(message, key):
    des = ARC4.new(key)
    cipher_text = des.encrypt(message)
    return cipher_text


# 解密
def decrypt(cipher_text, key):
    des3 = ARC4.new(key)
    message = des3.decrypt(cipher_text)
    return message


class Message(object):
    """信息头处理"""

    def __init__(self, data):
        self.uMessageSize = data['uMessageSize']
        self.bMainID = data['bMainID']
        self.bAssistantID = data['bAssistantID']
        self.bHandleCode = data['bHandleCode']
        self.bReserve = data['bReserve']
        self.s = struct.Struct('iiiii')

    # 打包
    def pack(self):
        return self.s.pack(self.uMessageSize, self.bMainID, self.bAssistantID, self.bHandleCode,
                           self.bReserve)

    # 解head包
    def unpack(self, _data):
        self.uMessageSize, self.bMainID, self.bAssistantID, self.bHandleCode, self.bReserve = self.s.unpack(_data)
        return self.uMessageSize, self.bMainID, self.bAssistantID, self.bHandleCode, self.bReserve


GATE_MSG = {
    'm_is_haveZhuanZhang': 12,
    'm_strGameSerialNO': 'asdf',
    'm_strMainserverIPAddr': 'adf',
    'm_iMainserverPort': 1024,
    'm_strWebRootADDR': 'asd',
    'm_strHomeADDR': 'aawe',
    'm_strHelpADDR': '2323',
    'm_strDownLoadSetupADDR': '123',
    'm_strDownLoadUpdatepADDR': '233',
    'm_strRallAddvtisFlashADDR': 'qw',
    'm_strRoomRollADDR': 'asdfd',
    'm_nHallInfoShowClass': 1,
    'm_nEncryptType': 1,
    'm_nFunction': 2,
    'm_lNomalIDFrom': 104,
    'm_lNomalIDEnd': 106,
    'm_nIsUsingIMList': 1,
    'm_iGameserverPort': 1901
}


class Gate():
    # def __init__(self):
    #     self.a = data['m_is_haveZhuanZhang']
    #     self.b = data['m_strGameSerialNO'].encode()
    #     self.c = data['m_strMainserverIPAddr'].encode()
    #     self.d = data['m_iMainserverPort']
    #     self.e = data['m_strWebRootADDR'].encode()
    #     self.f = data['m_strHomeADDR'].encode()
    #     self.g = data['m_strHelpADDR'].encode()
    #     self.h = data['m_strDownLoadSetupADDR'].encode()
    #     self.i = data['m_strDownLoadUpdatepADDR'].encode()
    #     self.j = data['m_strRallAddvtisFlashADDR'].encode()
    #     self.k = data['m_strRoomRollADDR'].encode()
    #     self.l = data['m_nHallInfoShowClass']
    #     self.m = data['m_nEncryptType']
    #     self.n = data['m_nFunction']
    #     self.o = data['m_lNomalIDFrom']
    #     self.p = data['m_lNomalIDEnd']
    #     self.q = data['m_nIsUsingIMList']
    #     self.r = data['m_iGameserverPort']
    #
    # # 打包
    # def head_struck(self):
    #     return struct.pack("i20s40sI128s128s128s128s128s128s200siiIqqiI", self.a, self.b, self.c, self.d,
    #                        self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l, self.m, self.n, self.o,
    #                        self.p, self.q, self.r)

    # 解包
    def body_unstruck(self, data, key=1):
        res = {}
        key = struct.pack('i', key)
        x = key+bytes(6-len(key))
        _data = decrypt(data, x)
        print(data)
        print(_data)
        md = 'i20s40sI128s128s128s128s128s128s200siiIIIiI'
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = struct.unpack(
            md, _data)
        # print(a,b.decode('utf-8','ignore'),c.decode('utf-8','ignore'))
        print(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r)
        res['m_is_haveZhuanZhang'] = a
        res['m_strGameSerialNO'] = b.decode()
        res['m_strMainserverIPAddr'] = c.decode()
        res['m_iMainserverPort'] = d
        res['m_strWebRootADDR'] = e.decode()
        res['m_strHomeADDR'] = f.decode()
        res['m_strHelpADDR'] = g.decode()
        res['m_strDownLoadSetupADDR'] = h.decode()
        res['m_strDownLoadUpdatepADDR'] = i.decode()
        res['m_strRallAddvtisFlashADDR'] = j.decode()
        res['m_strRoomRollADDR'] = k.decode()
        res['m_nHallInfoShowClass'] = l
        res['m_nEncryptType'] = m
        res['m_nFunction'] = n
        res['m_lNomalIDFrom'] = o
        res['m_lNomalIDEnd'] = p
        res['m_nIsUsingIMList'] = q
        res['m_iGameserverPort'] = r
        return res


if __name__ == '__main__':
    MSG_HEAD = {
        'uMessageSize': 0,
        'bMainID': 0,
        'bAssistantID': 0,
        'bHandleCode': 0,
        'bReserve': 0,
    }
    # _sender = Message(MSG_HEAD)
    a = encrypt(b'laksdjf', b'abcde')
    print(a)
    print(decrypt(a, b'abcde'))
