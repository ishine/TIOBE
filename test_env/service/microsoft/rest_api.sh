subscription_key=`cat SUBSCRIPTION_KEY`

language="zh-CN"

filename=test.wav

#token=$(curl -v -X POST \
#  "https://chinaeast2.api.cognitive.azure.cn/sts/v1.0/issueToken" \
#  -H "Content-type: application/x-www-form-urlencoded" \
#  -H "Content-Length: 0" \
#  -H "Ocp-Apim-Subscription-Key: $subscription_key")
#
#echo $token

url="https://chinaeast2.stt.speech.azure.cn/speech/recognition/conversation/cognitiveservices/v1"
url+="?language=$language"
Accept="Accept:application/json;text/xml"
ContentType="Content-Type:audio/wav;codecs=\"audio/pcm\";samplerate=16000"
Auth="Ocp-Apim-Subscription-Key:$subscription_key"
Format="format=detailed"
#url+="&Accept:application/json;text/xml"

echo $url
curl -X POST $url -H $Auth -H $Accept -H $ContentType -H $Format --data-binary @$filename

echo "Done"

