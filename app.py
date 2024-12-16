import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage

# LINE Bot 設定
LINE_ACCESS_TOKEN = "IwKLag3CEKNJmRD6fsALE00TihFGzIhjngMa8blDi4ftHaWKeECZ+G7NI/iAHFvWJQC8fmkdWVait1xSE4KHRAGthUvPKC/kX4QnPM0KScuCd+dZnvJFgQnTEuZgjATeziF6/VZJyOcj+WjmkLwWIQdB04t89/1O/w1cDnyilFU="
USER_ID = "U251508da6b8209d394d4cb9fc359673a"
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

# 爬蟲 URL
url = "https://wol.gg/stats/tw/%E5%8F%AF%E5%8F%A3%E9%9B%9E%E8%82%89%E9%A3%AF-tw2/"

pre_game = None
tz = pytz.timezone('Asia/Taipei')

def send_line_message(message):
    try:
        line_bot_api.push_message(USER_ID, TextSendMessage(text=message))
    except Exception as e:
        print(f"LINE 訊息發送失敗: {e}")

while True:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        result = soup.find(id="level")

        cur_game = None

        if result is not None:
            cur_game = result.text.strip()
            cur_game = cur_game.split("on ")[1]
            cur_game = datetime.strptime(cur_game, "%d %b %Y")
            cur_game = cur_game.strftime("%Y/%m/%d")
        else:
            print("未找到 id='level' 的元素")

        cur_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")

        if pre_game is None:
            pre_game = cur_game
            start_message = f"開始...時間為 : {cur_time}"
            print(start_message)
            send_line_message(start_message)
        elif pre_game != cur_game:
            finish_message = f"打完時間 : {cur_time}"
            print(finish_message)
            send_line_message(finish_message)
            pre_game = cur_game

        time.sleep(60)

    else:
        error_message = f"請求失敗，狀態碼: {response.status_code}"
        print(error_message)
        send_line_message(error_message)
        time.sleep(60)
