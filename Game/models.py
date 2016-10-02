# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from django.db import models
from django.dispatch import receiver
from django.core.files import File
import uuid
from Game.qrCode import generate_qrcode
from DiddleDay.settings import HOST, QRCODE_PATH, QRCODE_LOGO_PATH


class Puzzle(models.Model):
    link_uuid = models.CharField(blank=True, null=True, max_length=100, db_index=True,
                                 db_column='link_uuid',
                                 verbose_name='唯一识别码')
    name = models.CharField(blank=True, null=True, max_length=100, db_column='name', verbose_name='谜题')
    content = models.TextField(blank=True, null=True, db_column='content', verbose_name='内容')
    answer = models.TextField(blank=True, null=True, db_column='answer', verbose_name='答案')
    qr_code = models.ImageField(blank=True, null=True, db_column='qr_code', verbose_name='二维码', upload_to='QRcode')
    previous_puzzle = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True,
                                        db_column='previous_puzzle',
                                        verbose_name='前一个谜题')
    solve_times = models.IntegerField(blank=True, null=True, default=0, db_column='solve_times', verbose_name='通关人数')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '谜题'
        verbose_name_plural = verbose_name
        db_table = 'puzzle'

    def save(self, *args, **kwargs):
        link_uuid = str(uuid.uuid1())
        self.link_uuid = link_uuid
        url = HOST + '/puzzle_page?link_uuid=' + link_uuid
        image_file = File(open(generate_qrcode(url, QRCODE_LOGO_PATH, QRCODE_PATH,
                                               '%s.png' % link_uuid), 'r'))
        image_file = File(image_file)
        self.qr_code = image_file
        super(self.__class__, self).save(*args, **kwargs)
        os.remove(image_file.name)


# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Puzzle)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.qr_code:
        if os.path.isfile(instance.qr_code.path):
            os.remove(instance.qr_code.path)

