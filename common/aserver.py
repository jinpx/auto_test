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
        self.log.info('Aserver发送认证信息')

    # 解析返回的认证信息
    def recv_Connect(self):
        _data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(_data[:20])
        self.rc.Setkey([(int(i) + 48) for i in str(key)])
        self.rc.Process(_data[20:])
        if bMainID == MDM_CONNECT and bAssistantID == ASS_CONNECT_SUCCESS:
            res = 'Aserver认证信息成功'
        else:
            res = 'Aserver认证信息失败'
        self.log.info(res)

    # 发送网关请求
    def send_GateServer(self):
        _data = pack_head(GATE_SERVERS)
        self.m_socket.send(_data)
        self.log.info(msg='Aserver发送网关请求')

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
            self.log.info('Aserver写入配置文件成功')


class GServer(AServer):
    def __init__(self, my_sock):
        super().__init__(my_sock)
        ip, port = getValue('Aserver', 'm_strmainserveripaddr'), getInt('Aserver', 'm_imainserverport')
        self.m_socket.connect(ip, port)

    # 发送认证
    def send_Connect(self):
        data = pack_head(ASERVER_CONNECT)
        self.m_socket.send(data)
        self.log.info('Gserver发送认证信息')

    # 解析认证信息
    def recv_Connect(self):
        _data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(_data[:20])
        self.rc.Setkey([(int(i) + 48) for i in str(key)])
        self.rc.Process(_data[20:28])
        if bMainID == MDM_CONNECT and bAssistantID == ASS_CONNECT_SUCCESS:
            res = 'Gserver认证信息成功'
        else:
            res = 'Gserver认证信息失败'
        self.log.info(res)

    # 发送登录包
    def send_message(self):
        data_head = pack_head(LOGIN_HEAD)
        data_body = pack_head(LOGIN_BODY,s='I64s128s52s64s24s24s64s8sii50sii20s')
        send_data = data_head+bytes(self.rc.Process(data_body))
        print(send_data)
        self.m_socket.send(send_data)
        self.log.info('Gserver发送认证信息')

    def recv_message(self):
        data = self.m_socket.recv()
        print(unpack(data))


if __name__ == '__main__':
    _mysocket = MySocket()
    _a = GServer(_mysocket)
    _a.send_Connect()
    _a.recv_Connect()
    _a.send_message()
    _a.recv_message()
    _mysocket.close()
