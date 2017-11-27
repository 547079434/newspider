# -*- coding: utf-8 -*-
from backstage.models import News,Keys
import scrapy
import urllib
import datetime

class BaiduNewsSpider(scrapy.Spider):
    name = "baidunews"
    allowed_domains = ["news.baidu.com"]
    start_urls = ['http://news.baidu.com/']

    def parse(self, response):
        keys =  Keys.objects.all()
        for key in keys:
            key_str = urllib.quote(key.name.encode('utf8'))
            url = 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=%s&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=newstitle&word=%s' % (key_str,key_str)
            yield scrapy.Request(url, callback=self.parse_item,meta={'key':key})

    def parse_item(self, response):
        content = response.xpath('//*[@id="content_left"]/div[2]//div[@class="result title"]')   
        for c in content:
            url = c.xpath('h3/a/@href').extract_first()
            title = c.xpath('h3/a').xpath('string(.)').extract_first()
            text = c.xpath('div[@class="c-title-author"]/text()').extract_first()
            time_str = text.split(u'\xa0')[2]
            if u'分钟前' in time_str:
                minute = int(time_str.split(u'分钟前')[0])
                publish_at = datetime.datetime.now() - datetime.timedelta(minutes=minute)
            elif u'小时前' in time_str:
                hours = int(time_str.split(u'小时前')[0])
                publish_at = datetime.datetime.now() - datetime.timedelta(hours=hours)
            else:
                publish_at = time_str.replace(u'年','-').replace(u'月','-').replace(u'日','')

            if not News.objects.filter(url=url).count():
                News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'百度新闻搜索',publish_at=publish_at)
