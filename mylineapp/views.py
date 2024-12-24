from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

from datetime import datetime
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("阿母,我成功了~~!")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:

            # 若有訊息事件
            if isinstance(event, MessageEvent):

                txtmsg = event.message.text

                if txtmsg in ["你好", "Hello", "早安", "Hi"]:
                    
                    stkpkg, stkid = 1070, 17840
                    replymsg = "你好, 請問需要為你做什麼?"

                    line_bot_api.reply_message(
                    event.reply_token,
                    [StickerSendMessage(package_id = stkpkg, sticker_id=stkid),
                     TextSendMessage( text = replymsg )])

                elif txtmsg == "今天誰最帥":
                    names = ['1113212047 (曾宏仁)', '1112204048 (林宗諺)','1113211030 (黃冠森)',
                            '1113211006 (陳有信)','1110304012 (林彥庭)']
                    replymsg = "今天最帥的是:" + random.choice(names)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage( text = replymsg ))

                elif txtmsg == "今天誰最美":
                    names = ['1111211008 (呂婕瑀)','1112211014 (蘇育卉)','1109302041 (李俞廷)',
                            '1109302049 (陳禹彤)','1112211042 (潘欣慧)','1110302034 (王新霏)',
                            '1110302038 (林潁俞)','1109300092 (潘妍華)','1112224017 (郭季惠)',
                            '1109302030 (黃雅旋)','1111211010 (褚芸榕)','1112203020 (陳瑪莘)',
                            '1112200110 (蘇怡嘉)','1110210048 (苗琇雯)']

                    replymsg = "今天最美的是:" + random.choice(names)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage( text = replymsg ))

                elif txtmsg.startswith("今天誰最"):
                    names = ['1113212047 (曾宏仁)', '1112204048 (林宗諺)','1113211030 (黃冠森)',
                            '1113211006 (陳有信)','1110304012 (林彥庭)','1111211008 (呂婕瑀)','1112211014 (蘇育卉)','1109302041 (李俞廷)',
                            '1109302049 (陳禹彤)','1112211042 (潘欣慧)','1110302034 (王新霏)',
                            '1110302038 (林潁俞)','1109300092 (潘妍華)','1112224017 (郭季惠)',
                            '1109302030 (黃雅旋)','1111211010 (褚芸榕)','1112203020 (陳瑪莘)',
                            '1112200110 (蘇怡嘉)','1110210048 (苗琇雯)']

                    replymsg = "今天最" + txtmsg[4:] +"的是:"+ random.choice(names)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage( text = replymsg ))

                elif txtmsg in ["龍山寺求籤","求籤","龍山寺拜拜"]:

                    num = random.choice(range(1,101))
                    imgurl = f"https://www.lungshan.org.tw/fortune_sticks/images/{num:0>3d}.jpg"

                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=imgurl,
                        preview_image_url=imgurl))

                elif txtmsg == "淺草寺求籤":
                    num = random.choice(range(1,101))
                    imgurl1 = f"https://qiangua.temple01.com/images/qianshi/fs_akt100/{num}.jpg"
                    imgurl2 = f"https://qiangua.temple01.com/images/qianshi/fs_akt100/back/{num}.jpg" 

                    line_bot_api.reply_message(
                        event.reply_token,
                        [ImageSendMessage(original_content_url=imgurl1,
                        preview_image_url=imgurl1),
                        ImageSendMessage(original_content_url=imgurl2,
                        preview_image_url=imgurl2)])

                else:

                    replymsg = "你所傳的訊息是:\n" + txtmsg

                    # 回傳收到的文字訊息
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage( text = replymsg ))
                     
                     

        return HttpResponse()
    else:
        return HttpResponseBadRequest()