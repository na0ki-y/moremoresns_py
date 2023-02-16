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

from lang import wakatigai_return_meisi
secrets = json.load(open('./secrets/secrets.json', 'r'))
# APIクライアントとパーサーをインスタンス化

#[トップ>XXX>YYY >Messaging API設定>チャンネルアクセストークン(一番下)]で取得
line_api = AioLineBotApi(channel_access_token=secrets["Line"]["Channel_access_token"])

#まずwebhokのurlを登録　[トップ>XXX>YYY >Messaging API設定]
#[トップ>XXX>YYY >Messaging API設定>応答メッセージの編集>Messaging API]で取得
parser = WebhookParser(channel_secret=secrets["Line"]["Channel_secret"])

# FastAPIの起動
app = FastAPI()
# イベント処理
async def handle_broadcast(num):
    try:
        line_api.broadcast(TextSendMessage(text='今日は何食べたの？'))
    except Exception as e:
            print(e)

# イベント処理
async def handle_events(events):
    for ev in events:
        try:
            meisi=wakatigai_return_meisi(ev.message.text)
            if len(meisi)==1:
                return_text="そうなんだ！ツイートしようよ！\n https://twitter.com/intent/tweet?text="+meisi[0][0]+"を食べたよ"
                await line_api.reply_message_async(
                    ev.reply_token,
                    TextMessage(text=f"{return_text}"))
            else:
                return_text="https://twitter.com/intent/tweet?text="+meisi[0][0]+"を食べたよ"
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
    # 🌟イベント処理をバックグラウンドタスクに渡す
    print(events)
    background_tasks.add_task(handle_events, events=events)
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
    