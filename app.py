from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def call_phone(msg):
    url = "https://api.callmebot.com/telegram/call.php"
    requests.get(url, params={
        "user": "@你的Telegram用户名",
        "text": msg
    })

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.data.decode()

    print("收到信号:", data)

    # 只要有信号就触发（不解析RSI）
    message = "📉 RSI触发超卖信号"

    # 1. Telegram
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    # 2. 电话
    call_phone("RSI超卖，请查看行情")

    return "ok"
