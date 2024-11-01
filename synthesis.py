from tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2
import grpc
import os
import wave
import re

sample_rate = 48000

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIxUGNSUGsvMVo3WG9QSGxIS3d2cmdWUkxnQ1ZFTnByRHZPK1ArODM2NHM9VFRTX1RFQU0ifQ.eyJpc3MiOiJ0ZXN0X2lzc3VlciIsInN1YiI6InRlc3RfdXNlciIsImF1ZCI6InRpbmtvZmYuY2xvdWQudHRzIiwiZXhwIjoxNzI5OTY5NjcwLjB9.6AzSCacRLHMqPp_oQOBmgdJbFqTT10c2oGYz28t5Bys'
endpoint = "api.tinkoff.ai:443"

text = """**Дочка:** Привет, пап! Я только что прочитала статью о тензорах. Что это вообще такое?

**Отец:** Привет, солнышко! Тензоры — это такие математические объекты, которые помогают описывать разные вещи в науке. Они могут представлять многомерные данные. Например, если вектор — это просто направленная величина, то тензор может иметь много таких направлений.

**Дочка:** А как они выглядят? Они как-то отличаются от обычных чисел?

**Отец:** Да, именно! Представь, что тензор — это многомерный массив чисел. Например, скаляр — это одно число, вектор — это набор чисел, а матрица — это уже двумерный массив. Чем выше порядок тензора, тем больше измерений он охватывает.

**Дочка:** Интересно! А что значит "порядок" тензора?

**Отец:** Порядок тензора показывает, сколько индексов нужно, чтобы его описать. Например, у скаляра порядок 0, у вектора порядок 1, а у матрицы порядок 2. Тензоры более высокого порядка могут быть очень сложными!

**Дочка:** А как тензоры меняются, если поменять систему координат?

**Отец:** Это очень важный момент! Тензоры изменяются по определённым правилам при переходе от одной системы координат к другой. Например, если ты вращаешь систему координат, компоненты вектора будут изменяться по специальным формулам.

**Дочка:** Звучит сложно. А где тензоры используются на практике?

**Отец:** Они используются в разных областях. Например, в физике, в механике, в электромагнетизме и даже в теории относительности. Тензоры помогают описывать такие вещи, как гравитация или напряжения в материалах.

**Дочка:** О, я слышала о теории относительности! Как тензоры там помогают?

**Отец:** В теории относительности тензоры связывают геометрию пространства-времени с материей и энергией. Например, тензор Эйнштейна показывает, как масса и энергия влияют на кривизну пространства-времени.

**Дочка:** Это звучит как что-то из фильмов! А можно ли тензоры как-то визуализировать?

**Отец:** Визуализировать тензоры бывает непросто, но можно представить их как многомерные фигуры. Например, матрицу можно представить как таблицу, а более сложные тензоры — как кубы или гиперкубы.

**Дочка:** Пап, а в каких ещё областях могут быть тензоры?

**Отец:** Они также используются в континуум механике для описания напряжений в материалах и в электродинамике для объединения электрических и магнитных полей. Тензоры действительно универсальны!

**Дочка:** Спасибо, пап! Теперь я понимаю, почему тензоры такие важные! Буду дальше изучать их.

**Дочка:** Привет, пап! Я только что прочитала статью о тензорах. Что это вообще такое?

**Отец:** Привет, солнышко! Тензоры — это такие математические объекты, которые помогают описывать разные вещи в науке. Они могут представлять многомерные данные. Например, если вектор — это просто направленная величина, то тензор может иметь много таких направлений.

**Дочка:** А как они выглядят? Они как-то отличаются от обычных чисел?

**Отец:** Да, именно! Представь, что тензор — это многомерный массив чисел. Например, скаляр — это одно число, вектор — это набор чисел, а матрица — это уже двумерный массив. Чем выше порядок тензора, тем больше измерений он охватывает.

**Дочка:** Интересно! А что значит "порядок" тензора?

**Отец:** Порядок тензора показывает, сколько индексов нужно, чтобы его описать. Например, у скаляра порядок 0, у вектора порядок 1, а у матрицы порядок 2. Тензоры более высокого порядка могут быть очень сложными!

**Дочка:** А как тензоры меняются, если поменять систему координат?

**Отец:** Это очень важный момент! Тензоры изменяются по определённым правилам при переходе от одной системы координат к другой. Например, если ты вращаешь систему координат, компоненты вектора будут изменяться по специальным формулам.

**Дочка:** Звучит сложно. А где тензоры используются на практике?

**Отец:** Они используются в разных областях. Например, в физике, в механике, в электромагнетизме и даже в теории относительности. Тензоры помогают описывать такие вещи, как гравитация или напряжения в материалах.

**Дочка:** О, я слышала о теории относительности! Как тензоры там помогают?

**Отец:** В теории относительности тензоры связывают геометрию пространства-времени с материей и энергией. Например, тензор Эйнштейна показывает, как масса и энергия влияют на кривизну пространства-времени.

**Дочка:** Это звучит как что-то из фильмов! А можно ли тензоры как-то визуализировать?

**Отец:** Визуализировать тензоры бывает непросто, но можно представить их как многомерные фигуры. Например, матрицу можно представить как таблицу, а более сложные тензоры — как кубы или гиперкубы.

**Дочка:** Пап, а в каких ещё областях могут быть тензоры?

**Отец:** Они также используются в континуум механике для описания напряжений в материалах и в электродинамике для объединения электрических и магнитных полей. Тензоры действительно универсальны!

**Дочка:** Спасибо, пап! Теперь я понимаю, почему тензоры такие важные! Буду дальше изучать их.
"""

# Вика и артём
def text_to_ssml(text:str):
    daughter_name = 'vika'
    father_name = 'artem'
    replacements = {'**Дочка:**': f"<break time='400ms'/> </voice> <voice name = '{daughter_name}'>",
                    '**Отец:**': f"<break time='400ms'/> </voice> <voice name = '{father_name}'>",
                    '!':','}  
    pattern = re.compile('|'.join(map(re.escape, replacements.keys())))
    result = f"<speak> <voice name = '{father_name}'>"
    result += pattern.sub(lambda match: replacements[match.group(0)], text)
    result += '</voice> </speak>'
    return result

def build_request(text=None):
    return tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(ssml=text_to_ssml(text)),
            audio_config=tts_pb2.AudioConfig(
                audio_encoding=tts_pb2.LINEAR16,
                sample_rate_hertz=sample_rate,))

stub = tts_pb2_grpc.TextToSpeechStub(grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()))
metadata = [("authorization", f"Bearer {token}")]
request = build_request(text)
responses = stub.StreamingSynthesize(request, metadata=metadata)

with wave.open("synthesized.wav", "wb") as f:
    f.setframerate(sample_rate)
    f.setnchannels(1)
    f.setsampwidth(2)
    for response in responses:
      f.writeframes(response.audio_chunk)