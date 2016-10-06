# -*- coding: utf-8 -*-

from django.contrib import admin
from Game.models import *


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'previous_puzzle', 'solve_times')
    readonly_fields = ('solve_times', 'link_uuid', 'qr_code', 'qr_code_host_n_port')


admin.site.register(Puzzle, PuzzleAdmin)

admin.site.site_header = 'Sunday'
admin.site.index_title = '星期日 - 解谜游戏管理页面'
