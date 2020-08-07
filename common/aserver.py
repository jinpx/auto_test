from collections import namedtuple
import time
from tools.myfunction import *
from tcp.mysocket import MySocket
from tools.Config import *
from common.message import *

logger = my_Log()


def log_msg(t: int, a, b, c, d):
    if t == 1:
        return f"发送               请求协议[{b:3}:{c}] 请求数据大小：{d:5}"
    if t == 2:
        return f"响应  时间: {a:0>5d}   响应协议[{b:3}:{c}] 响应数据大小：{d:5}"


class AServer(object):
    def __init__(self):
        ip, port = getValue('Aserver', 'ip'), getInt('Aserver', 'port')
        self.m_socket = MySocket()
        self.m_socket.connect(ip, port)
        self.rc = RC4()
        self.t = int(time.time() * 1000)

    def __del__(self):
        self.m_socket.close()

    # 发送认证连接

    def send_Connect(self):
        data = pack(ASERVER_CONNECT)
        self.m_socket.send(data)
        logger.debug(log_msg(1, self.t, ASERVER_CONNECT["bMainID"], ASERVER_CONNECT["bAssistantID"], len(data)))

    # 解析返回的认证信息
    def recv_Connect(self):
        data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(data[:20])
        t = int(time.time() * 1000) - self.t
        logger.debug(log_msg(2, t, bMainID, bAssistantID, len(data)))
        self.rc.Setkey([(int(i) + 48) for i in str(key)])
        self.rc.Process(data[20:])

    # 发送网关请求
    def send_GateServer(self):
        data = pack(GATE_SERVERS)
        self.m_socket.send(data)
        self.t = int(time.time() * 1000)
        logger.debug(log_msg(1, self.t, GATE_SERVERS["bMainID"], GATE_SERVERS["bAssistantID"], len(data)))

    # 解析返回的网关请求
    def recv_GateServer(self):
        data = self.m_socket.recv()
        t = int(time.time() * 1000) - self.t
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(data[:20])
        logger.debug(log_msg(2, t, bMainID, bAssistantID, len(data)))
        if bMainID != MDM_GP_REQURE_GAME_PARA:
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


class GServer(object):
    def __init__(self, my_sock):
        self.m_socket = my_sock
        self.rc_Come = RC4()
        self.rc_Goto = RC4()
        ip, port = getValue('Aserver', 'm_strmainserveripaddr'), getInt('Aserver', 'm_imainserverport')
        self.m_socket.connect(ip, port)
        self.t = int(time.time() * 1000)

    # 发送认证
    def send_Connect(self):
        data = pack(ASERVER_CONNECT)
        self.m_socket.send(data)
        logger.debug(log_msg(1, self.t, ASERVER_CONNECT["bMainID"], ASERVER_CONNECT["bAssistantID"], len(data)))

    # 解析认证信息
    def recv_Connect(self):
        data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, key = unpack(data[:20])
        t = int(time.time() * 1000) - self.t
        logger.debug(log_msg(2, t, bMainID, bAssistantID, len(data)))
        self.rc_Come.Setkey([(int(i) + 48) for i in str(key)])
        self.rc_Goto.Setkey([(int(i) + 48) for i in str(key)])
        self.rc_Come.Process(data[20:28])
        if bMainID == MDM_CONNECT and bAssistantID == ASS_CONNECT_SUCCESS:
            res = 'Gserver认证信息成功'
        else:
            res = 'Gserver认证信息失败'

    # 发送登录包
    def send_Login(self):
        data_body = pack(LOGIN_BODY, s='=I64s128s52s64s24s24s64s8sii50sii20s')
        LOGIN_HEAD['uMessageSize'] += len(data_body)
        data_head = pack(LOGIN_HEAD)
        data_body = bytes(self.rc_Goto.Process(data_body))
        send_data = data_head + data_body
        self.t = int(time.time() * 1000)
        self.m_socket.send(send_data)
        logger.debug(log_msg(1, self.t, LOGIN_HEAD["bMainID"], LOGIN_HEAD["bAssistantID"], len(send_data)))

    # 解析成功
    def recv_Login(self):
        data = self.m_socket.recv()
        uMessageSize, bMainID, bAssistantID, bHandleCode, bReserve = unpack(data[:20])
        t = int(time.time() * 1000) - self.t
        logger.debug(log_msg(2, t, bMainID, bAssistantID, len(data)))
        _list = [
            'dwUserID', 'dwGamePower', 'dwMasterPower', 'dwMobile', 'dwAccID', 'dwLastLogonIP', 'dwNowLogonIP',
            'bLogoID', 'bBoy', 'szName', 'Wechat', 'szMD5Pass', 'nickName', 'i64Money', 'i64Bank', 'iLotteries',
            'dwFascination', 'dwDiamond', 'iRoomKey', 'szRealName', 'szIDCardNo', 'szMobileNo', 'szQQNum',
            'szAdrNation', 'szAdrProvince', 'szAdrCity', 'szZipCode', 'dwTimeIsMoney',
            'iVipTime', 'iDoublePointTime', 'iProtectTime', 'bLoginBulletin', 'iLockMathine',
            'iBindMobile', 'iAddFriendType', 'szAgentCode', 'nNameID', 'nRoomID', 'nDeskIndex',
            'szIP', 'nPort', 'szPwd', 'VIPLevel', 'IsYueKa', 'YueKatime', 'IsGetYkScore',
            'IsHaveBankPass', 'AgencyLevel', 'BankNo', 'Alipay', 'Exper', 'MachineCode', 'EBAT',
            'AgentID', 'IsCommonUser', 'UserChouShui']
        model = namedtuple('UserInfo', _list)
        # 登录成功解析返回数据
        s = '=iiiiiLLI?61s128s50s100sqqdiii50s36s50s20s50s50s50s10siiii?iii20siii50si60siiiiii20s50si64s100siii'
        User_Info = model._make(unpack(bytes(self.rc_Come.Process(data[20:])), s))

    # 获取游戏列表
    def send_Games(self):
        import struct
        AgentID = 14926056
        data_body = struct.pack('i', AgentID)
        data_body = bytes(self.rc_Goto.Process(data_body))
        self.rc_Goto.setCount(1)
        ASERVER_GAME_LIST['uMessageSize'] += len(data_body)
        ASERVER_GAME_LIST['bReserve'] = self.rc_Goto.getCount()
        data_head = pack(ASERVER_GAME_LIST)
        send_data = data_head + data_body
        self.t = int(time.time() * 1000)
        self.m_socket.send(send_data)
        logger.debug(
            log_msg(1, self.t, ASERVER_GAME_LIST["bMainID"], ASERVER_GAME_LIST["bAssistantID"], len(send_data)))

    # 解析第一次游戏所属类型
    def recv_Server_List(self):
        data = self.m_socket.recv()
        game_head = unpack(data[:20])
        res_body = data[20:]
        res_server = dict()
        for i in range(int((game_head[0] - 20) / 77)):
            servers = unpack(bytes(self.rc_Come.Process(res_body[i * 77:(i + 1) * 77])), s='=III61sI')
            res_server[str(servers[2])] = servers[3].decode('gbk').strip('\x00')
        setValue('servers', 'gametype', str(res_server))

    # 解析第二次游戏列表
    def recv_Game_List(self):
        data = self.m_socket.recv()
        game_head = unpack(data[:20])
        t = int(time.time() * 1000) - self.t
        logger.debug(log_msg(2, t, game_head[1], game_head[2], len(data)))
        res_body = data[20:]
        for i in range(int((game_head[0] - 20) / 146)):
            res = dict()
            games = unpack(bytes(self.rc_Come.Process(res_body[i * 146:(i + 1) * 146])), s='=IIII61s61sII')
            game = games[4].decode('gbk').strip('\x00')
            game_exe = games[5].decode('gbk').strip('\x00')
            res['game_code'], res['gametype'] = game, games[2]
            res['game_exe'], res['port'] = game_exe, games[7]
            setValue('GameList', game, str(res))

    def main(self):
        self.send_Connect()
        self.recv_Connect()
        self.send_Login()
        self.recv_Login()
        self.send_Games()
        self.recv_Server_List()
        self.recv_Game_List()


if __name__ == '__main__':
    a = AServer()
    a.main()
    _mysocket = MySocket()
    _a = GServer(_mysocket)
    _a.main()
    _mysocket.close()
