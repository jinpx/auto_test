from tcp.message import Message,Gate
from tcp.mysocket import MySocket

# 连接认证
MDM_CONNECT = 1  # 认证主消息
ASS_CONNECT_SUCCESS = 3  # 认证成功
ASS_NET_GET = 5  # 取得认证
ASERVER_CONNECT = {
    'uMessageSize': 20,
    'bMainID': MDM_CONNECT,
    'bAssistantID': ASS_NET_GET,
    'bHandleCode': 0,
    'bReserve': 0,
}

# 获取GateServer服务器列表
MDM_GP_REQURE_GAME_PARA = 102
GATE_SERVERS = {
    'uMessageSize': 20,
    'bMainID': MDM_GP_REQURE_GAME_PARA,
    'bAssistantID': 0,
    'bHandleCode': 0,
    'bReserve': 0,
}


class AServer(object):
    def __init__(self, my_sock):
        self.m_socket = my_sock

    # 发送认证连接
    def send_Connect(self):
        sender = Message(ASERVER_CONNECT)
        data = sender.pack()
        self.m_socket.send(data)
        ## print(f'发生认证连接：str{ASERVER_CONNECT} bytes{data}')

    # 认证成功
    def recv_Connect(self):
        sender = Message(ASERVER_CONNECT)
        _data = self.m_socket.recv()
        ## print(f'验证返回数据：{_data}')
        sender.unpack(_data)
        ## print(f'认证结果数据:bytes{_data} str{sender.bAssistantID}')
        if sender.bMainID == MDM_CONNECT and sender.bAssistantID == ASS_CONNECT_SUCCESS:
            return ASS_CONNECT_SUCCESS

    # 发送网关请求
    def send_GateServer(self):
        sender = Message(GATE_SERVERS)
        _data = sender.pack()
        self.m_socket.send(_data)

    # 接收网关请求
    def recv_GateServer(self, _data):
        _sender = Message(GATE_SERVERS)
        a,b,c,d,key = _sender.unpack(_data[:20])
        if b == MDM_GP_REQURE_GAME_PARA:
            _Gate = Gate()
            res = _Gate.body_unstruck(_data[20:],key)
            print(res)


if __name__ == '__main__':
    _mysocket = MySocket()
    _mysocket.connect('47.89.41.240', 37025)
    _a = AServer(_mysocket)
    _a.send_Connect()
    _data = _mysocket.recv()
    _a.send_GateServer()
    _data = _mysocket.recv()
    _a.recv_GateServer(_data)
    _mysocket.close()
