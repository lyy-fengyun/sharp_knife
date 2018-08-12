# coding=utf-8

import socket
import paramiko
from paramiko.ssh_exception import AuthenticationException,SSHException
from paramiko import SSHClient,SFTPClient
from paramiko.client import AutoAddPolicy
from paramiko.rsakey import RSAKey
import os
import sys
import logging
logger = logging.getLogger('LinuxServer')

home_dir = os.path.expanduser('~')

SSH_CONFIG={
    'SSH_CONN_TIMEOUT':5, #连接超时时间，单位 秒
    'SSH_PORT':22,
    'SSH_CONN_TYPE':0, #0：无密码登录，1：使用密码登录，配置为0时，需要以下配置
    'SSH_CONN_PRIVATE_KEY_FILE' : home_dir+os.sep+'.ssh'+os.sep+'id_rsa', #本机私钥文件
    'StrictHostKeyChecking': 0, # 本机核对公钥标志：0核对，1不核对，核对时，需要配置公钥文件KNOWN_SSH_HOST_KEYS_FILE
    'KNOWN_SSH_HOST_KEYS_FILE' : home_dir+os.sep+'.ssh'+os.sep+'known_hosts', #公钥记录文件
    }

class HostInfo(object):
    '''
    数据类，保存主机信息
    '''
    @property
    def ip(self,ip):
        return self._ip

    @ip.setter
    def ip(self,ip):
        self._ip = ip

    @property
    def user(self):
        return self._user

    @ip.setter
    def user(self, user):
        self._user = user

    @property
    def passwd(self):
        return self._passwd

    @ip.setter
    def ip(self, passwd):
        self._passwd = passwd


class LinuxServer(object):
    def __init__(self,hostInfo):
        self.ip = hostInfo.ip
        self.user = hostInfo.user
        self.passwd = hostInfo.passwd
    
    sshClient=None
    '''
    远程连接操作
    '''
        
    def runCommand(self,command,timeouts=None,userPWD=False):
        """
        @summary: 在远程机器执行命令 并返回执行状态
        @param hostname:登录IP
        @param username: 用户名
        @param password: 密码
        @param command: 命令行
        @return: result 字典  保存执行状态  'outMessage':正常日志,'errorMessage':异常日志
        """
        result={'outMessage':'','errorMessage':''}
        csshc = self.createSSHClient(self.ip, self.user, self.passwd,userPWD)
        ssh=csshc[0]
        if ssh !=-1 and ssh!=-2:
            try:
                logger.info('连接主机成功！')
                logger.info('开始执行命令')
                if timeouts==0:
                    timeouts=None
                stdin,stdout,sterr=ssh.exec_command(command,timeout=timeouts)
                result['errorMessage']=sterr.read()
                result['outMessage']=stdout.read() 
                logger.info('执行命令结束！')
            except socket.timeout as e:
                logger.warning('执行命令超时！')
                result['errorMessage']='执行命令超时！'
                pass
            except Exception as e:
                logger.warning('执行命令发生异常！')
                result['errorMessage']='执行命令发生异常!'+str(e)
                pass
            if ssh.connect:
                ssh.close()
        else:
            result['errorMessage']=csshc[1]
        return result
    
    def createSSHClient(self,hostIP,username,password,userPWD=False):
        ssh_config = SSH_CONFIG
        otherErrorMessage=''
        try:
            ssh=SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if int(ssh_config['SSH_CONN_TYPE']) == 0 and (not userPWD):
                logger.info('无密码登录！')
                privateFile = ssh_config['SSH_CONN_PRIVATE_KEY_FILE']
                logger.info('加载私钥记录文件:{}'.format(privateFile))
                key=RSAKey.from_private_key_file(privateFile)
                if int(ssh_config['StrictHostKeyChecking']) == 0:
                    keyFileName=ssh_config['KNOWN_SSH_HOST_KEYS_FILE']
                    logger.info('加载公钥记录文件:{}'.format(keyFileName))
                    ssh.load_system_host_keys(keyFileName)
                logger.info('无密码连接主机:{}'.format(hostIP))
                ssh.connect(hostIP, int(ssh_config['SSH_PORT']), username, pkey=key, timeout=ssh_config['SSH_CONN_TIMEOUT'])
            else:
                logger.info('密码连接主机:{}'.format(hostIP))
                ssh.connect(hostname=hostIP,username=username,password=password,timeout=ssh_config['SSH_CONN_TIMEOUT'],allow_agent=False,look_for_keys=False)
            logger.info('连接成功！')
        except AuthenticationException as a:
            logger.warn('连接异常:{}'.format(a))
            otherErrorMessage= '登录失败：\r\n%s' % str(a)
            if ssh.connect:
                ssh.close()
            return -2,otherErrorMessage
        except SSHException as s:
            logger.warn('连接异常:{}'.format(s))
            otherErrorMessage= '连接主机异常,请检查账户、密码、密钥等信息的正确性，错误描述为：%s' %str(s)
            if ssh.connect:
                ssh.close()
            return -2,otherErrorMessage
        except socket.timeout as e:
            logger.warn('连接异常：{}'.format(e))
            otherErrorMessage='连接主机超时:%s' % str(e)
            if ssh.connect:
                ssh.close()
            return -1,otherErrorMessage
        except Exception as e:
            logger.warn('连接异常:{}'.format(e))
            otherErrorMessage= '未知异常：%s' %str(e)
            if ssh.connect:
                ssh.close()
            return -2,otherErrorMessage
        return ssh,otherErrorMessage
    
    def uploadFile(self,hostIP,username,password,localFilePath,localFileList,remotePath,remoteFileName=[],userPWD=False):
        """
        @summary: 上传文件到指定主机目录
        @param hostIP: 主机IP地址
        @param username: 主机账户
        @param password: 主机密码
        @param localFilePath: 上传文件的本地目录
        @param localFileList: 文件名，以列表形式，值为None时, 代表上传整个本地目录文件
        @param remotePath: 上传的远程目录
        @param port: 连接端口
        @return: uploadFlag(0:全部成功，-1：全部失败，-2：部分成功),otherErrorMessage(非传输类错误),
                            failFileList(上传失败的文件列表,列表值为数组，0下标为文件名，1下标为错误描述)
        """
        csshc = self.createSSHClient(hostIP, username, password,userPWD)
        ssh = csshc[0]
        if ssh !=-1 and ssh!=-2:
            if len(remoteFileName)==0:
                remoteFileName=None
            result = self.uploadFileHandle(localFilePath, localFileList, remotePath, ssh,remoteFileName)
            return result
        else:
            return csshc
    
    def _callback(self,a,b):
        logger.info('文件已上传大小: %10d,上传进度： %3.2f%%\r' %(a,a*100./int(b)))
            
    def uploadFileHandle(self,localFilePath,localFileList,remotePath,sshClient,remoteFileName=None):
        logger.info('本地上传目录：{},远程接收目录：{}'.format(localFilePath,remotePath))
        otherErrorMessage=''
        uploadFlag=0
        failFileList=[]
        successTotal=0
        if not os.path.exists(localFilePath):
            logger.warn('本地目录不存在：{}'.format(localFilePath))
            #otherErrorMessage=u'本地目录不存在：%s' % localFilePath
            sshClient.close()
            return -1,otherErrorMessage,localFileList
        try:
            sftp=SFTPClient.from_transport(sshClient.get_transport())
        except AuthenticationException as a:
            logger.warn('登录账号不存在：{}'.format(a))
            otherErrorMessage= '登录账号不存在：%s' % str(a)
            sshClient.close()
            return -2,otherErrorMessage,localFileList
        except SSHException as s:
            logger.warn('连接主机异常：{}'.format(s))
            otherErrorMessage= '连接主机异常,请检查账户、密码、密钥等信息的正确性，错误描述为：%s' %str(s)
            sshClient.close()
            return -2,otherErrorMessage,localFileList
        try:
            sftp.stat(remotePath)
        except IOError:
            #otherErrorMessage= u'远程目录不存在:%s' % remotePath
            logger.info('远程目录不存在,创建远程目录：{}'.format(remotePath))
            try:
                otherErrorMessage= otherErrorMessage+'\r\n创建远程目录：%s' % remotePath
                sftp.mkdir(remotePath)
                pass
            except Exception:
                sshClient.close()
                return -1,otherErrorMessage,localFileList
        if localFileList==None:
            localFileList=os.listdir(localFilePath)
        total=len(localFileList)
        localFilePath=localFilePath+'/'
        remotePath=remotePath+'/'
        for lfl in localFileList:
            try:
                localFile=os.path.join(localFilePath,lfl)
                if remoteFileName!=None and total == 1:
                    remouteFile=os.path.join(remotePath,remoteFileName)
                else:
                    remouteFile=os.path.join(remotePath,lfl)
                if not os.path.exists(localFile):
                    errorMessage='本地文件不存在:%s' % localFile
                    failFileList.insert(0, (lfl,errorMessage))
                    continue
                logger.info('##########################################')
                logger.info('开始上传文件:{},远程目录：{}'.format(lfl,remouteFile))
                sftp.put(localFile,remouteFile,self._callback,True)
                sftp.close()
                logger.info('文件上传成功!')
                successTotal=successTotal+1
            except Exception as e:
                logger.warn('上传文件发生异常：{}'.format(e))
                errorMessage= '上传文件发生异常:%s' % str(e)
                failFileList.insert(0, (lfl,errorMessage))
                pass
        if sshClient.connect:
            sshClient.close()
        if successTotal==total:
            logger.info('全部上传成功！')
            uploadFlag=0
        elif successTotal==0:
            logger.warn('全部上传失败！')
            uploadFlag=-1
        else:
            uploadFlag=-2
            logger.warn('部分上传成功！')
        return uploadFlag,otherErrorMessage,failFileList
    
