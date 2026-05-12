from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json

    symbol = data.get("symbol")
    timeframe = data.get("timeframe")
    rsi = float(data.get("rsi"))
    price = data.get("price")

    # ===== 策略过滤 =====
    if rsi < 30:

        message = (
            f"⚠ A级机会警报\n\n"
            f"币种: {symbol}\n"
            f"周期: {timeframe}\n"
            f"RSI: {rsi}\n"
            f"价格: {price}"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            }
        )

        return "alert sent"

    return "ignored"

@app.route('/')
def home():
    return "running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
