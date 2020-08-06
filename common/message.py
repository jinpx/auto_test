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
