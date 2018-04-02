#!/usr/bin/python2s
# coding=utf-8
'''
修改配置文件，xml, propertirs,
'''
import ConfigParser as parser
import os
import socket
import time
import shutil
import platform
import logging

# 配置文件
config_file='smartcnf.ini'
midify_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
# 主机类型
os_type=platform.system()


def cmd_run(cmd):
    '''
    执行系统命令，并返回执行结果
    :param cmd:
    :return:
    '''
    ans = os.popen("cmd")
    return ans.readlines()

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
    print(sections)
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

def modify_config_file(modify_info):
    '''
    根据给定的配置文件进行文件备份与修改
    :param modify_info: data of dict
    :return: none
    '''
    for file_name in modify_info.keys():
        # 处理路径分隔符
        file_name_deal = convert_file_sep(file_name)
        print(file_name_deal)

        modifies= modify_info[file_name]
        try:
            backup_file_name=backup_file(file_name_deal)
        except IOError as msg:
            print(msg)
            continue

        if os.path.basename(file_name_deal).endswith('xml'):
           return
        else:
            # with open(backup_file_name, 'rU') as f_in:
            with open(backup_file_name,'r') as f_in:
                #print(f_in.readlines())
                key_used=[]
                with open(workspce+os.sep+file_name,'w') as f_out:
                    lines  = f_in.readlines()
                    for line in lines:
                        # 替换掉换行符
                        line = line.replace('\r\n','').replace('\n','').replace('\r','')

                        if line.startswith("#") or not len(line):
                            f_out.write(line+'\n')
                        elif line.split('=')[0].strip() in modifies.keys():
                            key=line.split('=')[0].strip()
                            value=modifies[key]
                            # 在原先值的后面进行新增
                            if value.startswith("${origin}"):
                                value = line.split('=')[1].strip()
                                value = modifies[key].replace("${origin}",value)

                            # 替换key的值
                            f_out.write(key+"="+value+'\n')
                            key_used.append(key)
                        else:
                            f_out.write(line + '\n')

                    # 新增 key-value 值
                    for key in modifies.keys():
                        if key not in key_used:
                            f_out.write(key+"="+modifies[key]+'\n')



if __name__ == '__main__':
    # 主机名
    host_name = socket.gethostname()
    workspce = os.getcwd()
    app_name = os.path.basename(workspce)

    print(host_name)
    print(workspce)
    print(app_name)
    config_info=getConfigInfo()
    convert(config_info)
    modify_config_file(config_info)
    print(config_info)

