# -*- coding: utf-8 -*-
from backstage.models import News,Keys
import scrapy
import urllib
import datetime

class SinaNewsSpider(scrapy.Spider):
    name = "sinanews"
    allowed_domains = ["search.sina.com.cn"]
    start_urls = ['http://search.sina.com.cn/']

    def parse(self, response):
        keys =  Keys.objects.all()
        for key in keys:
            key_str = urllib.quote(key.name.encode('cp936'))
            url = 'http://search.sina.com.cn/?q=%s&range=title&c=news&sort=time' % (key_str)
            yield scrapy.Request(url, callback=self.parse_item,meta={'key':key})

    def parse_item(self, response):
        content = response.xpath('//*[@id="result"]//div[@class="box-result clearfix"]/div')   
        for c in content:
            url = c.xpath('h2/a/@href').extract_first()
            if url:
                title = c.xpath('h2/a').xpath('string(.)').extract_first()
                text = c.xpath('h2/span[@class="fgray_time"]/text()').extract_first().split(' ')
                publish_at = text[1]+' '+text[2]
                if not News.objects.filter(url=url).count():
                    News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'新浪新闻搜索',publish_at=publish_at)
