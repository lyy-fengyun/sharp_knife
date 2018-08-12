#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import  argparse
import configparser
from util import fileUtil
import paramiko
from util import LinuxServer
from util.LinuxServer import HostInfo


configFile = os.getcwd()+os.sep+"hnquery.ini"
hostDict = None

fileParse = configparser.ConfigParser()
fileParse.read(configFile)

def ssh_cmdlst_run(cmdLst:list) -> list:
    '''
    批量跑命令  -后续再实现多进程
    :param cmdLst: [] of {ip:'',cmd:''}
    :return:
    '''
    alarmInfos = []
    for cmdInfo in cmdLst:
        alarmInfos.append(ssh_cmd_run(cmdInfo))
    return alarmInfos

def ssh_cmd_run(cmdInfo:dict) -> list:
    '''
    远程执行命令
    :param cmdInfo: {ip:'',cmd:''}
    :return:
    '''
    ip = cmdInfo.get('ip')
    cmd = cmdInfo.get("cmd")
    hosInfo = HostInfo()
    hosInfo.ip = ip
    hosInfo.user="upayq"
    hosInfo.passwd = ''
    server = LinuxServer(hosInfo)
    cmdAns = server.runCommand(cmd)
    alarmInfo = cmdAns.get('outMessage')
    return alarmInfo

def localCmd(cmd):
    '''
    执行本地命令
    :param cmd:
    :return:
    '''
    cmdInfo = os.popen(cmd)
    infos = cmdInfo.read()
    return infos

def getHnqueryInfo():
    '''
    获取查询应用的告警日志目录信息
    :return:
    '''
    infos = []
    hnquery = "hnquery"
    if fileParse.has_section(hnquery):
        infos = fileParse.items(hnquery)
    return dict(infos)

def getHostNameOfIps(iplst,hosts_file='/etc/hosts'):
    '''
    根据ip获取对应的主机名
    :param iplst:
    :param hosts_file:
    :return:
    '''
    hosts = []
    lines = fileUtil.readAllLines(hosts_file)
    for ip in iplst:
        print(ip)
        [hosts.append(info.split(" ")[1]) for info in lines]
    global  hostDict
    hostDict = dict(zip(hosts,iplst))
    return set(hosts)

def getArgInfo():
    '''
    解析并获取参数信息
    :return:
    '''
    infos = getHnqueryInfo()
    hosts = getHostNameOfIps(infos.keys(),'info')
    parser = argparse.ArgumentParser(description='get alarm info which province')
    parser.add_argument(dest='iplst', metavar='ip list', nargs='*')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose mode')
    parser.add_argument('-n', dest='logNumber', action='store_true',
                        help='alarm num in one application')
    parser.add_argument('-i','--ip', dest='ip', action='store',choices=infos.keys(),
                        help='ip value')
    parser.add_argument('-H', '--hostname', dest='hostname', action='store',choices=hosts,
                        help=' host name')
    args = parser.parse_args()
    return args

def main():
    args = getArgInfo()
    ip = args.ip
    hostname = args.hostname
    logNum = args.logNumber

    pass

if __name__ == '__main__':
    print(getHnqueryInfo())
    print(getHostNameOfIps(getHnqueryInfo().keys(),'info'))
    getArgInfo()

    pass