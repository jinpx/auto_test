import struct

MSG_HEAD = {
    'uMessageSize': 0,
    'bMainID': 0,
    'bAssistantID': 0,
    'bHandleCode': 0,
    'bReserve': 0,
}

class Message(object) :
    def __init__(self, data : MSG_HEAD) :
       self.uMessageSize = data['uMessageSize']
       self.bMainID = data['bMainID']
       self.bAssistantID = data['bAssistantID']
       self.bHandleCode = data['bHandleCode']
       self.bReserve = data['bReserve']

    ## 合包
    def pack(self) :
        a = self.uMessageSize
        b = self.bMainID
        c = self.bAssistantID
        d = self.bHandleCode
        e = self.bReserve
        _data = struct.pack('iii', a, b, c, d, e)
        return _data

    ## 解包
    def unpack(self, _data) :
        a, b, c, d, e = struct.unpack('iiiii', _data)
        self.uMessageSize = a
        self.bMainID = b
        self.bAssistantID = c
        self.bHandleCode = d
        self.bReserve = e

_sender = Message(MSG_HEAD)
_data = _sender.pack()
print(_data)
