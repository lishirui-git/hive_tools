#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-17
# @Author  : 殷帅
# hive中的日期与shell格式日期的互相转换

from time_util import *


class DateShellTrans:
    def __init__(self, hive_sql, oper):
        """
        类初始化函数
        :param table_name: 表英文名称
        :param hive_sql:
        :param oper 操作类型　
        """
        self.hive_sql = hive_sql
        self.oper = oper

    @staticmethod
    def replace_pt_2_shell(sql_line):
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

        return sql_line

    @staticmethod
    def replace_shell_flag(sql_line):
        """
        替换
        :param sql_line:
        :return:
        """
        sql_line = sql_line.lower()
        while 'yyyymmdd}' in sql_line:
            print sql_line
            regex_info = re.findall(re_yymmdd, sql_line)  # 获取范围
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y%m%d", time_range_param)  # 打印真实时间
            # 拼接出原始样子
            shell_origin = '${%dd_yyyymmdd}' % (time_range)
            sql_line = sql_line.lower().replace(shell_origin, real_time)

        while 'yyyy-mm-dd}' in sql_line:
            regex_info = re.findall(re_yy_mm_dd, sql_line)
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y-%m-%d", time_range_param)
            shell_origin = '${%dd_yyyy-mm-dd}' % (time_range)
            sql_line = sql_line.lower().replace(shell_origin, real_time)

        while 'd_pt}' in sql_line:
            regex_info = re.findall(re_pt, sql_line)
            time_range = int(regex_info[0])
            time_range_param = -time_range
            real_time = get_real_time("%Y%m%d000000", time_range_param)
            shell_origin = '${%dd_pt}' % (time_range)
            print shell_origin
            sql_line = sql_line.lower().replace(shell_origin, real_time)
        return sql_line

if __name__ == '__main__':
    pass