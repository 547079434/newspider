# -*- coding: utf-8 -*-

from backstage.models import News, Keys
import scrapy
import urllib
import datetime


class ThepaperSpider(scrapy.Spider):
    name = 'thepaper'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/']
    def parse(self, response):
        keys = Keys.objects.all()
        for key in keys:
            key_str = urllib.quote(key.name.encode('utf8'))
            url = 'https://www.thepaper.cn/searchResult.jsp?inpsearch=%s&searchPre=contentName_0' % (key_str) + '%3A&orderType=1'
            yield scrapy.Request(url, callback=self.parse_item, meta={'key':key})

    def parse_item(self, response):
        content = response.xpath('//*[@id="mainContent"]/div')
        for c in content:
            url = 'https://www.thepaper.cn/' + c.xpath('h2/a/@href').extract_first()
            if url:
                titles = c.xpath('h2/a/text()').extract()
                titles.insert(1, response.meta['key'].name)
                title = ''
                for t in titles:
                    title += t
                time_str = c.xpath('div/span/text()')[-1].extract()
                # print '=====', time_str
                if u'分钟前' in time_str:
                    minute = int(time_str.split(u'分钟前')[0])
                    publish_at = datetime.datetime.now() - datetime.timedelta(minutes=minute)
                elif u'小时前' in time_str:
                    hours = int(time_str.split(u'小时前')[0])
                    publish_at = datetime.datetime.now() - datetime.timedelta(hours=hours)
                elif u'天前' in time_str:
                    day = int(time_str.split(u'天前')[0])
                    publish_at = datetime.datetime.now() - datetime.timedelta(days=day)
                else:
                    publish_at = ''
                if publish_at:
                    days = (datetime.datetime.now() - publish_at).days
                    if days < 1:
                        if not News.objects.filter(url=url).count():
                            News.objects.create(title=title,keys=response.meta['key'],url=url,content=u'澎湃搜索',publish_at=publish_at)
