#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-17
# @Author  : 殷帅
# hive中的日期与shell格式日期的互相转换  效率工具

from time_util import *
import sys

import re


re_select_from = r'[\s\S]*SELECT([\s\S]*)FROM[\s\S]*'
re_comment = r'([\s\S]*) --([\s\S]*)[(][\s\S][)]'

re_yymmdd = re.compile(r'[\s\S]*[${]([\d-]+)d[_]yyyymmdd[}][\s\S]*', re.S)   # 用于匹配yyyyMMdd格式数据
re_yy_mm_dd = re.compile(r'[\s\S]*[${]([\d-]+)d[_]yyyy-mm-dd[}][\s\S]*', re.S)  # 用于匹配yyyy-MM-dd格式数据
re_pt = re.compile(r'[\s\S]*[${]([\d-]+)d[_]pt[\s\S]*', re.S)  # 用于匹配d_pt格式数据


# 反向转化　
re_pt_real = re.compile(r'[\s\S]*[^"]([\d]{8}000000)')
re_yymmdd_real = re.compile(r'[\s\S]*[^"](20[\d]{2}[\d]{2}[\d]{2})[\s\S]*')
re_yy_mm_dd_real = re.compile(r'[\s\S]*[^"](20[\d]{2}-[\d]{2}-[\d]{2})[\s\S]*')
re_yy_mm_real = re.compile(r'[\s\S]*[^"](20[\d]{2}-[\d]{2})[\'][\s\S]*')  # 匹配yyyy-MM格式



class DateShellTrans:
    def __init__(self, hive_sql, oper='true'):
        """
        类初始化函数
        :param table_name: 表英文名称
        :param hive_sql:
        :param oper 操作类型　
        """
        self.hive_sql = hive_sql
        self.oper = oper

    def replace_sql_pt_2_shell(self):
        """
        替换sql中的具体日期为shell格式的分区
        :return: 新的shell格式日期sql
        """
        if self.hive_sql.strip() == '':
            return self.hive_sql
        ret_sql = ""
        for sql_line in self.hive_sql.split('\n'):
            try:
                new_line = self.replace_sql_line_pt_2_shell(sql_line) + '\n'
                ret_sql += new_line
            except RuntimeError, e:
                print ("解析sql中的具体日期出现异常,异常行为  {} ,异常信息为 {} ".format(sql_line, e))
                # add logger info if have time
        return ret_sql

    @staticmethod
    def replace_sql_line_pt_2_shell(sql_line):
        """
        替换sql中的具体日期分区为shell格式的分区
        :param sql_line:
        :return:
        """
        # 匹配sql总的日期
        while re.findall(re_pt_real, sql_line):
            real_date = re.findall(re_pt_real, sql_line)[0]
            ranges = cal_timedelta(get_format_now('%Y%m%d000000'), real_date, '%Y%m%d000000')
            sql_line = sql_line.replace(real_date, '${%dd_pt}' % ranges)

        while re.findall(re_yymmdd_real, sql_line):
            real_date = re.findall(re_yymmdd_real, sql_line)[0]
            ranges = cal_timedelta(get_format_now('%Y%m%d'), real_date, '%Y%m%d')
            sql_line = sql_line.replace(real_date, '${%dd_yyyyMMdd}' % ranges)

        while re.findall(re_yy_mm_dd_real, sql_line):
            real_date = re.findall(re_yy_mm_dd_real, sql_line)[0]
            ranges = cal_timedelta(get_format_now('%Y-%m-%d'), real_date, '%Y-%m-%d')
            sql_line = sql_line.replace(real_date, '${%dd_yyyy-MM-dd}' % ranges)

        while re.findall(re_yy_mm_real, sql_line):
            real_date = re.findall(re_yy_mm_real, sql_line)[0]
            print real_date
            ranges = cal_timedelta(get_format_now('%Y-%m'), real_date, '%Y-%m')
            print ranges
            break
        return sql_line

    def replace_sql_shell_flag(self):
        """
        替换sql中的shell日期格式为
        :param hive_sql:输入的sq1
        :return: 转换之后的sql
        """
        if self.hive_sql.strip() == "":
            return self.hive_sql
        trans_sql = ""
        for line in self.hive_sql.split('\n'):
            trans_sql += self.replace_sql_line_shell_flag(line) + '\n'
        return trans_sql

    @staticmethod
    def replace_sql_line_shell_flag(sql_line):
        """
        将sql中的shell日期格式转换为实际日期格式
        :param sql_line:
        :return: new sql line
        """
        sql_line = sql_line.lower()
        while 'yyyymmdd}' in sql_line:
            print sql_line
            regex_info = re.findall(re_yymmdd, sql_line)  # 获取范围
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y%m%d", time_range_param)  # 打印真实时间
            # 拼接出原始样子
            shell_origin = '${%dd_yyyymmdd}' % time_range
            sql_line = sql_line.lower().replace(shell_origin, real_time)

        while 'yyyy-mm-dd}' in sql_line:
            regex_info = re.findall(re_yy_mm_dd, sql_line)
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y-%m-%d", time_range_param)
            shell_origin = '${%dd_yyyy-mm-dd}' % time_range
            sql_line = sql_line.lower().replace(shell_origin, real_time)

        while 'd_pt}' in sql_line:
            regex_info = re.findall(re_pt, sql_line)
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y%m%d000000", time_range_param)
            shell_origin = '${%dd_pt}' % time_range
            print shell_origin
            sql_line = sql_line.lower().replace(shell_origin, real_time)
        return sql_line


if __name__ == '__main__':
    sql = "where time = '2018-09'"
    dt = DateShellTrans(sql)
    dt.replace_sql_pt_2_shell()
    sys.exit(0)
    test_file = './sample1.sql'
    sql = ""
    with open(test_file, 'r') as f:
        sql = f.read()
    print sql
    dt = DateShellTrans(sql)
    trans_sql = dt.replace_sql_pt_2_shell()
    print trans_sql
    with open('./res.sql', 'w') as f:
        f.write(trans_sql)



#  需要添加一些单元测试用例　
