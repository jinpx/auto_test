import struct
from tcp.message import Message
from gate import Gate


## 连接认证
MDM_CONNECT 			= 1		## 认证主消息
ASS_CONNECT_SUCCESS 	= 3		## 认证成功
ASS_NET_GET 			= 5		## 取得认证
ASERVER_CONNECT = {
    'uMessageSize': 20,
    'bMainID': MDM_CONNECT,
    'bAssistantID': ASS_NET_GET,
    'bHandleCode': 0,
    'bReserve': 0,
}


## 获取GateServer服务器列表
MDM_GP_REQURE_GAME_PARA  = 102
ASERVER_CONNECT = {
    'uMessageSize': 20,
    'bMainID': MDM_GP_REQURE_GAME_PARA,
    'bAssistantID': 0,
    'bHandleCode': 0,
    'bReserve': 0,
}


class AServer(object) :
    def __init__(self, _sock) :
		self.m_socket=_sock

	## 发送认证连接
	def send_Connect(self) :
		_sender = Message(ASERVER_CONNECT)
		_data = _sender.pack()
		self.m_socket.send(_data, len(_data))

	## 认证成功
	def recv_Connect(self, _data) :
		_sender = Message(ASERVER_CONNECT)
		_data = _sender.unpack(_data)
		if _sender.bMainID = MDM_CONNECT and  bAssistantID = ASS_CONNECT_SUCCESS :
			return ASS_CONNECT_SUCCESS

	## 发送网关请求
	def send_GateServer(self) :
		_sender = Message(ASERVER_CONNECT)
		_data = _sender.pack()
		self.socket.send(_data, len(_data))
	
	## 接收网关请求
	def recv_GateServer(self, _data) :
		_sender = Message(ASERVER_CONNECT)
		_sender.unpack(_data)
		if _sender.bMainID = MDM_GP_REQURE_GAME_PARA :
			_Gate = Gate(GATE_MSG)
			print(_Gate.f)