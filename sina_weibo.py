#encoding:utf-8
#author:simple
import requests
import random
import re
import time
from datetime import datetime,timedelta
import json


# print(datetime.now().strftime("%m-%d"))
dd = datetime.now()
# print((d - timedelta(days=30)).strftime("%m-%d"))
expire_time = (dd - timedelta(days=30)).strftime("%m-%d")
cookie = {'cookie': 'your cookie'}
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

with open('sina_weibo.csv', 'a+', encoding='utf-8') as f:
    for j in range(1, 10000):
        url = 'https://m.weibo.cn/api/container/getIndex?uid=2183473425&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E8%81%94%E6%83%B3%E4%B8%AD%E5%9B%BD&containerid=1076032183473425&page={0}'.format(j)
        res = requests.get(url, headers=headers, cookies=cookie)
        # print(res)
        cards = json.loads(res.text)["data"]["cards"]
        print("正在抓取第{0}信息".format(j))
        try:
            for i in cards:
                d = {}
                # print(i["mblog"].get("text", 0))
                if i.get('mblog', 0) != 0:
                    # 获取评论详情的id
                    d['id'] = i['mblog']["id"]
                    # 创建时间
                    d['created_at'] = i['mblog']['created_at']
                    if d['created_at'] == expire_time:
                        break
                    # 微博来源
                    d['source'] = i['mblog']['source']
                    if i['mblog']['source'] == "微博视频":
                        d['obj_ext'] = i['mblog']['obj_ext']
                    else:
                        d['obj_ext'] = "None"
                    # 获取微博文本
                    html = re.findall("<.*?>", i['mblog']['text'], re.S)
                    d['text'] = i['mblog']['text']
                    html = set(html)
                    for h in html:
                        d['text'] = d['text'].replace(h, '')
                        # print(d['text'])
                    # 转发数
                    d['reposts_count'] = i['mblog']['reposts_count']
                    # 评论数
                    d['comments_count'] = i['mblog']['comments_count']
                    # 点赞数
                    d['attitudes_count'] = i['mblog']['attitudes_count']
                    # print(d)
                    s = json.dumps(d, ensure_ascii=False)
                    # print(s)
                    f.write(s+'\n')
        except Exception as e:
            print(e)
        time.sleep(random.randint(3, 6))

