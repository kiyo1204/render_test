from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('z/CdNOsTN438HCEigh1iFH6n1xucyEDxJ1/m2iRHa6fmPRonKFb98lpKbaYK30ajLVgdz+0utGRDglr15Y/umnHiCMrvC0RJBXz61nlVeV2MIxeTCj7/DzKuc1r6j7Ws8eVDMo32O2yo0HlqLJ/lEgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d603b7411843ba37b6b4e46b867d8dd9')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()