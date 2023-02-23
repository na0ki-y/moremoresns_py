from fastapi import FastAPI, Request, BackgroundTasks  
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='templates')
##
from linebot import WebhookParser
from linebot.models import TextMessage
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)#https://github.com/line/line-bot-sdk-python
from aiolinebot import AioLineBotApi
##
import json
import random
import os 

from GPT3 import gpt3
import urllib.parse

from lang import wakatigai
from img2text import init_img2text
from img2text import predict_step
secrets = json.load(open('./secrets/secrets.json', 'r'))
# APIクライアントとパーサーをインスタンス化

#[トップ>XXX>YYY >Messaging API設定>チャンネルアクセストークン(一番下)]で取得
line_api = AioLineBotApi(channel_access_token=secrets["Line"]["Channel_access_token"])

#まずwebhokのurlを登録　[トップ>XXX>YYY >Messaging API設定]
#[トップ>XXX>YYY >Messaging API設定>応答メッセージの編集>Messaging API]で取得
parser = WebhookParser(channel_secret=secrets["Line"]["Channel_secret"])


user_q_id={"XXXX":-1}#UserID:quessionID #誰にどの質問をしているか
questions={
        1:{"Q":"今日は何食べたの？","A":"{}をたべた"},
        2:{"Q":"いまどこにいるの？","A":"{}にいる"},
        3:{"Q":"なにしてるの？","A":"{}をしてるなう"},
        4:{
            "Q":"最近周りではどのようなことが流行っていますか?",
            "A":"{}が流行り中です!"
        },
        5:{
            "Q":"最近チームでどんな活動をしましたか?",
            "A":"この前, {}をやってみました!"
        },
        6:{
            "Q":"これから何か予定していることはありますか?",
            "A":"これから{}を行う予定です"
        },
        7:{
            "Q":"最近何か制作しているものはありますか?",
            "A":"最近{}を作っています"
        },
        8:{
            "Q":"最近勉強していることはなんですか?",
            "A":"{}を勉強中です"
        },
        9:{
            "Q":"どんな人とコラボレーションしてみたいですか?",
            "A":"{}と一緒になにかしたいです"
        },
        10:{
            "Q":"最近何かイベントに参加しましたか?",
            "A":"{}のイベントに参加しました"
        },
        11:{"Q":"最近何かあった？","A":"{}があったよ"}   
        }
# FastAPIの起動
app = FastAPI()
# イベント処理
async def handle_broadcast(num):
    try:
        if not num in questions.keys():
            num=random.choice(list(questions.keys()))
        for u in user_q_id.keys():
            user_q_id[u]=num
        line_api.broadcast(TextSendMessage(text="いきなり質問！\n"+questions[num]["Q"]))
    except Exception as e:
            print(e)
# イベント処理
async def send_question(num,ev):
    try:
        if not num in questions.keys():
            num=random.choice(list(questions.keys()))
        user_q_id[ev.source.user_id]=num
        print(user_q_id)
        await line_api.reply_message_async(
                        ev.reply_token,
                        TextMessage(text=questions[num]["Q"]))
    except Exception as e:
            print(e)
# イベント処理
async def send_sns_url(ev,tweet_text,return_text="そうなんだ！ツイートしようよ！"):
    try:
        print(type(tweet_text))
        print(tweet_text)
        return_text=return_text+"\nhttps://twitter.com/intent/tweet?text="+urllib.parse.quote(tweet_text)
        await line_api.reply_message_async(
            ev.reply_token,
            TextMessage(text=f"{return_text}"))
    except Exception as e:
            print(e)

# イベント処理
async def handle_events_text(events,background_tasks):
    '''
    LINEのメッセージ(テキスト)を処理する
    形態素解析してそれぞれのバックグラウンド処理へ
    '''
    for ev in events:
        try:
            wakati_ans=wakatigai(ev.message.text)
            if wakati_ans["flag_toukou"]:
                background_tasks.add_task(send_question,num=-1,ev=ev)
            elif len(wakati_ans["noun_count"])==1:
                # return_text="そうなんだ！ツイートしようよ！\n https://twitter.com/intent/tweet?text="+wakati_ans["noun_count"][0][0]+"を食べたよ"
                # await line_api.reply_message_async(
                #     ev.reply_token,
                #     TextMessage(text=f"{return_text}"))
                tweet_text = questions[user_q_id[ev.source.user_id]]["A"].format(wakati_ans["noun_count"][0][0])
                background_tasks.add_task(send_sns_url,ev=ev,tweet_text=tweet_text)
            else:
                # background_tasks.add_task(gpt3,num=-1)
                res = gpt3(ev.message.text)

                # gptの生成に時間がかかった場合
                if res == None:
                    await line_api.reply_message_async(
                    ev.reply_token,
                    TextMessage(text=f"それはなに？かんたんに答えて！"))
                else:
                    background_tasks.add_task(send_sns_url,ev=ev,tweet_text=res[0])
                
                

        except Exception as e:
            print(e)
# イベント処理
img_cnt=0
async def handle_events_img(events,background_tasks):
    '''
    LINEのメッセージ(画像)を処理する
    '''
    global img_cnt
    for ev in events:
        try:
            img_path="./tmp/img{}.png".format(img_cnt)
            #####画像の取得
            message_content = line_api.get_message_content(ev.message.id)
            with open(img_path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            #####ツイート文を生成
            pass
            #####メッセージを返す
            background_tasks.add_task(send_sns_url,ev=ev,tweet_text="いい写真を撮ったよ",return_text="いい写真だね！ツイートしようよ!")
            #####画像の取得
            #os.remove(img_path)
            img_cnt+=1
        except Exception as e:
            print(e)

@app.post("/messaging_api/handle_request")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    '''
    LINEのメッセージを受け取る
    内容を確認してバックグラウンドタスクへ
    '''
    # リクエストをパースしてイベントを取得（署名の検証あり）
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""))
    print(events)
    # イベント処理をバックグラウンドタスクに渡す
    if events[0].message.type=="text":
        background_tasks.add_task(handle_events_text, events=events,background_tasks=background_tasks)
    elif events[0].message.type=="image":
        background_tasks.add_task(handle_events_img, events=events,background_tasks=background_tasks)
        print("img")
    else:
        print(events[0].message.type,"no support")
    # LINEサーバへHTTP応答を返す
    return "ok"

# @app.get("/maintain/{id}", response_class=HTMLResponse)
# async def get_maintain(id: str, request: Request):
#     return templates.TemplateResponse(
#         "maintain.html",
#         {
#             "request": request,
#             "id": id
#         }
#     )
    
@app.post("/broadcast")
async def create_users(background_tasks: BackgroundTasks):
    background_tasks.add_task(handle_broadcast,num=-1)
    