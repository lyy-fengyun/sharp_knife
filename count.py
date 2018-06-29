# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd 
import numpy as np 

file_name='file:///C:/Users/liyayong/Desktop/告警日报模板/告警日志导出/20180624-sampleExport.xls'
msgs = pd.read_excel(file_name)

sys_list = set(msgs["处理意见"])
needed_value=[]
for info in sys_list:
    if info.startswith("严重告警"):
        needed_value.append(info)

print(needed_value)
#print(sys_list)

# 1. 筛选出严重告警,电话保障的告警
deal_msg =  msgs[msgs["处理意见"].isin(needed_value)]

# 2. 重新排序
deal_msg = deal_msg.reindex(range(0,len(deal_msg.index)))

# 3. 根据业务线，省份，告警内容进行初步统计
ans = deal_msg.groupby(['业务线','省份','告警内容']).size()

# 4. 对排序结果进行类型转换
ans = ans.to_frame()

# 将结果写入到excel中
ans.to_excel('C:/Users/liyayong/Desktop/ans.xls','sheet1')

print(ans.head)     
