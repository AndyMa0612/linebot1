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
            thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',
            title='中華民國',
            text='選單功能－TemplateSendMessage',
            actions=[
                PostbackAction(
                    label='這是PostbackAction',
                    display_text='顯示文字',
                    data='實際資料'
                ),
                MessageAction(
                    label='這是MessageAction',
                    text='實際資料'
                ),
                URIAction(
                    label='這是URIAction',
                    uri='https://en.wikipedia.org/wiki/Taiwan'
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
