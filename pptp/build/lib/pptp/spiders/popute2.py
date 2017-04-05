# -*- coding: utf-8 -*-
import re
import json
import os

import scrapy
import boto3

from pptp.items import PptpItem
from scrapy.conf import settings

class Popute2Spider(scrapy.Spider):
    name = "popute2"
    allowed_domains = ["mangalifewin.takeshobo.co.jp/rensai/popute2/"]
    start_urls = ['http://mangalifewin.takeshobo.co.jp/rensai/popute2/']
    print ("this is 1st start url -> "+ start_urls[0])

    def parse(self, response):
        # 1st.Crawl -> 2nd.update dynamodb

        # Crawl
        month_day =''
        lastMonth = 0
        lastDay = 0
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
                yield pptp

        # Update dynamoDB
        client = boto3.client('dynamodb', region_name=settings['AWS_DYNAMODB_REGION'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'])

        # print ("Last Month -> " + str(lastMonth) + ", Last Day -> " + str(lastDay))
        # print ("serial ->" + str(serial))
        scan = client.scan(TableName='pptp')
        if (lastMonth >= int(scan['Items'][0]['month']['N'])) & (lastDay > int(scan['Items'][0]['day']['N'])):
            # dynamodbのorderがlatestだからできる荒技
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
