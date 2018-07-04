# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import pandas as pd
import numpy as np
import os
import  datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AnalysisAlarmData')

class AnalysisAlarmData(object):

    def __init__(self, data_file):
        '''
         constructor of AnalysisAlarmData
        :param data_file: excel file name, which stored alarm data
        '''
        if  not isinstance(data_file,str):
            raise TypeError("参数传递错误")
        logger.info("从[%s]文件中读取数据",data_file)
        self.ori_data = pd.read_excel(data_file)
        droped_columns = ['关键字','处理人','工单编号','备注','处理时间','项目包名路径','过滤原因']
        self.ori_data = AnalysisAlarmData.drop_columns(self.ori_data, droped_columns)
         # 删除列为空的数据
        logger.info("删列为空的其他列")
        self.ori_data.dropna(axis=1, how='all')

        # 对默认值进行设置
        logger.info("对所有的空值设置默认值")
        self.ori_data =  self.ori_data.fillna('default_value')
        #print(self.ori_data.head(5))

    @staticmethod
    def drop_columns(ori_data,column_keys):
        '''
        delete given clumns data from given data
        :param ori_data: DataFrame of given
        :param column_keys: key of columns
        :return: DataFrame of delete columns
        '''
        if isinstance(column_keys,list):
            logger.info("开始删除数据，%s", str(column_keys))
            return ori_data.drop(column_keys,axis=1)
        else:
            raise TypeError("参数需要为列表")

    def count_dealed_alarm(self,ans_file_name,isSeriousAlarm):
        '''
        statistic alarm data according to province,business line,alarm content
        :return: None
        '''
        # 1. 筛选出严重告警,电话保障的告警
        if(isSeriousAlarm):
            logger.info("筛选严重告警，已经提过工单的告警")
            deal_msg = self.delete_data("处理意见","严重告警")
            if(deal_msg is None or len(deal_msg.index) == 0):
                logger.info("没有严重告警")
                return None
        else:
            deal_msg = self.ori_data
        #deal_msg = self.ori_data
        # 2. 重新排序
        #deal_msg = deal_msg.reindex(range(0, len(deal_msg.index)))
        #deal_msg.to_excel(ans_file_name, 'sheet3')
        # 3. 根据业务线，省份，告警内容进行初步统计
        logger.info("对告警进行分类统计")
        ans = deal_msg.groupby(['告警内容','省份', '业务线'])
        ans = ans.size()
        print(ans)
        # 4. 对排序结果进行类型转换
        ans = ans.to_frame()

        # 将结果写入到excel中
        logger.info("将统计结果写入到excel[%s]中",ans_file_name)
        ans.to_excel(ans_file_name, 'sheet1')

    def delete_data(self,key,contene_start):
        # 1. 筛选出严重告警,电话保障的告警
        sys_list = set(self.ori_data[key])
        needed_value = []
        for info in sys_list:
            if info.startswith(contene_start):
                needed_value.append(info)
        logger.info("严重告警如下：[%s]",str(needed_value))
        if(len(needed_value) == 0):
            return None
        else:
            return self.ori_data[self.ori_data[key].isin(needed_value)]

def getTodayFileList(file_dir):
    if(os.path.isdir(file_dir)):
        today = getToday()
        file_name_list = os.listdir(file_dir)
        for file_name in file_name_list[:]:
            if not file_name.startswith(today):
                file_name_list.remove(file_name)
        return file_name_list
    else:
        logger.info("[%s] 不是文件夹！",file_dir)

def getToday():
    '''
    获取当前日期时间
    :return: yyyymmdd
    '''
    today = datetime.datetime.now()
    today = today.strftime("%Y%m%d")
    logger.info("当前日期为：[%s]", today)
    return  today

def mock_getToday():
    return "20180702"

if __name__ == "__main__":
    base_dir=r"F:\值班对账查询学习\5 值班告警\值班告警相关资料\告警日报模板"
    file_name_list = getTodayFileList(base_dir)
    # 是否只统计严重告警, true 只统计严重告警，false,统计所有的告警
    isOnlyStaticSeriousAlarm = True
    for file_name in file_name_list:
        logger.info("文件列表：[%s]", str(file_name_list))
        complete_file_name = base_dir + os.sep + file_name
        ans_file_name = 'ans_'+file_name
        ans_file = base_dir +os.sep +ans_file_name

        try:
            logger.info("统计告警文件[%s]",complete_file_name)
            analysis = AnalysisAlarmData(complete_file_name)
            analysis.count_dealed_alarm(ans_file,isOnlyStaticSeriousAlarm)
        except Exception  as e:
            logger.warning("[%s] 统计出现问题,异常信息为:[%s]",complete_file_name,str(e))
            print(e)