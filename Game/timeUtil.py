#-*- coding: utf-8 -*
import time
from DiddleDay.settings import START_TIME, END_TIME

start_time = START_TIME
start_time_s = time.mktime(time.strptime(start_time, "%Y-%m-%d/%H:%M:%S"))

end_time = END_TIME
end_time_s = time.mktime(time.strptime(end_time, "%Y-%m-%d/%H:%M:%S"))


# 剩余开始/结束时间
def leftStartTime():
    return start_time_s - time.time()

def leftEndTime():
    return end_time_s - time.time()

# 是否已经开始
def isStart():
    left = leftStartTime()
    if left > 0:
        return False
    return True

# 是否已经结束
def isEnd():
    if isStart():
        left = leftEndTime()
        if left >= 0:
            return True
    return False

