# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from DiddleDay.settings import BASE_DIR
from Game.models import Puzzle
import logging.config

logging.config.fileConfig(BASE_DIR + '/config.ini')
game_log = logging.getLogger('game_log')


def index(request):
    try:
        return render(request, 'index.html', locals())
    except Exception as e:
        game_log.exception(e)


def descriptions(request):
    try:
        return render(request, 'description.html', locals())
    except Exception as e:
        game_log.exception(e)


def step(request, page):
    try:
        if page == '1':
            return render(request, 'step1.html')
        else:
            return render(request, 'stepn.html')
    except Exception as e:
        game_log.exception(e)
