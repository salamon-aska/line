
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('TOKEN')
# Channel Secret
handler = WebhookHandler('SECRET')

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
	
from bs4 import BeautifulSoup#
import requests#
def currency_crawler():
    res = requests.get('https://tw.money.yahoo.com/currency-converter')
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    #end = soup.find_all('td',class_='end')#24
    all_items = soup.find_all('tr'>'td')[310:311] #307-308 change to 310-311

    #get text
    for item in all_items:
        allCur=item.text
    #spilt the text
    spilt = allCur.splitlines()

    curList=[]
    i=2
    while(i<len(spilt)):
        curList.append(spilt[i])
        i+=8


    def getCurrency(num):
        str1=  spilt[num+1] +" "+ spilt[num+2] +" "+ spilt[num+3] +" "+ spilt[num+4] +" "+ spilt[num+5]  +" "+spilt[num+6]
        return str1

    strr=""
    num=2
    for curID in curList:
        strr = strr+curID+" : "+getCurrency(num)+"        "
        num+=8

    return strr
	
def stock_crawler(stockID):
    url = 'https://tw.stock.yahoo.com/q/q?s={}'.format(stockID)
    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'html.parser')
    table = html.findAll(text='個股資料')[0].parent.parent.parent
    dataRow = table.select('tr')[1].select('td')
    closingPrice = dataRow[7].text
    closingPrice_text=""
    closingPrice_text += str(stockID) + " 收盤價 : " + closingPrice
    return closingPrice_text
	
def weather_yahooAPI():
    #Taoyuan's woeid = 2028752467 
    res=requests.get("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%2028752467%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys")
    data=res.json()
    fdata=data["query"]["results"]["channel"]["item"]["forecast"]
    today=fdata[0]
    str_=""
    str_="最低溫 : "+today['low']+"  最高溫 : "+today['high']+"  天氣狀況 : "+today['text']
    return str_
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	text = event.message.text
	if text == 'weather' or text == '天氣':
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=weather_yahooAPI()) )
   
	elif text == 'stock' or text == 'Stock' or text == '股票':
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=stock_crawler(2330)) )
		
	elif text == 'currency' or text == 'Currency' or text == '匯率':
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=currency_crawler()) )
	elif text == '?' or text == '功能':
		line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請擇一輸入下列指令:\n\"天氣\" \"股票\" \"匯率\"") )
	
	#else:
		#texttest = "您輸入了錯誤的指令 請擇一輸入下列指令:\n\"天氣\" \"股票\" \"匯率\""
		
		#line_bot_api.reply_message(
        #event.reply_token,TextSendMessage(texttest))
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
