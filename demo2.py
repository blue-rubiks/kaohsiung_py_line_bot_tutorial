import configparser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])


@app.route("/test")
def hello():
    return "flask server success"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "demo":
        buttons_template = TemplateSendMessage(
            alt_text='test template',
            template=ButtonsTemplate(
                title='標題類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    URITemplateAction(
                        label='點我到 Google',
                        uri='https://www.google.com.tw/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "carousel":
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            MessageTemplateAction(
                                label='蘋果即時新聞',
                                text='蘋果即時新聞'
                            ),
                            URITemplateAction(
                                label='點我到 Google',
                                uri='https://www.google.com.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
                        title='this is menu2',
                        text='description2',
                        actions=[
                            MessageTemplateAction(
                                label='ptt熱門文章',
                                text='ptt熱門文章'
                            ),
                            URITemplateAction(
                                label='點我到 Google',
                                uri='https://www.google.com.tw/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            carousel_template_message)
        return 0

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
