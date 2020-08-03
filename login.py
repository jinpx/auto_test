import struct

class KK_packet:
    def __init__(self) :
        self.m_data  = []

    def addChar(self, _data) :
        struct.pack('c', _data)

        
    def addString(self, _data, _size) :
        struct.pack('c', _data)

    def addUint(self, _data) :  # 4bit
        self.m_data.append(_data)

    def to_bytes(self):
        data = str(self.m_data).encode()
        print(data)


logindata = {"AgentID": 14926056,
             "TML_SN": "EQ4gG6vEUL06ajaGn4EAuXDa662vaeeqL6UdoOQatxuujAlnqovO6VndvXT4Tv0l4a28XGoDxqde4El6XUAXLXe66lg2o6gQN4tlOgeAoV6gulE2jTNneUulE "
    , "device_info": "",
             "device_type": 2,
             "gsqPs": 5471,
             "szHardID": "2222222",
             "szIDcardNo": "*",
             "szIP": "192.168.0.59",
             "szMD5Pass": "14926056_026444-703017-106FA5-C05854-26B9-337F62",
             "szMathineCode": "026444-703017-106FA5-C05854-26B9-337F62",
             "szMobileVCode": "*",
             "szName": "BYPhone328497094",
             "uRoomVer": 220,
             "zCPUID": "612826255"
             }

def Login_Pack(a, b, c, d，e):
    a = KK_packet()
    a.addUint(14926056)
    a.addString("EQ4gG6vEUL06ajaGn4EAuXDa662vaeeqL6UdoOQatxuujAlnqovO6VndvXT4Tv0l4a28XGoDxqde4El6XUAXLXe66lg2o6gQN4tlOgeAoV6gulE2jTNneUulE ")
    a.addUint(100)
    a.addUint(101)
    a.addUint(100)
    a.to_bytes()
    return data;



a_data = Login_Pack(1,2,3,4,5);
socket.send(a_data, size)