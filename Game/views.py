# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from Game.models import Puzzle


def puzzle_page(request):
    link_uuid = request.GET.get('link_uuid')
    if link_uuid:
        return HttpResponse(link_uuid)
    else:
        return HttpResponse('error')
