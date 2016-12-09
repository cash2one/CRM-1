#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Doc String'''


import StringIO
import gzip
import urllib
import ssl
import socket
import re
from string import Template


T_HTTPS_DATA = Template('''POST $relative_path HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
X-HttpWatch-RID: 44415-10046
Referer: http://login.jiayuan.com/
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
User-Agent: Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Host: $host
Content-Length: $content_length
DNT: 1
Connection: Keep-Alive
Cache-Control: no-cache

$post_content''')

MAX_LENGTH = 8192


def gz_decode(data):
    '''gzip decode'''
    try:
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        data = gziper.read()
        return data
    except Exception,e:
        return None


def encode_post_data(post_data):
    for key, val in post_data.iteritems():
        if val == '0':post_data[key] = ''
    return urllib.urlencode(post_data)


def split_header(data):
    start_pos = data.find('\r\n\r\n')
    if start_pos < 0 or start_pos >= len(data):
        return (None, None)
    else:
        return (data[:start_pos], data[start_pos + 4:])


def chunk_decode(message):
    chunk_segment = message.split('\r\n')
    try:
        i = 0;
        result = ''
        while True:
            length = int(chunk_segment[i], 16)
            if length == 0:
                if len(chunk_segment[i+1]) == 0 and len(chunk_segment[i+2]) == 0:
                    return result
                else:
                    return None
            else:
                if len(chunk_segment[i+1]) == length:
                    result = result + chunk_segment[i+1]
                else:
                    return None
            i = i + 2
    except Exception,e:
        return None


def get_host(url):
    pattern = re.compile(r'http[s]{0,1}://(\S+?)/')
    s = pattern.match(url)
    if s:
        return s.group(1)
    else:
        return ''


def http_decode(data):
    if data is None:
        return None
    header, message = split_header(data)
    if header is None or message is None:
        return None
    if data.count('Transfer-Encoding: chunked'):
        message = chunk_decode(message)
    if message is None:
        return None
    if data.count('Content-Encoding: gzip'):
        message = gz_decode(message)
    return (header, message)


def https_post(passport_url, login_data):
    host = get_host(passport_url)
    if len(host) == 0:
        return None
    relative_path = passport_url[passport_url.find(host) + len(host):]
    post_content = encode_post_data(login_data)
    https_data = T_HTTPS_DATA.substitute({'host':host,
                                          'post_content':post_content,
                                          'content_length':len(post_content),
                                          'relative_path':relative_path
                                          })
    try:
        sock = ssl.wrap_socket(socket.socket(), ssl_version=ssl.PROTOCOL_SSLv3)
        sock.connect((host,443))
        sock.sendall(https_data)
        recv_data = sock.recv(MAX_LENGTH)
        sock.close()
        return http_decode(recv_data)
    except Exception,e:
        print e
        return None, None


if __name__ == "__main__":
    passport_url = r"https://dts.100credit.com/als/custom/create_user/"
    data = {'login_name':'test111', 'user_name':'客户名称', 'email':'xue.bai@100credit.com', 'analy':'分析师1'}
    header,message = https_post(passport_url, data)
    print message
    # passport_url = r'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'
    # payload = {'name':'baixuexue123@sina.com',
    #            'password': 'xuebailove321',
    #            '_s_x_id': '232224f0b279d8e650d5b61aebd5804b',
    #            'm_p_l': '1',
    #            'ljg_login': '1',
    #            'position': '0',
    #            'channel': '0',
    #            'remem_pass': 'on',
    #            }
    # # header,message = https_post(passport_url, payload)
    # # print
    # # print header
    # # print
    # # print message
    # import urllib, urllib2, cookielib
    # import monkey
    # cj = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # urllib2.install_opener(opener)
    # loginRequest = urllib2.Request(passport_url, urllib.urlencode(payload))
    # loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    # loginRequest.add_header('Accept-Encoding','gzip,deflate')
    # loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8')
    # loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
    # loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
    # response = urllib2.urlopen(loginRequest)
    # print  response.geturl()
    # print response.info()
    # content = response.read()
    # print gz_decode(content)









    

