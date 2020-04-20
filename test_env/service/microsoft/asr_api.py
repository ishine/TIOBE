#!/usr/bin/python3
# Request module must be installed.
# Run pip install requests if necessary.
# doc: https://docs.azure.cn/zh-cn/cognitive-services/speech-service/rest-speech-to-text

import sys
import requests, json, time
import codecs

#def get_token(subscription_key):
#    fetch_token_url = 'https://chinaeast2.api.cognitive.azure.cn/sts/v1.0/issueToken'
#    headers = {
#        'Ocp-Apim-Subscription-Key': subscription_key
#    }
#    response = requests.post(fetch_token_url, headers=headers)
#    access_token = str(response.text)
#    print(access_token)
#
#get_token(subscription_key)

lang='zh-CN'
MAX_RETRY=10

KEY=''
with open('SUBSCRIPTION_KEY', 'r') as f:
    KEY = f.readline().strip()

def recognize(key, audio):
    url='https://chinaeast2.stt.speech.azure.cn/speech/recognition/conversation/cognitiveservices/v1?language='+lang

    headers = {
        'Accept': 'application/json;text/xml',
        'Content-Type': 'audio/wav;codecs="audio/pcm";samplerate=16000',
        'Ocp-Apim-Subscription-Key': KEY,
        'format': 'detailed'
    }

    with open(audio, 'rb') as f:
        audio_data = f.read()

    #print(url, headers)
    rec = ''
    for i in range(MAX_RETRY):
        try:
            r = requests.post(url, data=audio_data, headers=headers)
            sys.stderr.write(r.text + '\n')
            rec = json.loads(r.text)['DisplayText']
            if rec == '':
                sys.stderr.write(audio + " empty rec result, retrying\n")
                time.sleep(1.0)
                continue
            break
        except:
            sys.stderr.write(audio + " exception, retrying\n")
            time.sleep(1.0)
            continue
    return rec

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("rest_api.py <in_scp> <out_trans>\n")
        exit(-1)
    
    SCP = sys.argv[1]
    TRANS = sys.argv[2]

    scp_file = codecs.open(SCP, 'r', 'utf8')
    trans_file = codecs.open(TRANS, 'w+', 'utf8')
    
    n = 0
    for l in scp_file:
        l = l.strip()
        if l == '':
            continue
    
        key, audio = l.split('\t')
        sys.stderr.write(str(n) + '\tkey:' + key + '\taudio:' + audio + '\n')
        sys.stderr.flush()

        rec_text = ''
        rec_text = recognize(KEY, audio)
    
        trans_file.write(key + '\t' + rec_text + '\n')
        trans_file.flush()
        n += 1

    scp_file.close()
    trans_file.close()

