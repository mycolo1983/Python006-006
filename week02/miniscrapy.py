import requests
from lxml import etree
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
r = requests.get('https://www.zhihu.com/question/29978072',headers=headers)
s = etree.HTML(r.text)
# 获取问题内容
q_content = s.xpath('//*[@class="QuestionHeader-title"]/text()')[0]
# 获取问题描述
q_describe = s.xpath('//*[@class="RichText ztext"]/text()')[0]
# 获取关注数和浏览量，这两个属性一样
q_number = s.xpath('//*[@class="NumberBoard-itemValue"]/text()')
concern_num = q_number[0]
browing_num = q_number[1]
# 打印
print('问题:',q_content,'\n','描述:',q_describe,'\n','关注数:',concern_num,'\n','浏览量:',browing_num)


#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote
import requests
from fake_useragent import UserAgent
from xml import etree
question = '有什么适合中学生使用的学习软件？'
id = 29978072
referer = 'https://www.zhihu.com/search?type=content&q=' + quote(question)
headers = {
    # 'referer': referer,
    'user-agent': UserAgent(verify_ssl=False).random
}


def spider(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    all = res.json()
    print(all)
    totals = all['paging']['totals']
    print(f'一共有{totals}回答')
    data = all['data']
    con_list = []
    for i in data:
        tmp = i['content']
        con_list.append(tmp)
    next_url = all['paging']['next']
    return con_list, totals, next_url


if __name__ == '__main__':
    fp = open('./spider.txt', mode='a+', encoding='utf-8')
    i = 0
    url = f'https://www.zhihu.com/api/v4/questions/{id}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit=3&offset=0&platform=desktop&sort_by=default'
    while i <= 15:
        con_list, totals, url = spider(url=url)
        fp.write('\r\n'.join(con_list))
        i += 1
    fp.close()
