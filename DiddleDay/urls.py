# -*- coding: utf-8 -*-

"""DiddleDay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from DiddleDay.settings import MEDIA_URL, MEDIA_ROOT

from Game import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'index.html', views.index),
    url(r'^description\.html.*?', views.descriptions),
    url(r'^step1', views.step_1),
    url(r'^step_n', views.step_n),
    url(r'^feed.html', views.feed),
    url(r'^add_solve_times', views.add_solve_times),
    url(r'^Game/uploadImg', views.uploadImg),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)  # 设置访问静态文件
