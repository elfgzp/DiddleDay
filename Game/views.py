# -*- coding: utf-8 -*-
import os
import time

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DiddleDay.settings import BASE_DIR
from Game.models import Puzzle, Feed
import logging.config
import timeUtil
import json

logging.config.fileConfig(BASE_DIR + '/config.ini')
game_log = logging.getLogger('game_log')


def index(request):
    # start_time = "2016-10-10 00:00:00"
    # start_time_s = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    try:
        link_uuid = request.GET.get('link_uuid')
        parameter = '?link_uuid=%s' % link_uuid if link_uuid else ''
        if not timeUtil.isStart():
            return render(request, 'countdown.html', {'left_time': timeUtil.leftStartTime()})
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
        # start_time = "2016-10-10 00:00:00"
        # start_time_s = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if not timeUtil.isStart():
            return render(request, 'countdown.html', {'left_time': timeUtil.leftStartTime()})
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
        submit_success = False
        if request.method == 'POST':
            email = request.POST.get('email')
            content = request.POST.get('content')
            feed_back = Feed(email=email, content=content)
            feed_back.save()
            submit_success = True
        return render(request, 'feed.html', locals(), RequestContext(request))
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


@csrf_exempt
def uploadImg(request):
    if request.method == 'POST':
        file_obj = open("log.txt", "w+")
        buf = request.FILES.get('imgFile', None)
        print >> file_obj, str(buf)
        file_buff = buf.read()
        time_format = str(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
        try:
            file_name = "img_" + time_format + ".jpg"
            save_file("Game/static/content_img", file_name, file_buff)
            dict_tmp = {}
            dict_tmp["error"] = 0
            dict_tmp["url"] = "/static/content_img/" + file_name
            return HttpResponse(json.dumps(dict_tmp))
        except Exception, e:
            dict_tmp = {}
            dict_tmp["error"] = 1
            print >> file_obj, e
            return HttpResponse(json.dumps(dict_tmp))


# 对path进行处理
def mkdir(path):
    # 去除左右两边的空格
    path = path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
    return path


# 保存相关的文件
def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


def get_first_puzzle(puzzle):
    try:
        while puzzle.previous_puzzle:
            puzzle = puzzle.previous_puzzle
        return puzzle
    except Exception as e:
        game_log.exception(e)
        return None
