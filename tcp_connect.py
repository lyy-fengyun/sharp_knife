#!/usr/bin/env python
# coding=utf-8

import socket
import sys
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(2)
if len(sys.argv) <3:
    print "Usage: ./tcp_connect.py dest_ip port"
    sys.exit(20)

green_start='\033[1;32m'
red_start='\033[1;31m'
color_closed='\033[0m'

dest_ip,port = sys.argv[1:]

def get_host_ip():
    '''
    获取本机ip
    :return:
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip

local_ip = get_host_ip()
try:
    sk.connect((dest_ip,int(port)))
    print '{} From {} telnet to {} on port {} OK!{}'.format(green_start,local_ip,dest_ip,port,color_closed)
except Exception:
    print '{} From {} telnet to {} on port {} Failed!{}'.format(red_start,local_ip,dest_ip, port,color_closed)
    print e 
sk.close()
