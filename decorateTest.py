#!/usr/bin/python
# coding=utf-8

from datetime import datetime
from functools import wraps


def mock(func,return_value=None):
    return return_value


def logException(func:function):
    @wraps()
    def inner(*args,**kwargs):
        try:
            ans = func(*args,**kwargs)
            return ans
        except Exception as e:
            print(e)
    return inner


@mock(return_value=30)
def add(x:int,y:int):
    #raise Exception("raised exception")
    return x+y;


def getDate():
    date  = datetime()
    return str(date.date())

if __name__ == '__main__':
    #print(mock(getDate,return_value=20190120))
    print(add(4,5))