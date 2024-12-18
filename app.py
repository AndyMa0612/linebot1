# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
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

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('uqn8F5AIftKxhnBJq+76T3YazN5AWYR+VxJrd68V6scH0EXgWzUzKiGMmGNXBn5u38i3OEKUEVmPbKkA7d2qrSstvGVxxOvJXel+l6LdC8KcxrlK1fuiS3C0iZu0CCV5ILLU1v50mud6jUaHkCOqSQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的 Channel Secret
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

# 訊息傳遞區塊
##### 基本上程式編輯都在這個 function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('查看菜單', message):
        # Flex Message for the menu
        flex_message = FlexSendMessage(
            alt_text='餐廳推薦菜單',
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/eP1v8W9.jpg",  # Replace with actual image URL
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "大牛排", "weight": "bold", "size": "xl"},
                                {"type": "text", "text": "多汁美味的頂級牛排，煎至完美熟度。", "wrap": True, "color": "#666666", "size": "sm"},
                                {"type": "text", "text": "NT$ 880", "weight": "bold", "size": "lg", "color": "#FF0000"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "您已成功將【大牛排】加入購物車"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/4zO6C2n.jpg",  # Replace with actual image URL
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "海鮮義大利麵", "weight": "bold", "size": "xl"},
                                {"type": "text", "text": "新鮮海鮮搭配濃郁醬汁，風味絕佳。", "wrap": True, "color": "#666666", "size": "sm"},
                                {"type": "text", "text": "NT$ 520", "weight": "bold", "size": "lg", "color": "#FF0000"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "您已成功將【海鮮義大利麵】加入購物車"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/VmWhEFD.jpg",  # Replace with actual image URL
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "抹茶蛋糕", "weight": "bold", "size": "xl"},
                                {"type": "text", "text": "香濃抹茶風味，搭配綿密蛋糕體。", "wrap": True, "color": "#666666", "size": "sm"},
                                {"type": "text", "text": "NT$ 250", "weight": "bold", "size": "lg", "color": "#FF0000"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "您已成功將【抹茶蛋糕】加入購物車"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
