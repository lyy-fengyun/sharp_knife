#!/usr/bin/python
# coding='utf-8'

import os
import glob
import unittest

def file_find(file_pattern):
    return  glob.glob(file_pattern)

def cmd_run(cmd):
    pro = os.popen('cmd')
    return pro.readlines()

def gen_grep_cmd(grepthing,file_list):
    pass

class TestOne(unittest.TestCase):
    def test_file_find(self):
        file_pattern='*.py'
        files = file_find(file_pattern)
        print(files)

    def test_cmd_run(self):
        print(cmd_run('dir'))

if __name__ == '__main__':
    unittest.main()