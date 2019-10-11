#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
The code is base on official documentation at:
    https://help.aliyun.com/document_detail/92131.html
    一句话识别RESTful API2.0
'''
# Python 2.x 引入httplib模块
# import httplib
# Python 3.x 引入http.client模块
import http.client
import json
import sys
import codecs

def process(request, token, audioFile) :
    MAX_RETRY = 10
    # 读取音频文件
    with open(audioFile, mode = 'rb') as f:
        audioContent = f.read()
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    # 设置HTTP请求头部
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': len(audioContent)
        }
    # Python 2.x 请使用httplib
    # conn = httplib.HTTPConnection(host)
    # Python 3.x 请使用http.client

    result = ''
    for i in range(MAX_RETRY):
        try:
            #print("hey")
            conn = http.client.HTTPConnection(host)
            #print(conn)
            conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)
            response = conn.getresponse()
            #print(response)

            body = response.read()
            #print(body)
            body = json.loads(body)
            #print(body)

            status = body['status']
            is_success = body['message']
            if status == 20000000 and is_success == 'SUCCESS':
                result = body['result']
                conn.close()
                break;
            else :
                sys.stderr.write('Failed recognizing, will retry.\n')
                conn.close()
                sleep(0.5)
                continue
        except:
            sys.stderr.write('Exception, will retry.\n')
            conn.close()
            sleep(0.5)
            continue

    return result

appKey = ''
with open('APPKEY', 'r') as f:
    appKey = f.readline().strip()

token = ''
with open('TOKEN', 'r') as f:
    token = f.readline().strip()

# 服务请求地址
url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
# 音频文件
format = 'wav'
sampleRate = 16000

enablePunctuationPrediction  = True
enableInverseTextNormalization = True
enableVoiceDetection  = False

# 设置RESTful请求参数
request = url + '?appkey=' + appKey
request = request + '&format=' + format
request = request + '&sample_rate=' + str(sampleRate)
if enablePunctuationPrediction :
    request = request + '&enable_punctuation_prediction=' + 'true'
if enableInverseTextNormalization :
    request = request + '&enable_inverse_text_normalization=' + 'true'
if enableVoiceDetection :
    request = request + '&enable_voice_detection=' + 'true'

sys.stderr.write('Request: ' + request + '\n')

if len(sys.argv) != 3:
    sys.stderr.write("rest_api.py <in_scp> <out_trans>\n")
    exit(-1)

SCP = sys.argv[1]
TRANS = sys.argv[2]

scp_file = codecs.open(SCP, 'r', 'utf8')
trans_file = codecs.open(TRANS, 'w+', 'utf8')
n = 0
for l in scp_file:
    if l.strip() == '':
        continue

    key = ''
    audio = ''

    cols = l.split('\t')
    assert(len(cols) == 2)
    key = cols[0].strip()
    audio = cols[1].strip()

    sys.stderr.write(str(n) + '\t' + key + '\n')
    rec_text = ''
    rec_text = process(request, token, audio)
    n += 1

    trans_file.write(key + '\t' + rec_text + '\n')
    trans_file.flush()

scp_file.close()
trans_file.close()

