#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-19
# @Author  : 殷帅
# hive小工具单元测试

import unittest
import os
from date_shell_trans import DateShellTrans

test_sql_path = './test_sql'

class DateShellTransTest(unittest.TestCase):

    def test_shell_to_date(self):
        """
        测试shell_to_date 功能
        :return:
        """
        test_file_origin = './1-shell_to_date_sample.sql'
        test_sql_file_origin = os.path.join(test_sql_path, test_file_origin)
        test_file_target = os.path.join(test_sql_path, './1-shell_to_date_sample_out.sql')
        with open(test_sql_file_origin, 'r') as f:
            test_sql = f.read()
        if test_sql.strip() == '':
            raise ValueError("传入测试sql文件不能为空文件")
        dt_ins = DateShellTrans(test_sql)
        trans_res = dt_ins.replace_sql_shell_flag()
        with open(test_file_target, 'w') as f:
            f.write(trans_res)

    def test_date_to_shell(self):
        """
        测试date_to_shell功能
        :return:
        """
        test_file_origin = './2-date_to_shell_sample.sql'
        test_sql_file_origin = os.path.join(test_sql_path, test_file_origin)

        with open(test_sql_file_origin, 'r') as f:
            test_sql = f.read()
        if test_sql.strip() == '':
            raise ValueError("传入测试sql文件不能为空")
        dt_ins = DateShellTrans(test_sql)
        trans_res = dt_ins.replace_sql_pt_2_shell()
        test_file_out = './2-date_to_shell_sample_out.sql'
        # with open(os.path.join(test_sql_path, test_file_out), 'w') as f:
        #     f.write(trans_res)
        with open(os.path.join(test_sql_path, test_file_out), 'r') as f:
            self.assertEqual(trans_res, f.read())








