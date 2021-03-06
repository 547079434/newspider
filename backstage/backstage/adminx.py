# -*- coding: utf-8 -*-
import xadmin
from xadmin.views.base import CommAdminView
from xadmin.plugins.themes import ThemePlugin
from .models import *
from backstage.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
import xlwt
import os

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class AdminSettings(object):
    menu_style = "accordion"
    site_title = '爬虫管理系统'
    site_footer = '爬虫管理系统'

    def get_site_menu(self):
        return [
            {'title': '新闻管理','icon':'fa fa-bar-chart-o', 'perm': self.get_model_perm(Keys, 'change'), 'menus':(
                {'title': '关键词配置', 'url': self.get_model_url(Keys, 'changelist'),
                'perm': self.get_model_perm(Keys, 'changelist')},
                {'title': '新闻', 'url': self.get_model_url(News, 'changelist'),
                'perm': self.get_model_perm(News, 'changelist')},
            )},
        ]

xadmin.site.register(xadmin.views.BaseAdminView,BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView,AdminSettings)

class KeysAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = []
xadmin.site.register(Keys, KeysAdmin)


class NewsAdmin(object):
    list_display = ['title','publish_at','link','keys']
    search_fields = ['title','url']
    list_filter = ['keys','publish_at']
    list_export = ['xls','xml','csv','json']
    actions = ['export_excel']

    def export_excel(self, request, queryset):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, u'标题')
        sheet.write(0, 1, u'链接')
        sheet.write(0, 2, u'发布时间')
        sheet.write(0, 3, u'关键词')
        for i,q in enumerate(queryset):
            sheet.write(i+1, 0, q.title)
            sheet.write(i+1, 1, q.url)
            sheet.write(i+1, 2, q.publish_at.strftime("%Y-%m-%d %H:%M:%S"))
            sheet.write(i+1, 3, q.keys.name)
        if not os.path.exists(MEDIA_ROOT):
            os.mkdir(MEDIA_ROOT)
        workbook.save(MEDIA_ROOT+'/news.xls')
        return HttpResponseRedirect('/media/news.xls')
    export_excel.short_description = u'导出Excel'

xadmin.site.register(News, NewsAdmin)
