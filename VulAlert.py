#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup
import time

class VulAlert(object):
    # send_msg
    def send_msg(self,message):
        url = 'https://oapi.dingtalk.com/robot/send?access_token={your dingtalk access_token}'
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.message = message
        data = {
            "msgtype": "text",
            "text": {
                "content": self.message
            }
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r.text

    # 获取漏洞链接
    def vlu_link(self):
        # 获取内容
        url = "https://help.aliyun.com/noticelist/9213612.html"
        headers = {'Content-Type': 'application/json;charset=utf-8',
                   'user_agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        req = requests.get(url=url, headers=headers)
        res = BeautifulSoup(req.text, "html.parser")

        # 当前时间
        time_today = time.strftime("%Y-%m-%d", time.localtime())
        # time_today = '2021-07-22'
        # 正则漏洞标题、时间、链接
        re_link = re.findall(r'<a href="(.*?)" >【漏洞通告】', req.text)
        re_time = re.findall(r'<span class="y-right">(.*?)<span class="time">', req.text)
        # re_vlu = re.findall(r'html" >(.*?)</a>', req.text)

        # 获取当日漏洞链接
        url_list = []
        for i in range(15):
            if time_today == re_time[i]:
                vlu_link = "https://help.aliyun.com/" + re_link[i]
                url_list.append(vlu_link)

        return url_list

    # 漏洞详情
    def vlu_detail(self):
        headers = {'Content-Type': 'application/json;charset=utf-8',
                   'user_agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        url_list = self.vlu_link()
        vlu_list = []
        for url in url_list:
            req = requests.get(url=url)
            res = BeautifulSoup(req.text, "html.parser")
            # 漏洞标题
            vlu_name = res.h3.get_text()
            # 漏洞描述
            vlu_describe = res.find_all("div", id="se-knowledge")[0].p.get_text()

            vlu_list.append(vlu_name + "\n" + vlu_describe + "\n" + "漏洞详情：" + str(url) + "\n")

        return vlu_list


if __name__ == '__main__':
    for msg in VulAlert().vlu_detail():
        VulAlert().send_msg(msg)
