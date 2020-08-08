import hashlib, re, time

import requests


def CalcSign(pd_id, sign, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + sign).encode())
    csign = md5.hexdigest()
    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


class Code(object):
    """解析数字验证码"""

    def __init__(self):
        self.user_id = '124466'
        self.sign = 'YK+bAvFIfe5qFdtQLfgHQ2xgilKQHgd+'
        self.url = 'http://pred.fateadm.com'
        self.predict_type = '10400'  # 4位纯数字
        self.session = requests.Session()

    def get_balace(self):
        url = self.url + '/api/custval'
        tm = str(int(time.time()))
        param = {'user_id': self.user_id, 'sign': CalcSign(self.user_id, self.sign, tm), 'timestamp': tm}
        res = self.session.post(url, param)
        print(res.text)

    def get_code(self, img_data):
        url = self.url + '/api/capreg'
        tm = str(int(time.time()))
        param = {'user_id': self.user_id, 'sign': CalcSign(self.user_id, self.sign, tm), 'timestamp': tm,
                 'predict_type': self.predict_type, 'img_data': img_data}
        res = self.session.post(url, data=param).json()
        if res['RetCode'] == '0':
            code = re.findall('(\d+)', res['RspData'])[0]
        else:
            code = None
        return code


if __name__ == '__main__':
    a = Code()
    a.get_balace()
