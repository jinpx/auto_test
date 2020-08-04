import struct
from tools.Config import Logger

jc = {
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


class GateServer(Message): 
    def __init__(self, data: dict):
        loger = Logger().logger
        loger.info(f'传入数据{str(data)}')
        self.data = data
        self.a = data['m_is_haveZhuanZhang']
        self.b = data['m_strGameSerialNO'].encode()
        self.c = data['m_strMainserverIPAddr'].encode()
        self.d = data['m_iMainserverPort']
        self.e = data['m_strWebRootADDR'].encode()
        self.f = data['m_strHomeADDR'].encode()
        self.g = data['m_strHelpADDR'].encode()
        self.h = data['m_strDownLoadSetupADDR'].encode()
        self.i = data['m_strDownLoadUpdatepADDR'].encode()
        self.j = data['m_strRallAddvtisFlashADDR'].encode()
        self.k = data['m_strRoomRollADDR'].encode()
        self.l = data['m_nHallInfoShowClass']
        self.m = data['m_nEncryptType']
        self.n = data['m_nFunction']
        self.o = data['m_lNomalIDFrom']
        self.p = data['m_lNomalIDEnd']
        self.q = data['m_nIsUsingIMList']
        self.r = data['m_iGameserverPort']

    # 打包
    def head_struck(self):
        return struct.pack("i20s40sI128s128s128s128s128s128s200siiIqqiI", self.a, self.b, self.c, self.d,
                           self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l, self.m, self.n, self.o,
                           self.p, self.q, self.r)

    # 解包
    def head_unstruck(self, data):
        res = {}
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = struct.unpack(
            "i20s40sI128s128s128s128s128s128s200siiIqqiI", data)
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


a = Message(jc)
b = a.head_struck()
print(b)
print(len(b))
print(a.head_unstruck(b))
