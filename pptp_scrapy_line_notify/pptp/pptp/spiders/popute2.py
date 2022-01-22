# -*- coding: utf-8 -*-

import json
import os
import re

import boto3

import scrapy
from scrapy.conf import settings

from pptp.items import PptpItem

class Popute2Spider(scrapy.Spider):
    name = "popute2"
    allowed_domains = ["mangalifewin.takeshobo.co.jp/rensai/popute2/"]
    start_urls = ['http://mangalifewin.takeshobo.co.jp/rensai/popute2/']

    def parse(self, response):
        # 1st.Crawl -> 2nd.update dynamodb

        # Crawl
        month_day = '' #X-Y話の一時格納用の変数
        lastMonth = 0 #取得したエピソードのうち、最新X-Y話の X を格納
        lastDay = 0 #取得したエピソードのうち、最新X-Y話の Y を格納
        for sel in response.css("div.bookR"):
            for td in sel.css("td"):
                pptp = PptpItem()
                pptp['title'] = td.css("a::attr('title')").extract_first()
                pptp['url'] = td.css("a::attr('href')").extract_first()
                # print ('pptp["title"] -> ' + pptp["title"]) #visualize code
                match = re.search(r'\d+-\d+',pptp['title'])
                if match != None:
                    month_day = match.group().split("-")
                    # print("month_day -> " + str(month_day)) # visualize vode
                    if (int(month_day[0]) >= lastMonth) & (int(month_day[1]) >= lastDay):
                        lastMonth = int(month_day[0])
                        lastDay = int(month_day[1])
                        serial = int(re.search(r'/(\d+)/$',pptp['url']).group(1))
                yield pptp # 取得したエピソードを全て格納するが、後工程では最新話以外は未使用

        # Update dynamoDB
        client = boto3.client('dynamodb', region_name=settings['AWS_DYNAMODB_REGION'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'])

        # print ("Last Month -> " + str(lastMonth) + ", Last Day -> " + str(lastDay))
        # print ("serial ->" + str(serial))
        scan = client.scan(TableName='pptp')
        if (lastMonth >= int(scan['Items'][0]['month']['N'])) & (lastDay > int(scan['Items'][0]['day']['N'])):
            # dynamodbには最新のエピソード1レコードだけを格納する。
            res = client.put_item(
                TableName='pptp',
                Item={
                    'serial':{'N':str(serial)},
                    'month':{'N':str(lastMonth)},
                    'day':{'N':str(lastDay)}
                }
            )
            # print ("put item finished! res -> ")
            # print (res)
        pass
