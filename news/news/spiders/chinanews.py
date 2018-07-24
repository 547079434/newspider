# -*- coding: utf-8 -*-

import scrapy
import time
import urllib
import datetime
from backstage.models import News, Keys



class ChinaNewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['chinanews.com']
    def start_requests(self):
        keys = Keys.objects.all()
        for key in keys:
            url = 'http://sou.chinanews.com.cn/search.do'
            FormData = {'field': 'title', 'q': key.name, 'ps': '100', 'adv':'1', 'time_scope':'1', 'channel':'all', 'sort':'pubtime'}
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata = FormData, meta={'key':key})
    
    def parse(self, response):
        for table in  response.xpath('//*[@id="news_list"]/table'):
            url = table.xpath('tr[2]/td/ul/li/text()').extract()[0].split('\n')[0][:-3]
            publish_at = table.xpath('tr[2]/td/ul/li/text()').extract()[0].split('\n')[1].strip()
            publish_at = datetime.datetime.strptime(publish_at, "%Y-%m-%d %H:%M:%S")
            title = ''
            text = table.xpath('tr[1]/td[2]/ul/li[1]/a/text()').extract()
            text.insert(1, response.meta['key'].name)
            for i in text:
                title += i.strip()
            if not News.objects.filter(url=url).count():
                News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'中新网搜索',publish_at=publish_at)
                   

    



