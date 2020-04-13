#!/usr/bin/python3
import base64
import requests
import json
import io, sys
import codecs
import time

MAX_RETRY=10

def encode_audio(path):
  with open(path, "rb") as audio_file:
    encoded_string = base64.b64encode(audio_file.read())
  return encoded_string.decode('ascii')

def recognize(appid, token, path):
  data = {
    'config': {
      'encoding': 'LINEAR16',
      'sample_rate_hertz': 16000,
      'language_code': 'zh-cmn-Hans-CN'
    },
    'audio': {
      'content': encode_audio(path)
    }
  }
  headers = {
    'Content-Type': 'application/json',
    'Appid': appid,
    'Authorization': 'Bearer ' + token
  }

  rec = ''
  for i in range(MAX_RETRY):
    try:
      rec = ''
      r = requests.post('https://api.zhiyin.sogou.com/apis/asr/v1/recognize', data=json.dumps(data), headers=headers)
      rec = json.loads(r.text)['results'][0]['alternatives'][0]['transcript']
      if rec != "":
          break;
    except:
      sys.stderr.write("exception, retrying.\n")
      time.sleep(1.0)
      continue
  return rec

with open('APP_ID', 'r') as f:
    APP_ID = f.readline().strip()

with open('TOKEN', 'r') as f:
    token_string = f.readline().strip()
    TOKEN = json.loads(token_string)['token']
    #print(TOKEN)


#response = recognize(APP_ID, TOKEN, 'test.wav')
#rec_text = json.loads(response)['results'][0]['alternatives'][0]['transcript']
#print (rec_text)

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
        rec_text = recognize(APP_ID, TOKEN, audio)
    
        trans_file.write(key + '\t' + rec_text + '\n')
        trans_file.flush()
        n += 1

    scp_file.close()
    trans_file.close()

