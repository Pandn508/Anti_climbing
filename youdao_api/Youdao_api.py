import requests
from time import time
from random import randint, sample
import hashlib
from urllib import request, parse
import re

class youdao():
    def fanyi(url, data):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            }
            data = parse.urlencode(data).encode()
            req = request.Request(url=url, data=data, headers=header)
            rsq = request.urlopen(req)
            html = rsq.read().decode()
            tgt = re.findall('"tgt":"([\s\S]+?)"', html)
            tgt1 = ' '.join(tgt)
            src = re.findall('"src":"([\s\S]+?)"', html)
            src1 = ' '.join(src)
            print('原文：', src1)
            print('翻译：', tgt1)

            responce = requests.get(url, headers=header, params=data)
            responce.encoding = responce.apparent_encoding
            if responce.status_code == 200:
                return responce.text
            return 'link wrong'
        except requests.RequestException:
            return 'wrong'

    def hex5(value):
        manipulator = hashlib.md5()
        manipulator.update(value.encode('utf-8'))
        return manipulator.hexdigest()

    def main(i):
        ts = round(time() * 1000)
        bv = '42160534cfa82a6884077598362bbc9d'
        salt = ts + randint(1, 10)
        sign = youdao.hex5("fanyideskweb" + i + str(salt) + "Nw(nmmbP%A-r6U3EUn]Aj")
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {
            'i': i,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': str(salt),
            'sign': str(sign),
            'ts': str(ts),
            'bv': str(bv),
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
        youdao.fanyi(url, data)

if __name__ == '__main__':
    i = "GitHub is built for collaboration. Set up an organization to improve the way your" \
        " team works together, and get access to more features."
    youdao.main(i)
