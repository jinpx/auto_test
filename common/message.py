

# 连接认证
MDM_CONNECT = 1  # 认证主消息
ASS_CONNECT_SUCCESS = 3  # 认证成功
ASS_NET_GET = 5  # 取得认证
# Aserver 认证包
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
# 登录头
LOGIN_HEAD = {
    'uMessageSize': 20,
    'bMainID': 100,
    'bAssistantID': 1,
    'bHandleCode': 0,
    'bReserve': 0
}
# 登录体
LOGIN_BODY = {
    "uRoomVer": 220,
    "szName": "13713185800",
    "TML_SN": "EQ4gG6vEUL06ajaGn4EAuXDa662vaeeqL6UdoOQatxuujAlnqovO6VndvXT4Tv0l4a28XGoDxqde4El6XUAXLXe66lg2o6gQN4tlOgeAoV6gulE2jTNneUulE",
    "szMD5Pass": "3d24b838770ee90773804e8599e549ff",
    "szMathineCode": "026444-703017-106FA5-C05854-26B9-337F63",
    "zCPUID": "612826255",
    "szHardID": "2222222",
    "szIDcardNo": "*",
    "szMobileVCode": "*",
    "gsqPs": 5471,
    "iUserID": 0,
    "szdevice_info": "",
    "szdevice_type": 2,
    "AgentID": 14926056,
    "szIP": "192.168.0.59",
}

# 登录返回状态码
LOGIN_RES_CODE = {'5': '登录成功', '4': '登录失败'}

# 获取游戏列表
ASERVER_GAME_LIST = {
    'uMessageSize': 20,
    'bMainID': 101,
    'bAssistantID': 1,
    'bHandleCode': 0,
    'bReserve': 1,
}
