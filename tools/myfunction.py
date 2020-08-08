import ast
import configparser, struct, hashlib, re, traceback
import datetime
import time, base64
import psutil
from tools.get_code import Code
from loguru import logger
from tools.Config import *


def my_Log():
    # logger.add(LOG_PATH + '{time:%Y%m%d}.log',
    #            format='{time:YYYY-MM-DD HH:mm:ss}-process:{process}-{level}-{module}-{name}-{line}-{message}',
    #            encoding='utf-8', level='INFO')
    logger.add(LOG_PATH + '{time:%Y%m%d%H%M}_diff.log', format='{message}',
               encoding='utf-8', level='DEBUG')
    return logger


# 读取ini配置文件
def getValue(key, value):
    con = configparser.RawConfigParser()
    con.read(INI_PATH)
    result = con.get(key, value)
    return result


# 读取配置文件Int 类型
def getInt(option, key):
    con = configparser.ConfigParser()
    con.read(INI_PATH)
    return con.getint(option, key)


# 写回ini配置文件
def setValue(option, key, value):
    con = configparser.ConfigParser()
    con.read(INI_PATH, encoding='utf-8')
    try:
        if key != "":
            header = con[option]
            header[key] = value
            with open(INI_PATH, 'w', encoding='utf-8')as file:
                con.write(file)
    except Exception as e:
        traceback.print_exc()


CD_Cookies = lambda: getValue('chandao', 'cookies')


def get_buglist(chan_session, url):
    r = chan_session.get(url, cookies=ast.literal_eval(CD_Cookies()))
    return_list = list()
    bug_list = r.html.xpath('//*[@id="bugList"]/tbody/tr')
    for bug in bug_list:
        b = dict()
        b['id'] = bug.attrs['data-id']
        b['title'] = bug.xpath('//*[@class="c-title text-left"]', first=True).text
        b['url'] = f'http://192.168.0.42/zentao/bug-view-{b["id"]}.html'
        b['active'] = bug.xpath('//td[6]', first=True).text
        b['creat'] = bug.xpath('//td[7]', first=True).text
        b['to_user'] = bug.xpath('//td[9]', first=True).text
        return_list.append(b)
    return return_list


def get_tasklist(chan_session, url, cook=None):
    cook = cook if cook else ast.literal_eval(CD_Cookies())
    r = chan_session.get(url, cookies=cook)
    return_list = list()
    task_list = r.html.xpath('//*[@id="taskList"]/tbody/tr')
    for task in task_list:
        b = dict()
        b['id'] = task.attrs['data-id']
        b['title'] = task.xpath('//td[3]/a', first=True).text
        b['url'] = f'http://192.168.0.42/zentao/task-view-{b["id"]}.html'
        b['status'] = task.xpath('//td[4]/span', first=True).text
        b['to_user'] = task.xpath('//td[5]/a/span', first=True).text
        b['progress'] = task.xpath('//td[10]', first=True).text
        return_list.append(b)
    return return_list


# 禅道bug
def chandao_bugs(chan_session):
    urls = {'kk测试': 'http://192.168.0.42/zentao/bug-browse-6-0-unclosed.html',
            '商务部': 'http://192.168.0.42/zentao/bug-browse-8-0-unclosed.html',
            '伍佰棋牌': 'http://192.168.0.42/zentao/bug-browse-7-0-unclosed.html',
            '金牌娱乐': 'http://192.168.0.42/zentao/bug-browse-5-0-unclosed.html',
            '扑克王': 'http://192.168.0.42/zentao/bug-browse-4-0-unclosed.html',
            '必发娱乐': 'http://192.168.0.42/zentao/bug-browse-3-0-unclosed.html',
            '旗开得胜': 'http://192.168.0.42/zentao/bug-browse-2-0-unclosed.html'}

    bug_list = dict()
    for name in urls.keys():
        url = urls[name]
        r = chan_session.get(url, cookies=ast.literal_eval(CD_Cookies()))
        toal = int(r.html.xpath('//*[@class="label label-light label-badge"]', first=True).text)
        pages = toal // 20 + 1
        bug_list[name] = list()
        for i in range(pages):
            u = url.find('.html')
            link = f'{url[:u]}-0--{toal}-20-{i + 1}.html'
            bug_list[name] += get_buglist(chan_session, link)
    return bug_list


# 分页查询bug
def getBug_forPage(chan_session, page):
    url = 'http://192.168.0.42/zentao/bug-browse-6-0-unclosed.html'
    r = chan_session.get(url, cookies=ast.literal_eval(CD_Cookies()))
    toal = int(r.html.xpath('//*[@class="label label-light label-badge"]', first=True).text)
    u = url.find('.html')
    link = f'{url[:u]}-0--{toal}-20-{page + 1}.html'
    bugs = get_buglist(chan_session, link)
    return bugs


# 分页查询任务
def getTask_forPage(chan_session, page):
    task_url = 'http://192.168.0.42/zentao/project-task-5-unclosed.html'
    r = chan_session.get(task_url, cookies=ast.literal_eval(CD_Cookies()))
    toal = int(r.html.xpath('//*[@class="label label-light label-badge"]', first=True).text)
    u = task_url.find('.html')
    link = f'{task_url[:u]}-0--{toal}-20-{page + 1}.html'
    task_list = get_tasklist(chan_session, link)
    return task_list


# 禅道任务
def chandao_tasks(chan_session):
    task_url = 'http://192.168.0.42/zentao/project-task-5-unclosed.html'
    cookes = {'zentaosid': 'q8sjsmbmjkov0bs3hi4vve9h12', 'device': 'desktop', 'theme': 'default',
              'pagerProjectTask': '2000'}
    task_list = get_tasklist(chan_session, task_url, cookes)
    return task_list


# 获取验证码登录后台
def login_kk(dev, session):
    code = Code()
    url = getValue('environment', dev)
    code_url = url + f'/Login/GetValidateCode?time={int(time.time() * 1000)}'
    img = session.get(code_url)
    headers = img.headers
    img = code.get_code(base64.b64encode(img.content))
    if img:
        login_url = url + '/login/login'
        data = {'UserName': 'QA04', 'password': '123qwe', 'code': img}
        session.post(login_url, data, headers)
        return session


# 游戏报表
def report_game(dev, session):
    url = getValue('environment', dev)
    url = url + '/ReportForm/GetNewGameReportPage'
    data = {"pageIndex": 1,
            "pageSize": "50",
            "searchDate": "",
            "agentID": "0"}
    res = session.post(url, data)
    print(res.status_code, res.text)
    try:
        if res.status_code == 200 and res.json()['state'] == 1:
            msg = res.json()['value']
        else:
            msg = res.text
    except Exception as e:
        msg = res.text
    return msg


# 全局报表
def globle_report(dev, session):
    url = getValue('environment', dev)
    url = url + '/ReportForm/GetGlobalValue'
    data = {"time": "", "agentid": 0}
    res = session.post(url, data)
    print(res.status_code, res.text)
    try:
        if res.status_code == 200 and res.json()['state'] == 1:
            msg = res.json()['value']
        else:
            msg = res.text
    except Exception as e:
        msg = res.text
    return msg


# 性能监控
def alarm_performance():
    try:
        res = dict()
        res['cpu'] = psutil.cpu_percent()  # cpu 使用率
        memony = psutil.virtual_memory()
        res['memony_used'] = str(round(memony.used / 1024 / 1024 / 1024, 2))  # 已使用内存
        res['memony_total'] = str(round(memony.total / 1024 / 1024 / 1024, 2)) + 'G'  # 总内存
        res['memony_free'] = str(round(memony.free / 1024 / 1024 / 1024, 2)) + 'G'  # 未使用内存
        res['memony_pre'] = round(memony.used / memony.total * 100, 2)  # 内存使用率
        res['boot_time'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")  # 上次开机时间
        sum_threads = sum(list(psutil.Process(i).num_threads() for i in psutil.pids()))  # 根据进程号获取所有线程数
        res['sum_threads'] = sum_threads
        res['pids'] = len(psutil.pids())
        return res
    except:
        pass


class RC4(object):
    def __init__(self):
        self.perm = []
        self.index1 = 0
        self.index2 = 0
        self.key = None
        self.count = 0

    def Setkey(self, keybytes):
        self.key = keybytes
        self.perm = [0] * 256
        for i in range(256):
            self.perm[i] = i

        j = 0
        for i in range(256):
            j = (j + self.perm[i] + self.key[i % len(self.key)]) % 256
            self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

    def setCount(self, count):
        self.count = count

    def getCount(self):
        return self.count

    def Process(self, _data):
        j = 0
        output = [0] * len(_data)
        for i in range(len(_data)):
            self.index1 = (self.index1 + 1) % 256
            self.index2 = (self.index2 + self.perm[self.index1]) % 256
            self.perm[self.index1], self.perm[self.index2] = self.perm[self.index2], self.perm[self.index1]
            j = (self.perm[self.index1] + self.perm[self.index2]) % 256
            output[i] = _data[i] ^ self.perm[j]
        return output

    def ReadProcess(self, _data, _len):
        j = 0
        output = [0] * _len
        for i in range(_len):
            self.perm[self.index1], self.perm[self.index2] = self.perm[self.index2], self.perm[self.index1]

            j = (self.perm[self.index1] + self.perm[self.index2]) % 256
            output[i] = _data[i] ^ self.perm[j]
        return output

    def ReverseBytes(self, _Pointer, _Length):
        Temp = _Pointer
        for i in range(_Length):
            _Pointer[i] = Temp[_Length - i - 1]


def myMd5(msg):
    m = hashlib.md5()
    b = msg.encode('utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


def pack(data, s='iiiii'):
    s = struct.Struct(s)
    return s.pack(*data.values())


def unpack(data, s='iiiii'):
    return struct.unpack(s, data)


def c_to_fmt():
    import re
    path = 'D:\struck.txt'
    ft = {'int': 'i', 'INT': 'i', 'ULONG': 'L', 'UINT': 'I', 'bool': '?'}
    with open(path, 'r', encoding='utf-8')as f:
        datas = [i.split() for i in f.read().splitlines()]
    s = ''
    for i in datas:
        if len(i) < 2:
            continue
        if i[0] == 'int' or i[0] == 'INT':
            s += 'i'
        if i[0] == 'ULONG':
            s += 'L'
        if i[0] == 'UINT':
            s += 'I'
        if i[0] == 'bool':
            s += '?'
        if i[0] == 'char':
            l = str(re.search(r'.*\[(\d+)\];', i[1]).group(1)) + 's'
            s += l
        if i[0] == '__int64':
            s += 'q'
        if i[0] == 'DOUBLE':
            s += 'd'
        else:
            print('找不到类型', i[0])
    print(s)


def c_fmt():
    p = re.compile(r'\s?(?P<_type>\w+)\s+(?P<key>[^\[;]+)(\([?P<size>\d+)\])?.+')
    source = 'D:\struck.txt'

    def c():
        for m in p.finditer(source):
            if not m:
                continue
            yield m.groupdict()

    fields = tuple(c())
    f = ''.join(f'{field["size"] or ""}{d_type[field["_type"]]}' for field in fields)
