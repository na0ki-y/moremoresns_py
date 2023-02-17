# pipenv install openai

import openai
import os
# import pickle
import time

f = open(os.path.join("secrets","OPENAI_KEY"), "r")
OPENAI_KEY = f.read()
f.close()

openai.api_key = OPENAI_KEY

def gpt3(input_str):
    prompt = "「{}」をツイート文っぽく変換してください".format(input_str)

    # 以下、課金要素
    start = time.time()
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        # max_tokens=256,
        max_tokens=128,
        temperature=0.2 #0.0~2.0
    )
    finish_time = time.time() - start
    # 以上、課金要素

    
    return [res.choices[0].text.strip(), finish_time] # [GPTの答え, 実行時間]