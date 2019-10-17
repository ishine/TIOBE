#!/usr/bin/python3
# coding: utf8
'''
this code is based on official sdk demo at:
    https://github.com/googleapis/google-cloud-python/blob/master/speech/samples/v1/speech_transcribe_sync.py

Cloud Speech-to-Text API documentation entry can be found here:
    https://cloud.google.com/speech-to-text/
'''
# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_sync")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Transcribe Audio File (Local File)
#   description: Transcribe a short audio file using synchronous speech recognition
#   usage: python3 samples/v1/speech_transcribe_sync.py [--local_file_path "resources/brooklyn_bridge.raw"]

# [START speech_transcribe_sync]
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

import io, sys
import codecs

def transcribe_file(client, file_name):
    """
    Transcribe a short audio file using synchronous speech recognition
    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
    # Instantiates a client
    #client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "zh"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16

    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }

    # Loads the audio into memory
    with io.open(file_name, 'rb') as f:
        content = f.read()
    audio = {"content": content}

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    #for result in response.results:
    #    # First alternative is the most probable result
    #    alternative = result.alternatives[0]
    #    print(u"Transcript: {}".format(alternative.transcript))

    rec_text = ''
    for result in response.results:
        rec_text += result.alternatives[0].transcript
    return rec_text
# [END speech_transcribe_sync]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("rest_api.py <in_scp> <out_trans>\n")
        exit(-1)
    
    SCP = sys.argv[1]
    TRANS = sys.argv[2]
    
    client = speech_v1.SpeechClient()

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

        rec_text = transcribe_file(client, audio)
    
        trans_file.write(key + '\t' + rec_text + '\n')
        trans_file.flush()
        n += 1

    scp_file.close()
    trans_file.close()

