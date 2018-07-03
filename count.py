# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd 
import numpy as np
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
        self.ori_data = pd.read_excel(data_file)
        droped_columns = ['关键字','处理人','工单编号','备注','处理时间','项目包名路径','过滤原因']
        self.ori_data = AnalysisAlarmData.drop_columns(self.ori_data, droped_columns)

    @staticmethod
    def drop_columns(ori_data,column_keys):
        if isinstance(column_keys,list):
            logger.info("开始删除数据，%s", str(column_keys))
            return ori_data.drop(column_keys,axis=1)
        else:
            raise TypeError("参数需要为列表")

    def assignValueToNan(self):
        self.ori_data["业务线"].apply()
        pass

    def count_dealed_alarm(self):
        '''
        statistic alarm data according to province,business line,alarm content
        :return: None
        '''
        # 1. 筛选出严重告警,电话保障的告警
        sys_list = set(self.ori_data["处理意见"])
        needed_value = []
        for info in sys_list:
            if info.startswith("严重告警"):
                needed_value.append(info)
        deal_msg = self.ori_data[self.ori_data["处理意见"].isin(needed_value)]

        # 2. 重新排序
        deal_msg = deal_msg.reindex(range(0, len(deal_msg.index)))

        # 3. 根据业务线，省份，告警内容进行初步统计
        ans = deal_msg.groupby(['省份', '业务线', '告警内容']).size().sort_values()

        # 4. 对排序结果进行类型转换
        ans = ans.to_frame()

        # 将结果写入到excel中git
        ans.to_excel('C:/Users/liyayong/Desktop/ans.xls', 'sheet1')


if __name__ == "__main__":
    file_name = 'file:///C:/Users/liyayong/Desktop/告警日报模板/告警日志导出/20180624-sampleExport.xls'
    analysis = AnalysisAlarmData(file_name)
    analysis.count_dealed_alarm()