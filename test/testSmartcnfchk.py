#!/usr/bin/python
# coding=utf-8
import unittest
import os
import logging
import smartcnfchk as chk
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Test_chk(unittest.TestCase):
    def setUp(self):
        chk.logger = logger
        self.file_name_not_exist = "test_file"
        self.file_name_exist="file_exist.txt"
        self.file_name_exist_with_path = "test/file_exist.txt"

        with open(self.file_name_exist,'w') as f_out:
            f_out.write("this is a test file")

        self.dir_test=os.path.dirname(self.file_name_exist_with_path)
        os.mkdir(self.dir_test)
        with open(self.file_name_exist_with_path,'w') as f_out:
            f_out.write("this is a test file")

    # 测试 None 值
    def test_backup_file_None(self):
        back_file = chk.backup_file(None)
        self.assertIsNone(back_file)

    # 测试不存在的文件
    def test_backup_file_file_not_exist(self):
        self.assertRaises(IOError,chk.backup_file,self.file_name_not_exist)

    # 测试不带路径的文件
    def test_backup_file_file_exis(self):
        back_file_name = chk.backup_file(self.file_name_exist)
        self.assertTrue(os.path.exists(back_file_name))
        os.remove(back_file_name)

    # 测试带有路径的文件
    def test_backup_file_file_exis_with_path(self):
        back_file_name = chk.backup_file(self.file_name_exist_with_path)
        self.assertTrue(os.path.exists(back_file_name))
        os.remove(back_file_name)

    def tearDown(self):
        os.remove(self.file_name_exist)
        # 删除非空文件夹
        shutil.rmtree(self.dir_test)


if __name__ == '__main__':
    unittest.main()