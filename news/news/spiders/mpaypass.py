
# -*- coding: utf-8 -*-
import scrapy
import time
import urllib
import datetime
from backstage.models import News, Keys



class ChinaNewsSpider(scrapy.Spider):
    name = 'mpaypass'
    allowed_domains = ['mpaypass.com.cn']

    def start_requests(self):
        keys = Keys.objects.all()
        for key in keys:
            url = 'http://www.mpaypass.com.cn/Search.asp'
            FormData = {'keywords': key.name, 'jingdu':'1'}
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata = FormData, meta={'key':key})
    
    def parse(self, response):
        for div in  response.xpath('/html/body/div[2]/div[1]/div/div')[:-1]:
            url = div.xpath('div/div[2]/div[1]/a/@href').extract_first()
            publish_at = div.xpath('div/div[2]/div[3]/text()').extract_first()[1:]
            publish_at = datetime.datetime.strptime(publish_at, "%Y-%m-%d %H:%M")
            title = div.xpath('div/div[2]/div[1]/a/@title').extract_first()
            days = (datetime.datetime.now() - publish_at).days
            if response.meta['key'].name in title and days < 1:
                if not News.objects.filter(url=url).count():
                    News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'mpaypass搜索',publish_at=publish_at)
