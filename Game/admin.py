# -*- coding: utf-8 -*-

from django.contrib import admin
from Game.models import *


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'previous_puzzle', 'solve_times')
    readonly_fields = ('link_uuid', 'qr_code', 'qr_code_host_n_port')

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/puzzle_config.js'
        )


class FeedAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_time')
    readonly_fields = ('email', 'content', 'date_time')


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Feed, FeedAdmin)

admin.site.site_header = 'Sunday'
admin.site.index_title = '星期日 - 解谜游戏管理页面'
