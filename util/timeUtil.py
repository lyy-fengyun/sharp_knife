#!/usr/bin/python
# coding=utf-8


import sys
import imp
imp.reload(sys)
sys.setdefaultencoding( "utf-8" )
from  datetime import datetime
import time
import traceback
def strToDatetime(timeStr,timeFormat="%Y-%m-%d %H:%M:%S.%f"):
    '''
    将时间字符串转换为 datatime 类型的数据
    :param timeStr: 时间字符
    :param timeFormat: 时间模式, 默认设置为 %Y-%m-%d %H:%M:%S.%f
    :return: datetime
    '''
    dateTimeObj = None
    try:
        dateTimeObj = datetime.strptime(timeStr, timeFormat)
    except ValueError as err:
        print(err)
        # 通过 traceback 打印当前的错误堆栈信息
        traceback.print_exc()
    return dateTimeObj

def strTotimestamp(timeStr,timeFormat="%Y-%m-%d %H:%M:%S.%f"):
    '''
    将时间字符串转换为毫秒时间戳
    :param timeStr: 时间字符串
    :param timeFormat: 时间字符格式， 默认："%Y-%m-%d %H:%M:%S.%f"
    :return:
    '''
    time_info = strToDatetime(timeStr,timeFormat)
    return datetimeTotimestamp(time_info)

def datetimeTotimestamp(timeGiven):
    '''
    将 datetime 时间类型的函数准换为时间戳，微妙
    :param timeGiven:
    :return:
    '''
    if timeGiven is None:
        raise ValueError("paramter timeGiven is None value, It should be a datetime object")
    # 获取毫秒数， time_info.microsecond 微妙
    millseconds = timeGiven.microsecond // 1000
    timestamp = time.mktime(timeGiven.timetuple())
    return int(timestamp * 1000 + millseconds)

if __name__ == '__main__':
    pass