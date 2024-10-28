from openai import OpenAI
import synthesisAPI

def gpt_request(article_text):
    client = OpenAI(
        api_key='sk-6EZ3UEB1vKCGkfItMcjOkwr63aKi0mh8',
        base_url="https://api.proxyapi.ru/openai/v1"
    )
    index_prompt = '3'
    prompt_dir = './prompts/'

    with open(prompt_dir + index_prompt+'prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()

    MODEL="gpt-4o-mini"

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": article_text}
        ],
        max_tokens=len(article_text) // 3
    )

    with open(prompt_dir + index_prompt + 'prompt_for_voice.txt', 'r', encoding='utf-8') as file:
        prompt_for_voice = file.read()
    responce = completion.choices[0].message.content
    completion_for_voice = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_for_voice},
            {"role": "user", "content": responce}
        ]
    )

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIxUGNSUGsvMVo3WG9QSGxIS3d2cmdWUkxnQ1ZFTnByRHZPK1ArODM2NHM9VFRTX1RFQU0ifQ.eyJpc3MiOiJ0ZXN0X2lzc3VlciIsInN1YiI6InRlc3RfdXNlciIsImF1ZCI6InRpbmtvZmYuY2xvdWQudHRzIiwiZXhwIjoxNzMwMDM0Nzg0LjB9.MdFFTzRSEcpo1KDHcrKEadpyifKyqZBTW_-Bs6_YQX8'
    synthesisAPI.synthesis(completion_for_voice.choices[0].message.content, token)

    return completion.choices[0].message.content