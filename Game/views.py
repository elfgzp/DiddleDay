# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from DiddleDay.settings import BASE_DIR
from Game.models import Puzzle
import logging.config
import time

logging.config.fileConfig(BASE_DIR + '/config.ini')
game_log = logging.getLogger('game_log')


def index(request):
    start_time = "2016-10-10 00:00:00"
    start_time_s = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    try:
        link_uuid = request.GET.get('link_uuid')
        parameter = '?link_uuid=%s' % link_uuid if link_uuid else ''
        if start_time_s - time.time() > 0:
            return render(request, 'countdown.html', {'left_time': start_time_s - time.time()})
        return render(request, 'index.html', locals())
    except Exception as e:
        game_log.exception(e)


def descriptions(request):
    try:
        return render(request, 'description.html', locals())
    except Exception as e:
        game_log.exception(e)


def step_1(request):
    try:
        link_uuid = request.GET.get('link_uuid')
        if link_uuid:
            first_puzzle = Puzzle.objects.filter(link_uuid=link_uuid).first()
            has_first_puzzle = False
            if first_puzzle:
                has_first_puzzle = True
            return render(request, 'step1.html', locals())
        else:
            first_puzzle = Puzzle.objects.filter(previous_puzzle=None).first()
            has_first_puzzle = False
            if first_puzzle:
                has_first_puzzle = True
            return render(request, 'step1.html', locals())
    except Exception as e:
        game_log.exception(e)


def step_n(request):
    try:
        start_time = "2016-10-10 00:00:00"
        start_time_s = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if start_time_s - time.time() > 0:
            return render(request, 'countdown.html', {'left_time': start_time_s - time.time()})
        link_uuid = request.GET.get('link_uuid')
        if link_uuid:
            puzzle = Puzzle.objects.filter(link_uuid=link_uuid).first()
            if puzzle:
                if puzzle.previous_puzzle:
                    return render(request, 'stepn.html', locals())
                else:
                    return redirect('index.html?link_uuid=%s' % link_uuid)
            else:
                return HttpResponse('404')
        else:
            return HttpResponse('404')
    except Exception as e:
        game_log.exception(e)


def feed(request):
    try:
        return render(request, 'feed.html', locals())
    except Exception as e:
        game_log.exception(e)


def add_solve_times(request):
    try:
        link_uuid = request.GET.get('link_uuid')
        if link_uuid:
            puzzle = Puzzle.objects.filter(link_uuid=link_uuid).first()
            if puzzle:
                puzzle.solve_times += 1
                super(Puzzle, puzzle).save()
                return HttpResponse('{status:1}')
            else:
                return HttpResponse('{status:0, error:"Can not find puzzle!"')
    except Exception as e:
        game_log.exception(e)
