# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from django.db import models
from django.dispatch import receiver
from django.core.files import File
import uuid
from Game.qrCode import generate_qrcode
from DiddleDay.settings import BASE_DIR, HOST, PORT, QRCODE_PATH, QRCODE_LOGO_PATH
import logging.config

logging.config.fileConfig(BASE_DIR + '/config.ini')
game_log = logging.getLogger('game_log')


class Puzzle(models.Model):
    link_uuid = models.CharField(blank=True, null=True, max_length=100, db_index=True,
                                 db_column='link_uuid',
                                 verbose_name='唯一识别码')
    name = models.CharField(blank=True, null=True, max_length=100, db_column='name', verbose_name='谜题')
    story_description = models.TextField(blank=True, null=True, db_column='story_description', verbose_name='该二维码的内容')
    content = models.TextField(blank=True, null=True, db_column='content', verbose_name='该二维码的问题')
    answer = models.TextField(blank=True, null=True, db_column='answer', verbose_name='该问题的答案')
    hint = models.TextField(blank=True, null=True, db_column='hint',
                            verbose_name='该二维码的位置提示')
    qr_code = models.ImageField(blank=True, null=True, db_column='qr_code', verbose_name='二维码', upload_to='QRcode')
    qr_code_host_n_port = models.CharField(blank=True, null=True, max_length=100, db_column='qr_code_host_n_port',
                                           verbose_name='二维码存储的域名和地址')
    previous_puzzle = models.OneToOneField('self', models.DO_NOTHING, blank=True, null=True,
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
        try:
            _ = Puzzle.objects.filter(link_uuid=self.link_uuid).first()
            if not _:
                link_uuid = str(uuid.uuid1())
                self.link_uuid = link_uuid
                self.qr_code_host_n_port = '%s:%s' % (HOST, PORT)
                url = 'http://%s/step_n?link_uuid=%s' % (self.qr_code_host_n_port, link_uuid)
                image_file = File(open(generate_qrcode(url, QRCODE_LOGO_PATH, QRCODE_PATH,
                                                       '%s.png' % link_uuid), 'r'))
                image_file = File(image_file)
                self.qr_code = image_file
            super(self.__class__, self).save(*args, **kwargs)
            if not _:
                os.remove(image_file.name)
        except Exception as e:
            game_log.exception(e)


class Feed(models.Model):
    email = models.CharField(blank=True, null=False, max_length=100, db_column='email', verbose_name='邮箱')
    content = models.TextField(blank=True, null=True, db_column='content', verbose_name='建议内容')
    date_time = models.DateTimeField(blank=True, null=False, db_column='date_time', verbose_name='时间', auto_now=True)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = '意见建议'
        verbose_name_plural = verbose_name
        db_table = 'feed'


# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Puzzle)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    try:
        """Deletes file from filesystem
            when corresponding `MediaFile` object is deleted.
            """
        if instance.qr_code:
            if os.path.isfile(instance.qr_code.path):
                os.remove(instance.qr_code.path)
    except Exception as e:
        game_log.exception(e)


def check_qrcode():
    try:
        host_n_port = '%s:%s' % (HOST, PORT)
        all_puzzle = Puzzle.objects.filter().all()
        if all_puzzle:
            for each_puzzle in all_puzzle:
                if each_puzzle.qr_code_host_n_port != host_n_port:
                    url = 'http://%s:%s/step_n?link_uuid=%s' % (HOST, PORT, each_puzzle.link_uuid)
                    image_file = File(open(generate_qrcode(url, QRCODE_LOGO_PATH, QRCODE_PATH,
                                                           '%s.png' % each_puzzle.link_uuid), 'r'))
                    image_file = File(image_file)
                    each_puzzle.qr_code = image_file
                    each_puzzle.qr_code_host_n_port = host_n_port
                    super(Puzzle, each_puzzle).save()
                    os.remove(image_file.name)
    except Exception as e:
        game_log.exception(e)


def generate_index_qrcode():
    generate_qrcode('http://%s:%s' % (HOST, PORT), QRCODE_LOGO_PATH, QRCODE_PATH, 'first_puzzle.png')


generate_index_qrcode()
check_qrcode()
