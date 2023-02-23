# pipenv install openai

import openai
import os
# import pickle
import time

f = open(os.path.join("secrets","OPENAI_KEY"), "r")
OPENAI_KEY = f.read()
f.close()

openai.api_key = OPENAI_KEY

def gpt3(input_str,req_jp=False):
    prompt = "「{}」をツイート文っぽく変換して。".format(input_str)
    if req_jp:
        prompt+="日本語で"
    try:
        # 以下、課金要素
        start = time.time()
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            # max_tokens=256,
            max_tokens=128,
            temperature=1.0, #0.0~2.0
            timeout=10
        )
        finish_time = time.time() - start
        # 以上、課金要素
    except Exception as e:
        print(e)
        return None

    res_text = res.choices[0].text

    # 前後の余計な空文字の削除
    res_text = res_text.strip()

    # 文がかぎ括弧で囲まれる問題の修正
    delete_target_list = [("「","」"),("\"","\"")]
    for tup in delete_target_list:
        if res_text[0] == tup[0] and res_text[-1] == tup[1]:
            res_text = res_text[1:-1]
    
    return [res_text, finish_time] # [GPTの答え, 実行時間]