from tcp.mysocket import MySocket
from tools.Config import *
from aserver import AServer
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
my_socket = MySocket()
ip,port = getValue('Aserver','ip'),int(getValue('Aserver','port'))
print(ip,port)
my_socket.connect(ip,port)
aserver= AServer(my_socket)
aserver.send_Connect()
print(aserver.recv_Connect())
my_socket.close()




