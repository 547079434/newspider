# -*- coding: utf-8 -*-
import xadmin
from xadmin.views.base import CommAdminView
from xadmin.plugins.themes import ThemePlugin
from .models import *

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
xadmin.site.register(News, NewsAdmin)
