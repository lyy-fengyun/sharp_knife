#!/usr/bin/python
# coding='utf-8'
import unittest
from py_grep import *

class TestOne(unittest.TestCase):
    def test_file_find(self):
        file_pattern='*.py'
        files = file_find(file_pattern)
        print(files)

    @unittest.skip("cmd_run have some problem")
    def test_cmd_run(self):
        pass
        #print(cmd_run('dir'))

if __name__ == '__main__':
    unittest.main()