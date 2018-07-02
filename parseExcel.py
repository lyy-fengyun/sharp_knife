#!/usr/bin/python
# coding=utf-8

import xlrd

class ExcelFileReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_reader = xlrd.parse(file_name)

    def getSheetName(self):
        pass

    def getSheet(self,sheet_name):
        pass

    def getTitleFromSheet(self):
        pass

    def getContentFromSheet(self):
        pass

if __name__ == '__main__':

    pass