#coding:utf8
from django.db import models

class Keys(models.Model):
    name = models.CharField(u'名称',max_length=20)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'关键词配置'
        verbose_name_plural = u'关键词配置管理'

class News(models.Model):
    title = models.CharField(u'标题',max_length=200)
    keys = models.ForeignKey('Keys',verbose_name=u'关键词')
    url = models.URLField(u'链接')
    content = models.TextField(u'备注',null=True)
    publish_at = models.DateTimeField(u'发布时间')
    create_at = models.DateTimeField(u'爬取时间', auto_now_add=True)

    def link(self):
        return '<a target=_blank href="%s">%s</a>' % (self.url,self.url)
    link.allow_tags = True
    link.short_description = u'链接'
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = u'新闻管理'