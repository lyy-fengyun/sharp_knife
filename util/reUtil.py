#!/usr/bin/python
# coding=utf-8
import sys
import imp
imp.reload(sys)
sys.setdefaultencoding( "utf-8" )
import  re

def generateXmlTagPattern(xmlTagName):
    '''
    通过给定的xml tag 名称，生成对应的正则匹配
    :param xmlTagName:
    :return:
    '''
    tagstart = "<" + xmlTagName + ">"
    tagend = "</" + xmlTagName + ">"
    pattern = tagstart + "(.*)" + tagend
    return re.compile(pattern)

def getMatchInfo(info, pattern):
    if info is None or pattern is None:
        raise ValueError("must give two paramter")
    groupsValues = pattern.search(info)
    return groupsValues

def getXmlTagValue(info,pattern):
    '''
    获取xml文件中的 xml tag 标签中的值
    :param info: xml 字符串
    :param pattern: 正则匹配表达式
    :return: xml tag value
    '''
    value = ''
    match = getMatchInfo(info,pattern)
    if not match is None:
        value = match.group(1)
    return value

if __name__ == '__main__':
    pass