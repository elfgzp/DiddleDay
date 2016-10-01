# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Puzzle(models.Model):
    content = models.TextField(blank=True, null=False, db_column='content', verbose_name='内容')
    answer = models.TextField(blank=True, null=False, db_column='answer', verbose_name='答案')
    qr_code = models.ImageField()
