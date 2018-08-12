#!/usr/bin/python
# coding=utf-8

import tools.logTools.logQuery as logquery

if __name__ == '__main__':
    logquery.getHnqueryInfo()
    logquery.getHostNameOfIps(logquery.getHnqueryInfo().keys(),'tools//logTools//info')
    logquery.getArgInfo()
    pass