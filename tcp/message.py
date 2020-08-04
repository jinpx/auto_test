import struct


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


if __name__ == '__main__':
    MSG_HEAD = {
        'uMessageSize': 0,
        'bMainID': 0,
        'bAssistantID': 0,
        'bHandleCode': 0,
        'bReserve': 0,
    }
    _sender = Message(MSG_HEAD)
    _data = _sender.pack()
    print(_data)
    _sender.unpack(_data)
    print(_sender.bMainID)
