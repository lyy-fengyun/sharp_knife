#!/usr/bin/python2
# coding=utf-8
'''
根据smartcnf.ini 检查文件是否已经进行替换
usage: python smartcnfchk.py smartcnf.ini
'''
import ConfigParser as parser
import os
import socket
import time
import shutil
import platform
import logging
import sys
from string import Template

# 配置文件
config_file='smartcnf.ini'
midify_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
# 主机类型
os_type=platform.system()

key_value_split='='
origin="${origin}"

# report info
report_head=Template('#---------[$file_name] modify check report start--------')
report_ok_msg = Template("OK: [$key = $value] in [$file_name]")
report_error_msg = Template("ERROR: [$key = $value] in [$file_name],should be modify to [${s_value}]")
report_tail=Template('#---------[$file_name] modify check report ending--------')


def cmd_run(cmd):
    '''
    执行系统命令，并返回执行结果
    :param cmd:
    :return:
    '''
    ans = os.popen(cmd)
    return ans.readlines()

class PropertiesFileParse(object):
    '''
        解析配置文件
    '''
    def __init__(self,file_name):
        self._file_name = file_name

    def read_file(self):
        if os.path.isfile(self._file_name):
            logger.error("{} is not a file",self._file_name)
            raise IOError (self._file_name+" is not exist")
        else:
            with open(self._file_name,'r') as f_in:
                contents = f_in.readlines()
            return contents


def is_not_empty(string):
    '''
    判断是否为空串,用于filter
    :param string:
    :return: boolean
    '''
    if len(string)!=0:
        return True
    else:
        return False

def getConfigInfo():
    '''
    解析ini配置文件,获取需要修改文件的相关信息
    :return:
    '''
    global host_name,app_name

    config = parser.ConfigParser()
    config.read(config_file)
    sections = config.sections()  # 获取配置文件里的sections
    config_dict={}

    for section in sections:
        splits = section.split(" ")
        # 将空字符串进行过滤
        splits = filter(is_not_empty, splits)

        # 校验配置的主机是否包含文件所在的主机
        if len(splits) == 2 and (host_name not in section and splits[1] != "all"):
            continue

        # 校验主机与应用名是否符合要求
        if len(splits) == 3 and ((host_name not in section and splits[1] != "all") or (app_name not in section and splits[2]!="all")):
            continue

        model = splits[0].strip()
        values = config.items(section)
        # 配置为空则跳过
        if not len(values):
            continue

        if model in config_dict.keys():
            config_dict[model].extend(values)
        else:
            config_dict[model] = values
    logger.debug(config_dict)

    return config_dict


def convert(config_info_dict):
    '''
    将字典值由列表转化为字典
    :param config_info_dict:
    :return:
    '''
    for key in config_info_dict.keys():
        info=config_info_dict[key]

        file_modify={}
        for list_key,value in info:
            file_modify[list_key]=value
        config_info_dict[key]=file_modify

def backup_file(file_name):
    '''
    back up config file
    :param file_name: file name with path
    :return: backup file name
    :raise: IOERROR
    '''
    real_file_name=workspce+os.sep+file_name
    backup_file_name='_'+os.path.basename(real_file_name)+"_"+midify_time+'_bak'
    real_backup=os.path.dirname(real_file_name)+os.sep+backup_file_name
    if os.path.exists(real_file_name):
        shutil.copy(real_file_name,real_backup)

        logger.debug("backup %s",str(real_file_name))
        return real_backup
    else:
        raise IOError(real_file_name+" is not exist")


def convert_file_sep(file_path):
    '''
    将linux下的文件分割符转换为windows下的分隔符
    :param file_path: file_name
    :return:
    '''
    if os_type == 'Windows':
        return file_path.replace('/',os.sep)
    elif os_type == 'Linux' or os_type == "Unix":
        return file_path.replace("\\", os.sep)
    else:
        return file_path
    fi

def check_config_file(modify_info):
    '''
    根据给定的配置文件进行文件检查与备份
    :param modify_info: data of dict
    :return: none
    '''
    for file_name in modify_info.keys():
        # 处理路径分隔符
        file_name_deal = convert_file_sep(file_name)
        logger.debug(file_name_deal)

        modifies= modify_info[file_name]
        if os.path.basename(file_name_deal).endswith('xml'):
            print ("now can't check xml file, file name is "+file_name_deal)
            return
        else:
            # 读取文件内容
            try:
                file_contents = get_file_content(file_name_deal)
            except IOError as e:
                logger.error(e)
                continue
            full_file_path = os.getcwd() + os.sep +file_name_deal
            file_base_name=os.path.basename(file_name_deal)

            # 打印报告首部
            print report_head.substitute(file_name=full_file_path)
            defule_value = 'is not set'
            report_contents=[]
            # 检查配置项是否进行了替换
            for key,value in modifies.items():
                prod_value = file_contents.get(key,defule_value)

                if value == prod_value:
                    msg = report_ok_msg.substitute(key=key,value=prod_value,file_name=file_base_name)
                else:
                    if value.startswith(origin):
                        suffix = value.replace(origin,'')
                        if file_contents.get(key,'').endswith(suffix):
                            msg = report_ok_msg.substitute(key=key, value=prod_value, file_name=file_base_name)
                        else:
                            msg = report_error_msg.substitute(key=key,value=prod_value,file_name=file_base_name,s_value=value)
                    else:
                        msg = report_error_msg.substitute(key=key, value=prod_value, file_name=file_base_name,s_value=value)
                report_contents.append(msg)

            msgs = [x for x in report_contents if x.startswith("OK")]
            msgs.extend([x for x in report_contents if x.startswith("ERROR")])

            # 打印报告内容
            for info in msgs:
                print(info)

            # 打印报告尾部内容
            print report_tail.substitute(file_name=full_file_path)
            print("")

def get_file_content(file_name):
    '''
    根据文件名进行文件读取，并丢掉注释与空行
    :param file_name:
    :return:
    '''
    if os.path.exists(file_name):
        with open(file_name,'r') as f_in:
            contents = f_in.readlines()
            logger.debug(contents)
            # 处理文件换行符
            contents = [x.replace('\r\n','').replace('\n','').replace('\r','') for x in contents]
            #  删除注释与空行
            contents = [x for x in contents if not x.startswith("#")]
            contents = [x  for x in contents if len(x) != 0]
            logger.debug(contents)

            content_dict = {}
            for content in contents:
                key  = content.split(key_value_split)[0].strip()
                value  = content.split(key_value_split)[1].strip()
                content_dict[key] = value
            return content_dict
    else:
        raise IOError(file_name+" is didn't exist")


if __name__ == '__main__':
    # 主机名
    host_name = socket.gethostname()
    workspce = os.getcwd()
    app_name = os.path.basename(workspce)
    args = sys.argv
    # print(args)
    if len(args) < 2:
        print("Usage: python smartcnfchk.py smartcnf.ini")
        SystemExit(0)
    config_file=args[1]

    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    config_info=getConfigInfo()
    convert(config_info)
    logger.debug(config_info)

    check_config_file(config_info)
    print('config files have been checked!')