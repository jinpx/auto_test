# -*- coding:utf-8 -*-
import configparser, os, traceback, time
from loguru import logger


def my_Log():
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/')
    logger.add(BASE_DIR + '{time:%Y%m%d}.log',
               format='{time:YYYY-MM-DD HH:mm:ss}-process:{process}-{level}-{module}-{name}-{line}-{message}',
               encoding='utf-8', level='INFO')
    logger.add(BASE_DIR + '{time:%Y%m%d%H%M%S}_diff.log',format='{message}',
               encoding='utf-8', level='DEBUG')
    return logger


# 读取ini配置文件
def getValue(key, value):
    con = configparser.RawConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    con.read(config_path)
    result = con.get(key, value)
    return result


# 读取配置文件Int 类型
def getInt(option, key):
    con = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    con.read(config_path)
    return con.getint(option, key)


# 写回ini配置文件
def setValue(option, key, value):
    con = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    con.read(config_path, encoding='utf-8')
    try:
        if key != "":
            header = con[option]
            header[key] = value
            with open(config_path, 'w', encoding='utf-8')as file:
                con.write(file)
    except Exception as e:
        traceback.print_exc()

# class Logger(object):
#     def __init__(self):
#         """
#             指定保存日志的文件路径，日志级别，以及调用文件
#             将日志存入到指定的文件中
#         """
#         # 创建一个logger
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.DEBUG)
#
#         # 创建一个handler，用于写入日志文件
#         rq = time.strftime('%Y%m%d', time.localtime(time.time()))
#         log_path = os.path.join(os.path.dirname(__file__), '../logs/')
#         log_name = log_path + rq + '.log'
#         fh = logging.FileHandler(log_name, encoding="utf-8")
#         fh.setLevel(logging.INFO)
#
#         # 再创建一个handler，用于输出到控制台
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.INFO)
#
#         # 定义handler的输出格式
#         formatter = logging.Formatter(
#             '%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(lineno)d - %(message)s')
#         fh.setFormatter(formatter)
#         ch.setFormatter(formatter)
#
#         # 给logger添加handler
#         self.logger.addHandler(fh)
#         self.logger.addHandler(ch)
#
#     def getlog(self):
#         return self.logger


# if __name__ == '__main__':
#     from loguru import logger
#     logger.info('你是一条狗')
#     logger.debug('你还是一条狗')

