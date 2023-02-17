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

# from GPT3 import gpt3

from lang import wakatigai
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
        3:{"Q":"なにしてるの？","A":"{}をしてるなう"}   
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
async def send_sns_url(ev,tweet_text):
    try:
        return_text="そうなんだ！ツイートしようよ！\nhttps://twitter.com/intent/tweet?text="+tweet_text
        await line_api.reply_message_async(
            ev.reply_token,
            TextMessage(text=f"{return_text}"))
    except Exception as e:
            print(e)

# イベント処理
async def handle_events(events,background_tasks):
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
                # background_tasks.add_task(GPT,ev=ev,wakati_ans=wakati_ans)
                await line_api.reply_message_async(
                    ev.reply_token,
                    TextMessage(text=f"それはなに？かんたんに答えて！"))
        except Exception as e:
            print(e)

@app.post("/messaging_api/handle_request")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    # リクエストをパースしてイベントを取得（署名の検証あり）
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""))
    print(events)
    # 🌟イベント処理をバックグラウンドタスクに渡す
    background_tasks.add_task(handle_events, events=events,background_tasks=background_tasks)
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
    