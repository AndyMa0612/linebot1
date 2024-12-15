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
line_bot_api = LineBotApi('JMCPBQudpqEoC4PYuKzq5n5keshLPWyw1xVDWNL3w31JlRYHb6YxTAd7fhQaDqfZ38i3OEKUEVmPbKkA7d2qrSstvGVxxOvJXel+l6LdC8JXZKzZnzyj3Rdz5h5973ZozJxk84DoVHfeN2op+ONCCAdB04t89/1O/w1cDnyilFU=')
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
    if re.match('音樂片',message):
        video_message = VideoSendMessage(
            original_content_url='https://raw.githubusercontent.com/AndyMa0612/linebot1/main/Endless%20Tears%20feat.%20%E4%B8%AD%E6%9D%91%E8%88%9E%E5%AD%90%20-%20Love%20is%20a%20beautiful%20pain%E5%96%9C%E6%AD%A1%E4%BD%A0%E7%9C%9F%E7%9A%84%E5%A5%BD%E7%97%9B%E8%8B%A6%E4%B8%AD%E6%97%A5%E5%8B%95%E6%85%8B%E6%AD%8C%E8%A9%9ELyrics.mp4
',
            preview_image_url='https://raw.githubusercontent.com/AndyMa0612/linebot1/main/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202024-12-15%20114636.png
'
        )
        line_bot_api.reply_message(event.reply_token, video_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，沒有這類型的影片"))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
