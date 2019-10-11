#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
this code is based on official demo at:
    https://cloud.tencent.com/document/product/1093/35734
    一句话识别 python SDK
    install SDK: pip install tencentcloud-sdk-python
'''

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.asr.v20190614 import asr_client, models 
import base64
import sys, codecs, json

try: 
    if len(sys.argv) != 3:
        sys.stderr.write("rest_api.py <in_scp> <out_trans>\n")
        exit(-1)
    
    SCP = sys.argv[1]
    TRANS = sys.argv[2]

    MAX_RETRY = 10
    
    #重要：<Your SecretId>、<Your SecretKey>需要替换成客户自己的账号信息
    #请参考接口说明中的使用步骤1进行获取。 
    secret_id = ''
    secret_key = ''
    with open('SECRET_ID', 'r') as f:
        secret_id = f.readline().strip()

    with open('SECRET_KEY', 'r') as f:
        secret_key = f.readline().strip()

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

        #fwave = open('./test.wav', mode='r')
        #data = str(fwave.read())
        #dateLen = len(data)
        #base64Wav = base64.b64encode(data)

        #读取文件以及base64
        with open(audio, mode='rb') as f:
          data = f.read()
          dataLen = len(data)
          base64Wav = base64.b64encode(data)

        for i in range(MAX_RETRY):
            try:
                cred = credential.Credential(secret_id, secret_key) 
                httpProfile = HttpProfile()
                httpProfile.endpoint = "asr.tencentcloudapi.com"
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile) 
    
                #发送请求
                req = models.SentenceRecognitionRequest()
                params = {"ProjectId":0,"SubServiceType":2,"EngSerViceType":"16k","SourceType":1,"Url":"","VoiceFormat":"wav","UsrAudioKey":"session-123", "Data":base64Wav, "DataLen":dataLen}
                req._deserialize(params)
    
                resp = client.SentenceRecognition(req) 
                #print(resp.to_json_string())
                rec_text = json.loads(resp.to_json_string())['Result']
                break
            except:
                continue

        n += 1
        trans_file.write(key + '\t' + rec_text + '\n')
        trans_file.flush()

    scp_file.close()
    trans_file.close()

except TencentCloudSDKException as err: 
    print(err) 
