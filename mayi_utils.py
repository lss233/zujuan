# Python 3.x
import hashlib
import time
import requests
import json
import urllib
import os

# 找群主购买 my_app_key, myappsecret, 以及蚂蚁代理服务器的 mayi_url 地址和 mayi_port 端口
my_app_key = "76854064"
app_secret = "a6ffd061b9f1f2559f7e8262a5122085"
mayi_url = 's4.proxy.mayidaili.com'
mayi_port = '8123'

# 蚂蚁代理服务器地址
mayi_proxy = {'http': 'http://{}:{}'.format(mayi_url, mayi_port)}

# 准备去爬的 URL 链接
url = 'http://zujuan.21cnjy.com/question/detail/4119613'

# 计算签名
timesp = '{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
codes = app_secret + 'app_key' + my_app_key + 'timeout5000' + 'timestamp' + timesp + app_secret
sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()

# 拼接一个用来获得蚂蚁代理服务器的「准入」的 header (Python 的 concatenate '+' 比 join 效率高)
authHeader = 'MYH-AUTH-MD5 sign=' + sign + '&app_key=' + my_app_key + '&timeout=5000' + '&timestamp=' + timesp 

# 用 Python 的 Requests 模块。先订立 Session()，再更新 headers 和 proxies 
s = requests.Session()
s.headers.update({'Proxy-Authorization': authHeader, 'user-agent': 'Mozilla/5.0'})
s.proxies.update(mayi_proxy)

def find_beg(text):
    beg = text.find('MockDataTestPaper')
        
    beg_location = text.find('[', beg)

    return beg_location

def find_end(text, beg):
    end = text.find('OT2.renderQList', beg)
    return end


def download(url, params=None, cookies=None):
    finished = False
    timeout_count = 0
    no_answer_count = 0
    while not finished:
        try:
            print("Downloading: ", url)
            pg = s.get(url, timeout=60, params=params, cookies=cookies)  # tuple: 300 代表 connect timeout, 270 代表 read timeout
            text = pg.text
            start = find_beg(text)
            end = find_end(text, start)

            '''
            json_file = open(os.getcwd() + '\\json\\' + url.split('/')[-1] + '.json', 'w', encoding='utf-8')
            json_file.write(str(text[start: end]))
            json_file.close()
            '''

            json_obj = json.loads(text[start: end].strip('\t\n; '))

            if json_obj[0]['questions'][0]['answer'] == '':
                if 'list' in json_obj[0]['questions'][0]:
                    pass
                else:
                    print("No answer")
                    no_answer_count += 1
                    if no_answer_count == 5:
                        finished = True
                    continue
        except Exception as e:
            print(e)
            timeout_count += 1
            if timeout_count == 5:
                finished = True
            continue
        return pg
    return None

def download_normal(url, params=None, cookies=None):
    finished = False
    count = 0
    while not finished:
        try:
            pg = s.get(url, timeout=60, params=params, cookies=cookies)
        except:
            count += 1
            if count == 5:
                finished = True
        return pg
    return None