from tools.myfunction import *
from tcp.mysocket import MySocket
from tools.Config import *
from common.message import *


class AServer(object):
    def __init__(self, my_sock):
        self.m_socket = my_sock
        self.rc = RC4()
        self.log = Logger().getlog()

    # 发送认证连接
    def send_Connect(self):
        data = pack_head(ASERVER_CONNECT)
        self.m_socket.send(data)
        self.log.info('发送认证信息')

    # 解析返回的认证信息
    def recv_Connect(self):
        _data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(_data[:20])
        self.rc.Setkey([(int(i) + 48) for i in str(key)])
        self.rc.Process(_data[20:])
        if bMainID == MDM_CONNECT and bAssistantID == ASS_CONNECT_SUCCESS:
            res = '认证信息成功'
        else:
            res = '认证信息失败'
        self.log.info(res)
        return res

    # 发送网关请求
    def send_GateServer(self):
        _data = pack_head(GATE_SERVERS)
        self.m_socket.send(_data)
        self.log.info(msg='发送网关请求')

    # 解析返回的网关请求
    def recv_GateServer(self):
        data = self.m_socket.recv()
        a, b, c, d, keys = unpack(data[:20])
        if b != MDM_GP_REQURE_GAME_PARA:
            return
        res = dict()
        res_f = self.rc.Process(data[20:])
        s = 'i20s40sI128s128s128s128s128s128s200siiIIIiI'
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = unpack(bytes(res_f), s)
        res['m_is_haveZhuanZhang'] = a
        res['m_strGameSerialNO'] = b.decode('utf-8').strip(b'\x00'.decode())
        res['m_strMainserverIPAddr'] = c.decode('utf-8').strip(b'\x00'.decode())
        res['m_iMainserverPort'] = d
        res['m_strWebRootADDR'] = e.decode('utf-8').strip(b'\x00'.decode())
        res['m_strHomeADDR'] = f.decode('utf-8').strip(b'\x00'.decode())
        res['m_strHelpADDR'] = g.decode('utf-8').strip(b'\x00'.decode())
        res['m_strDownLoadSetupADDR'] = h.decode('utf-8').strip(b'\x00'.decode())
        res['m_strDownLoadUpdatepADDR'] = i.decode('utf-8').strip(b'\x00'.decode())
        res['m_strRallAddvtisFlashADDR'] = j.decode('utf-8').strip(b'\x00'.decode())
        res['m_strRoomRollADDR'] = k.decode('utf-8').strip(b'\x00'.decode())
        res['m_nHallInfoShowClass'] = l
        res['m_nEncryptType'] = m
        res['m_nFunction'] = n
        res['m_lNomalIDFrom'] = o
        res['m_lNomalIDEnd'] = p
        res['m_nIsUsingIMList'] = q
        res['m_iGameserverPort'] = r
        return res

    def main(self):
        self.send_Connect()
        self.recv_Connect()
        self.send_GateServer()
        res = self.recv_GateServer()
        for i in res.keys():
            setValue('Aserver', i, str(res[i]))
        else:
            self.log.info('写入配置文件成功')


if __name__ == '__main__':
    _mysocket = MySocket()
    _mysocket.connect('47.89.41.240', 37025)
    _a = AServer(_mysocket)
    _a.main()
    _mysocket.close()
