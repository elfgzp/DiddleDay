# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
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


def step_1(request):
    try:
        first_puzzle = Puzzle.objects.filter(previous_puzzle=None).first()
        has_first_puzzle = False
        if first_puzzle:
            has_first_puzzle = True
        return render(request, 'step1.html', locals())
    except Exception as e:
        game_log.exception(e)


def step_n(request):
    try:
        link_uuid = request.GET.get('link_uuid')
        if link_uuid:
            puzzle = Puzzle.objects.filter(link_uuid=link_uuid).first()
            if puzzle:
                if puzzle.previous_puzzle:
                    return render(request, 'stepn.html', locals())
                else:
                    return redirect('index.html')
            else:
                return HttpResponse('404')
        else:
            return HttpResponse('404')
    except Exception as e:
        game_log.exception(e)


def add_solve_times(request):
    try:
        link_uuid = request.GET.get('link_uuid')
        if link_uuid:
            puzzle = Puzzle.objects.filter(link_uuid=link_uuid).first()
            if puzzle:
                if puzzle.previous_puzzle:
                    puzzle.previous_puzzle.solve_times += 1
                    super(Puzzle, puzzle.previous_puzzle).save()
                    return HttpResponse('{status:1}')
                else:
                    return HttpResponse('{status:0, error:"Can not find previous puzzle!"')
            else:
                return HttpResponse('{status:0, error:"Can not find puzzle!"')
    except Exception as e:
        game_log.exception(e)
