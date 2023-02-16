from fastapi import FastAPI, Request, BackgroundTasks  # 🌟BackgroundTasksを追加
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi
import json
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)#https://github.com/line/line-bot-sdk-python
secrets = json.load(open('./secrets/secrets.json', 'r'))
# APIクライアントとパーサーをインスタンス化

#[トップ>XXX>YYY >Messaging API設定>チャンネルアクセストークン(一番下)]で取得
line_api = AioLineBotApi(channel_access_token=secrets["Line"]["Channel_access_token"])

#まずwebhokのurlを登録　[トップ>XXX>YYY >Messaging API設定]
#[トップ>XXX>YYY >Messaging API設定>応答メッセージの編集>Messaging API]で取得
parser = WebhookParser(channel_secret=secrets["Line"]["Channel_secret"])

# FastAPIの起動
app = FastAPI()

# 🌟イベント処理（新規追加）
async def handle_events(events):
    line_api.broadcast(TextSendMessage(text='ブロードキャストですHello World!'))
    for ev in events:
        try:
            await line_api.reply_message_async(
                ev.reply_token,
                TextMessage(text=f"You said: {ev.message.text}"))

        except Exception as e:
            # エラーログ書いたりする
            print(e)

@app.post("/messaging_api/handle_request")
async def handle_request(request: Request, background_tasks: BackgroundTasks):  # 🌟background_tasksを追加
    # リクエストをパースしてイベントを取得（署名の検証あり）
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""))

    # 🌟イベント処理をバックグラウンドタスクに渡す
    background_tasks.add_task(handle_events, events=events)

    # LINEサーバへHTTP応答を返す
    return "ok"