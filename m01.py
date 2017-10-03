# -*- coding: utf-8 -*-
import requests
import json
import datetime
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import TextSendMessage
import config

# reload (sys)
# sys.setdefaultencoding ('utf-8')

BOT_ACCESS_TOKEN = config.BOT_ACCESS_TOKEN
BOT_OWNER_ID = config.BOT_OWNER_ID
BOT_SECRET = config.BOT_SECRET

line_bot_api = LineBotApi(BOT_ACCESS_TOKEN)
handler = WebhookHandler(BOT_SECRET)


def get_mobile01_posts():

    m01_url = "https://www.mobile01.com/"
    url = "https://www.mobile01.com/hottopics.php?id=5"
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    flist = soup.findAll("td", { "class" : "subject" })

    keywords = ["開箱", "入手"]

    def notification(title, link):
        with open('data/notify_list.json', 'r') as file:
            notify_list = json.load(file)
        if len(notify_list) == 0:
            return False
        content = "{}\n{}".format(title, link)
        line_bot_api.multicast(notify_list, TextSendMessage(text=content))
        print("Done.")
        return True

    match = []
    for post in flist:
        title = post.select('a')[0].text
        for keyword in keywords:
            if keyword in title:
                link = m01_url + post.select('a')[0]['href']
                post_id = link[link.index("&t=") + 3:]
                match.append({'title':title, 'link':link, 'id':post_id})

    with open('data/history_post.json', 'r+') as file:
        history = json.load(file)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
        new_flag = False
        print(history)
        for post in match:
            if post['id'] in history:
                break
            new_flag = True
            history.append(post['id'])
            notification(post['title'], post['link'])

        if new_flag == True:
            file.seek(0)
            file.truncate()
            file.write(json.dumps(history))
        else:
            print("{}: Nothing".format(now))


get_mobile01_posts()