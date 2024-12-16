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
    message = event.message.text
    if re.match('推薦餐廳',message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://github.com/AndyMa0612/linebot1/raw/main/%E5%90%84%E5%BC%8F%E6%96%99%E7%90%86.png',
            alt_text='組圖訊息',
            base_size=BaseSize(height=2000, width=2000),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.popdaily.com.tw/search/%23%E6%97%A5%E5%BC%8F%E6%96%99%E7%90%86?filter=ALL&sort=RELEVANT',
                    area=ImagemapArea(
                        x=0, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.popdaily.com.tw/search/%23%E8%A5%BF%E5%BC%8F%E6%96%99%E7%90%86?filter=ALL&sort=RELEVANT',
                    area=ImagemapArea(
                        x=1000, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.popdaily.com.tw/search/%23%E4%B8%AD%E5%BC%8F%E6%96%99%E7%90%86?filter=ALL&sort=RELEVANT',
                    area=ImagemapArea(
                        x=0, y=1000, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.popdaily.com.tw/search/%23%E6%B3%95%E5%BC%8F%E6%96%99%E7%90%86?filter=ALL&sort=RELEVANT',
                    area=ImagemapArea(
                        x=1000, y=1000, width=1000, height=1000
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
