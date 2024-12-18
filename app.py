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
line_bot_api = LineBotApi('uqn8F5AIftKxhnBJq+76T3YazN5AWYR+VxJrd68V6scH0EXgWzUzKiGMmGNXBn5u38i3OEKUEVmPbKkA7d2qrSstvGVxxOvJXel+l6LdC8KcxrlK1fuiS3C0iZu0CCV5ILLU1v50mud6jUaHkCOqSQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2dfd9021dc688c45c6b5cbc9bf18cabc')

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
    if re.match('電影推薦',message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='這是TemplateSendMessage',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/jR5ClEy.png',
                        action=PostbackAction(
                            label='獅子王：木法沙',
                            display_text='http://app2.atmovies.com.tw/poster/fmen13186482/',
                            data='action=001'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4zQ528x.png',
                        action=PostbackAction(
                            label='白雪公主',
                            display_text='http://www.atmovies.com.tw/movie/fsen46208148/',
                            data='action=002'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/rnBycmI.png',
                        action=PostbackAction(
                            label='麥塊電影',
                            display_text='http://www.atmovies.com.tw/movie/faen83566834/',
                            data='action=003'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/1tTl3ab.png',
                        action=PostbackAction(
                            label='玩具總動員5',
                            display_text='http://www.atmovies.com.tw/movie/ften29355505/',
                            data='action=004'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
