# -*- coding: UTF-8 -*-

import sys
import os
import re
import traceback
import gzip
import csv
from  functools import wraps
# FileName: fileUtil.py  # 模块名
__all__ = ['readAllLines','writeListToFile','List_All_Files','Files_Filter','paraseOrdernumTimestamp','isDir','isFile']


def exception_deal(exceptionObj):
    '''
    异常处理
    :param exceptionObj: 异常对象
    :return:
    '''
    print(exceptionObj)
    traceback.print_exc()

def fileOpenError_catch(func):
    '''
    文件打开装饰器
    :param func:
    :return:
    '''
    @wraps(func)
    def inner(*args,**kwargs):
        try:
            ans = func(*args,**kwargs)
            return ans
        except (IOError,ValueError,TypeError,Exception) as e:
            exception_deal(e)
    return inner

@fileOpenError_catch
def readAllLines(fileName):
    '''
    获取文件所有内容
    :param fileName: 文件路径
    :return: [] content of file,  line strip  wihth weight space
    '''
    if fileName.endswith("gz"):
        return _readAllLineFromGzipFile(fileName)
    else:
        return _readAllLineFromFile(fileName)

def _readAllLineFromFile(fileName):
    with  open(fileName, 'r') as file_object:
        return _readAllLineFronFileobj(file_object)

def _readAllLineFromGzipFile(fileName):
    with  gzip.open(fileName, 'r') as file_object:
        return _readAllLineFronFileobj(file_object)

def _readAllLineFronFileobj(f_in):
    if f_in is None:
        raise  ValueError("f_in must be not None")
    lines = f_in.readlines()
    lines = [x.strip() for x in lines]
    return lines

@fileOpenError_catch
def writeListToFile(filename, content):
    '''
    :param filename: 文件路径
    :param content：写入内容 list:
    :return: boolean write to file success return True, else False
    '''
    isSuccess = False
    infos = [line + os.linesep for line in content]
    with open(filename, 'w') as f_out:
        f_out.writelines(infos)
    isSuccess = True
    return isSuccess

@fileOpenError_catch
def paraseOrdernumTimestamp(fileName):
    '''
    :param fileName:
    :return:
    '''
    orderTimeDict = {}
    with open(fileName, 'r') as file_object:
        for line in file_object:
            line = line.decode('utf-8').split('#')
            orderTimeDict[line[1]] = line[0]
    return orderTimeDict

@fileOpenError_catch
def List_All_Files(rootdir):
    '''
    返回目录下（包括子目录）所有文件
    :param rootdir: base dir
    :return: files[] 返回文件列表
    '''
    if not isDir(rootdir):
        raise IOError("rootdir is not directort file, it should be a dir file")
    fileList = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            fileList.extend(List_All_Files(path))
        if os.path.isfile(path):
            fileList.append(path)
    return fileList

def Files_Filter(file_list,name_pattern):
    '''
    输入文件列表，需要匹配的文件名，返回匹配文件列表
    :param file_list: list of file name with file path
    :param name_pattern: 需要匹配文件的正则表达式
    :return: 参数不为Null值，通过正则匹配返回文件列表，否则返回空列表
    '''
    if file_list is None or name_pattern is None:
        return []
    re_pattern = re.compile(name_pattern)
    return [x for x in file_list if re_pattern.search(x)]

@fileOpenError_catch
def getheadTailInfoFromFile(messageFileName):
    '''
    根据给定的文件路径，获取文件的第一行与最后一行内容
    :param messageFileName: filename with path
    :return: first line, last line
    '''
    fileSize  = os.path.getsize(messageFileName)
    if fileSize < 500:
        # 处理小文件
        contentList = readAllLines(messageFileName)
        return contentList[0],contentList[-1]
    else:
        # 处理大文件
        if messageFileName.endswith("gz"):
            with gzip.open(messageFileName, 'rb') as f_in:  # 打开文件
                return  _getFirstAndLastLineFromFileObj(f_in)
        else:
            with open(messageFileName, 'rb') as f_in:  # 打开文件
                return  _getFirstAndLastLineFromFileObj(f_in)

def _getFirstAndLastLineFromFileObj(f_in):
    # 在文本文件中，没有使用b模式选项打开的文件，只允许从文件头开始,只能seek(offset,0)
    first_line = f_in.readline()  # 取第一行
    offset = -50  # 设置偏移量
    while True:
        """
        file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
        如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。
        """
        f_in.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
        lines = f_in.readlines()  # 读取文件指针范围内所有行
        if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
            last_line = lines[-1]  # 取最后一行
            break
        # 如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
        # 所以off翻倍重新运行，直到readlines不止一行
        offset *= 2
    return first_line.decode(), last_line.decode()

@fileOpenError_catch
def dictReadFromCsvFile(fileName:str,file_header=None) -> []:
    '''
    读取csv文件中的内容，以字典的形式
    :param fileName: 文件名
    :param file_header: info key list
    :return: [] list of dict infos
    '''
    infoLines = []
    with open(fileName,'r') as f_in:
        readerIte = csv.DictReader(f_in,restkey=file_header)
        [infoLines.append(line) for line in readerIte]
    return infoLines

def isDir(dirName):
    '''
    判断文件是否为目录
    :param dirName:
    :return:
    '''
    if os.path.isdir(dirName):
        return True
    return  False

def isFile(fileName):
    '''
     判断文件是否为文件
    :param fileName:
    :return:
    '''
    if os.path.isfile(fileName):
        return True
    return  False

@fileOpenError_catch
def gzip_compress(gzipFileName,srcFileName):
    '''
    压缩文件
    :param gzipFileName: 文件压缩后的名字
    :param srcFileName: 源文件
    :return:
    '''
    with gzip.open(gzipFileName,'wb') as f_out:
        lines = readAllLines(srcFileName)
        [f_out.write(x+os.linesep) for x in lines]
    return True