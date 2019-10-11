# coding=utf-8

'''
this test script is based on the official demo release:
    https://github.com/Baidu-AIP/speech-demo/rest-api-asr/python/asr_raw.py

'''

import sys
import json
import time
import codecs

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode

    timer = time.perf_counter
else:
    import urllib2
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

# authentication
API_KEY = ''
SECRET_KEY = ''
with open('API_KEY', 'r') as f:
    API_KEY = f.readline().strip()
with open('SECRET_KEY', 'r') as f:
    SECRET_KEY = f.readline().strip()

CUID = '123456PYTHON';
RATE = 16000;  # 采样率


# 普通版
DEV_PID = 1536;  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

#测试自训练平台需要打开以下信息， 自训练平台模型上线后，您会看见 第二步：“”获取专属模型参数pid:8001，modelid:1234”，按照这个信息获取 dev_pid=8001，lm_id=1234
# DEV_PID = 8001 ;   
# LM_ID = 1234 ;

# 极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版（开通后可能会收费）

#DEV_PID = 80001
#ASR_URL = 'http://vop.baidu.com/pro_api'
#SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里开通极速版

# 忽略scope检查，非常旧的应用可能没有
# SCOPE = False


# 极速版

class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("rest_api.py <in_scp> <out_trans>")
        exit(-1)

    """
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler)
    urllib2.install_opener(opener)
    """

    token = fetch_token()

    SCP = sys.argv[1]    # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
    TRANS = sys.argv[2]  # output result in Kaldi's trans format
    FORMAT = 'wav'       # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
    MAX_RETRY = 10

    scp_file = codecs.open(SCP, 'r', 'utf8')
    trans_file = codecs.open(TRANS, 'w+', 'utf8')

    n = 0

    for l in scp_file:
        key = ''
        audio = ''
        audio = l.strip()
        if audio == '':
            continue
        
        cols = l.split('\t')
        assert(len(cols) == 2)
        key = cols[0].strip()
        audio = cols[1].strip()
        sys.stderr.write(str(n) + '\t' + key + '\t')

        speech_data = []
        with open(audio, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % audio)

        params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
        #测试自训练平台需要打开以下信息
        #params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID, 'lm_id' : LM_ID}
        params_query = urlencode(params);

        headers = {
            'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
            'Content-Length': length
        }

        url = ASR_URL + "?" + params_query
        req = Request(ASR_URL + "?" + params_query, speech_data, headers)
        time.sleep(0.55)  # baidu API calling limitation: 2 qps for free
        for i in range(MAX_RETRY): # retry
            try:
                begin = timer()
                f = urlopen(req)
                result_str = f.read()
                sys.stderr.write("Request time cost %f \n" % (timer() - begin))
                break
            except:
                if i != (MAX_RETRY-1):
                    time.sleep(0.55)
                    continue
                else:
                    sys.stderr.write('Failed after multiple retries.\n')
                    exit(-1)

        if (IS_PY3):
            result_str = str(result_str, 'utf-8')

        n+=1
        sys.stderr.write(result_str + '\n')
        result = json.loads(result_str)
        rec_text = result['result'][0].strip()
        trans_file.write(key + '\t' + rec_text + '\n')
        trans_file.flush()

    scp_file.close()
    trans_file.close()

