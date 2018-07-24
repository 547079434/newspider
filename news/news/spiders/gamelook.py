# -*- coding: utf-8 -*-
from backstage.models import News,Keys
import scrapy
import urllib
import datetime

class SinaNewsSpider(scrapy.Spider):
    name = "gamelook"
    allowed_domains = ["gamelook.com.cn"]

    def start_requests(self):
        keys = Keys.objects.all()
        for key in keys:
            key_str = urllib.quote(key.name.encode('utf8'))
            url = 'http://www.gamelook.com.cn/?s=%s' % (key_str)
            yield scrapy.FormRequest(url=url, callback=self.parse, meta={'key':key})

    def parse(self, response):
        for li in response.xpath('//*[@id="wrap"]/div/div/div/ul/li'):
            publish_at = li.xpath('div[2]/div[2]/span/text()').extract_first()
            publish_at = datetime.datetime.strptime(publish_at, "%Y-%m-%d")
            url = li.xpath('div[2]/h2/a/@href').extract_first()
            title = li.xpath('div[2]/h2/a/text()').extract_first().strip()
            days = (datetime.datetime.now() - publish_at).days
            if response.meta['key'].name in title and days < 1:
                if not News.objects.filter(url=url).count():
                    News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'gamelook搜索',publish_at=publish_at)
