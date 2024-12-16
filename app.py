# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('GHY2NQzOGaVPecTUi1IjgFAlsZaZ1uWE0z8VzPQwpQcHuoZ260TfDg6zMuu+CZSi38i3OEKUEVmPbKkA7d2qrSstvGVxxOvJXel+l6LdC8LbCy9HuvfcnX+fyupnmW3v0IOIpqmmK5mYH1HCn75tbAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2d76a3d9752771ac55a74d90e1ff6e2e')

line_bot_api.push_message('U0b6441bd0ff804fe3f87793461cf615f', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('推薦景點',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這是樣板傳送訊息',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/0IKFpMG.jpeg',
            title='台中望高寮',
            text='選單功能－TemplateSendMessage',
            actions=[
                PostbackAction(
                    label='想了解資訊',
                    display_text='我想了解',
                    data='臺中市南屯區中台路'
                ),
                MessageAction(
                    label='想知道那邊可以幹嘛',
                    text='為觀看夕陽西下、夜景的好去處，附近的人常將望高寮稱為「東海古堡」。'
                ),
                URIAction(
                    label='地圖位置',
                    uri='https://www.google.com/maps?s=web&lqi=CgnmnJvpq5jlr65I5Iblk82CgIAIWhkQABABEAIYABgBGAIiC-acmyDpq5gg5a-ukgESdG91cmlzdF9hdHRyYWN0aW9umgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVF5TW5OeFVqUlJSUkFCqgFEEAEqDyIL5pybIOmrmCDlr64oRTIeEAEiGiVDROdMvSvBqWNkmDIgcjpyFgL6TMDUhobaMg8QAiIL5pybIOmrmCDlr676AQQIABAZ&vet=12ahUKEwjv0a6Az6yKAxVZgq8BHZOnCeYQ1YkKegQIIBAB..i&cs=0&um=1&ie=UTF-8&fb=1&gl=tw&sa=X&geocode=KRFoFrP3Pmk0MU45sK7I91Ji&daddr=408%E5%8F%B0%E4%B8%AD%E5%B8%82%E5%8D%97%E5%B1%AF%E5%8D%80%E4%B8%AD%E5%8F%B0%E8%B7%AF601%E8%99%9F'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
