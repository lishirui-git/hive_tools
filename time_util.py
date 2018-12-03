#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def get_real_time(date_format, time_range):
    """
    根据不同的分区范围来获取特定格式的日期
    :param date_format 日期格式
    :param time_range 日期范围
    :return: exg:
    """
    date_info = datetime.datetime.now() - datetime.timedelta(days=time_range)
    format_time = date_info.strftime(date_format)
    return format_time

def cal_timedelta(start_date, end_date, time_format, type='d'):
    """
    计算两个之间的天数间隔
    :param start_date:
    :param end_date:
    :param time_format:
    :param type: 计算类型，包含d(day),m(month),y(year)
    :return:
    """
    start = datetime.datetime.strptime(start_date, time_format)
    end = datetime.datetime.strptime(end_date, time_format)
    if type == 'd':
        return (end - start).days
    if type == 'm':
        pass


def get_format_now(time_format):
    """
    生成当前日期的指定格式
    :param time_format:
    :return:
    """
    return datetime.datetime.strftime(datetime.datetime.now(), time_format)


def get_shell_from_real(date_format, time_info):
    """
    将具体的时间分区转化为shell分区格式
    :param date_format:　日期格式
    :return: time_info 时间内容
    """
    if date_format == '%y%m%d000000':
        pass

    raise ValueError("date_format is not correct")


if __name__ == '__main__':
    the_str = "where pt= '20181111' and first_visit_date='2018-11-11' and dp '20181105000000' '20181105000000'in ('app') and pt = '20181105000000'"