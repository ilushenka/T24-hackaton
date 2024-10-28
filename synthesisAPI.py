import os
import base64
import httpx
import wave
import re

from tinkoff.cloud.tts.v1 import tts_pb2
from google.protobuf.json_format import MessageToDict

endpoint = "api.tinkoff.ai:443"
sample_rate = 48000

def text_to_ssml(text:str):
    daughter_name = 'alyona'
    father_name = 'dorofeev'
    replacements = {'**Дочка:**': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Девочка:**': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Девочка**:': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Дочка**:': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Дочь:**': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Дочь**:': f"<break time='400ms'/> </prosody> </voice> <voice name = '{daughter_name}'> <prosody pitch ='110%'>",
                    '**Отец:**': f"<break time='400ms'/> </prosody> </voice> <voice name = '{father_name}'> <prosody pitch ='60%'>",
                    '**Отец**:': f"<break time='400ms'/> </prosody> </voice> <voice name = '{father_name}'> <prosody pitch ='60%'>",
                    '**Папа:**': f"<break time='400ms'/> </prosody> </voice> <voice name = '{father_name}'> <prosody pitch ='60%'>",
                    '**Папа**:': f"<break time='400ms'/> </prosody> </voice> <voice name = '{father_name}'> <prosody pitch ='60%'>",
                    '!':"<break time='400ms'/>",
                    '(Дочка радость)':f"<voice name = '{daughter_name}:funny'>",
                    '(Дочка грусть)':f"<voice name = '{daughter_name}:sad'>",
                    '(Дочь радость)':f"<voice name = '{daughter_name}:funny'>",
                    '(Дочь грусть)':f"<voice name = '{daughter_name}:sad'>",
                    '(Девочка радость)':f"<voice name = '{daughter_name}:funny'>",
                    '(Девочка грусть)':f"<voice name = '{daughter_name}:sad'>",
                    '(Отец радость)':f"<voice name = '{father_name}:comedy'>",  
                    '(Отец грусть)':f"<voice name = '{father_name}:tragedy'>",  
                    '(Папа радость)':f"<voice name = '{father_name}:comedy'>",  
                    '(Папа грусть)':f"<voice name = '{father_name}:tragedy'>",  
                    '(конец)':"</voice>"}  
    pattern = re.compile('|'.join(map(re.escape, replacements.keys())))
    result = f"<speak> <voice name = '{father_name}'> <prosody pitch ='80%'>"
    result += pattern.sub(lambda match: replacements[match.group(0)], text)
    result += '</prosody> </voice> </speak>'
    return result

def build_request_from_pb(text):
    return MessageToDict(tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(ssml=text_to_ssml(text)),
            audio_config=tts_pb2.AudioConfig(
                audio_encoding=tts_pb2.LINEAR16,
                sample_rate_hertz=sample_rate,)))

def synthesis_main(text=None, token=None):
    with httpx.Client(http2=True) as client:
        request = build_request_from_pb(text)
        metadata = [("authorization", f"Bearer {token}")]
        response = client.post(f"http{'s' if endpoint.endswith('443') else ''}://{endpoint}/v1/tts:synthesize", json=request, headers=metadata, timeout=None)

        if response.status_code != 200:
            print(f"REST failed with HTTP code {response.status_code}\nHeaders: {response.headers}\nBody: {response.text}")
        else:
            response = response.json()
            
            with wave.open("synthesized.wav", "wb") as f:
                f.setframerate(sample_rate)
                f.setnchannels(1)
                f.setsampwidth(2)
                f.writeframes(base64.b64decode(response['audio_content']))

def synthesis(text=None, token=None):
        synthesis_main(text, token)
    