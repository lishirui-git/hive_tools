#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-17
# @Author  : 殷帅
from time_util import *
import re
import sys
re_table_name = r'[\s\S]*表名:[\s]*([\w_]+)'  # ([a-zA-Z_]+)
re_table_name_zh = r'[\s\S]*表中文名:[\s]*([\s\S]+)'  # ([a-zA-Z_]+)


re_field_info = re.compile(r'([\s\S][^-]*)([-]+)(.*?)[(](.*?)[)]', re.S)  #最小匹配带着最后的类型的
re_field_info_not_type = re.compile(r'([\s\S][^-]*)([-]+)(.*)', re.S) #　 最小匹配并且用户未定义字段类型的

re_select_from = r'[\s\S]*select([\s\S]*)from[\s\S]*'
re_comment = r'([\s\S]*) --([\s\S]*)[(][\s\S][)]'




re_field_info = re.compile(r'([\s\S][^-]*)([-]+)(.*?)[(](.*?)[)][\s\S]*', re.S)  # 最小匹配带着最后的类型的

strs = ', house_type -- 房屋类型'
#
re_field_info_not_type = re.compile(r'([\s\S][^-]*)([-]+)(.*?)[\n]*', re.S)  # 最小匹配并且用户未定义字段类型的

res = re.findall(re_field_info_not_type, strs)

print res

class HiveSchemaCreate:

    def __init__(self, hive_sql=""):
        """
        类初始化函数
        :param table_name: 表英文名称
        :param hive_sql:
        :param table_name_zh: 表中文名称(可选值)
        """
        self.table_name = ""
        self.table_name_zh = ""
        self.hive_sql = hive_sql
        self.hive_schema = ""
        self.mysql_schema = ""
        self.field_key_info = self.get_field_key_info()
        self.get_table_name()

    @staticmethod
    def get_mysql_default_info(self, field_type):
        """
        获取mysql字段的默认字段信息
        :param field_type:
        :return:
        """
        if 'int' in field_type.lower():
            return " not null default 0"
        if field_type in ["double", "float", "DECIMAL"]:
            return " not null default 0.0"
        if field_type in ['string', 'text', 'blob']:
            return " not null default ''"

    def check_sql_valid(self, hive_sql):
        """
        检测输入mysql的有效性
        :param hive_sql:
        :return: True: valid, False: not Valid
        :except:
        """
        pass

    def get_table_name(self):
        """
         获取表的中文名和英文名字
         :param
         :return: (表英文名,表中文名字)
        """
        try:
            ret = re.match(re_table_name, self.hive_sql, re.M | re.I)  # match 从开头开始匹配
            table_name = ret.groups(1)[0]
        except Exception as e:
            raise ValueError('表的英文名字未正常解析, {}'.format(e) )

        try:
            ret = re.match(re_table_name_zh, self.hive_sql, re.M | re.I)  # match 从开头开始匹配
            print ret
            table_name_zh = ret.groups(1)[0]
        except Exception as err:
            raise ValueError('表的英文名字未正常解析, {}'.format(err))
        self.table_name = table_name
        self.table_name_zh = table_name_zh



    def get_field_key_info(self):
        """
        获取输入hive_sql中非关键信息(字段名称、字段类型、字段备注
        :return: [[字段名称, 字段类型, 字段备注],[]]
        """
        ret = re.match(re_select_from, self.hive_sql, re.M | re.I)  # match 从开头开始匹配
        field_str = str(ret.groups(1))[2:-3]
        field_arr = field_str.split('\\n')
        field_info_ret = []

        for field_info in field_arr:
            field_info = field_info.strip()
            print "field info is " + field_info
            if field_info == '':
                continue
            try:
                field_info_tuple = re.findall(re_field_info, field_info)
                print "tuple is " + field_info_tuple
                # print "field tuple is " + str(field_info_tuple) + '\n'
            except Exception as err:
                try:
                    field_info_tuple = re.findall(re_field_info_not_type, field_info)

                except Exception, e:
                    error_info = '{}, {}数据行异常'.format(e, field_info)
                    raise ValueError(error_info)
            field_info_tuple = field_info_tuple[0]
            print 'tuple is ' + field_info_tuple
            if field_info_tuple == 'FROM(':
                break
            field_name = field_info_tuple[0][:field_info_tuple[0].find(',')]
            field_type = field_info_tuple[3]
            field_comment = field_info_tuple[2]
            field_info_ret.append([field_name, field_type, field_comment])
        return field_info_ret

    def get_field_len(self):
        """
        获取字段个数
        :return: lenth
        """
        return len(self.field_key_info)

    def hive_sql_to_hive_schema(self):
        """
        根据输入的hive_sql生成hive建表语句
        :return: hive_schema
        """
        if self.table_name == '':
            raise ValueError("表格英文名不能为空")
        schema_ret = ""
        field_key_info_arr = self.field_key_info
        for field_index, key_info in enumerate(field_key_info_arr):
            field_name = key_info[0]
            field_type = key_info[1]
            field_comment = key_info[2]
            # print field_comment
            schema_line = "    {} {} {} comment '{}'".format(' ' if field_index == 1 else ',',
                                                         field_name.strip(),
                                                         field_type.strip(),
                                                         field_comment.strip()
                                                           )
            # print schema_line
            schema_ret = schema_ret + '\n' + schema_line

        schema_ret += '\n'
        schema_head = "create external table if not exists '{}' (".format(self.table_name)
        if '.' in self.table_name:
            table_layer = self.table_name.split('.')[0]
            table_name = self.table_name.split('.')[1]
        else:
            table_layer = self.table_name[:self.table_name.find('_')]
            table_name = self.table_name
        schema_tail = """
          )partitioned by (pt string)
          row format delimited 
          fields terminated by '\u0001' 
          collection items terminated by '\u0002' 
          map keys terminated by '\u0003' 
          stored as orc 
          location '/user/bigdata/{}/{}' 
        """.format(table_layer, table_name).strip()
        hive_schema = '{}{}{}'.format(schema_head, schema_ret, schema_tail)
        return hive_schema

    def hive_sql_to_mysql_scheme(self):
        """
        根据输入hive_sql生成mysql建表语句
        :return:
        """
        if self.table_name == '':
            raise ValueError("表格的英文名称不能为空")
        if self.table_name_zh == '':
            raise ValueError("表格的中文名称不能为空")
        schema_ret = ""
        field_key_info_arr = self.field_key_info
        for field_index, key_info in enumerate(field_key_info_arr):
            field_name = key_info[0]
            field_type = key_info[1]
            field_comment = key_info[2]
            schema_ret += '\n    {}{} {} {} comment {}'.format(
                                                        ' ' if field_index == 0 else ',',
                                                        field_name,
                                                        field_type,
                                                        self.get_mysql_default_info(field_type),
                                                        unicode(field_comment, 'utf-8'))

        mysql_head = "CREATE TABLE {} (".format(self.table_name)
        mysql_tail = """\n    ,PRIMARY KEY (`id`)\n) ENGINE=InnoDB CHARSET=utf8mb4 COMMENT '{}'
        """.format(self.table_name_zh)
        return '{} {} {}'.format(mysql_head, schema_ret, mysql_tail)





if __name__ == '__main__':
    sql = ""
    with open('./sample2.sql', 'r') as f:
        hive_sql = f.read().strip().lower()
    print hive_sql
    re_select_from = r'([\s\S]*)select([\s\S]*)from([\s\S]*)'
    ret = re.search(re_select_from, hive_sql)  # match 从开头开始匹配
    field_str = ret.groups(0)[0]

    field_arr = field_str.split('\\n')





    # print re.findall(re_field_info, 'device_id -- \xe8\xae\xbe\xe5\xa4\x87id(string)')
    # print re.findall(re_field_info_not_type,  'device_id -- \xe8\xae\xbe\xe5\xa4\x87id')
    field_info_ret = []
    for field_info in field_arr:
        field_info = field_info.strip()
        print "field info is " + field_info
        if field_info == '':
            continue
        try:
            field_info_tuple = re.findall(re_field_info, field_info)
            field_name = field_info_tuple[0][:field_info_tuple[0].find(',')]
            field_type = field_info_tuple[3]
            field_comment = field_info_tuple[2]
            # print "tuple is " + field_info_tuple
            # print "field tuple is " + str(field_info_tuple) + '\n'
        except Exception as err:
            try:
                field_info_tuple = re.findall(re_field_info_not_type, field_info)
                field_name = field_info_tuple[0][:field_info_tuple[0].find(',')]
                field_type = "string"
                field_comment = field_info_tuple[1]
            except Exception, e:
                error_info = '{}, {}数据行异常'.format(e, field_info)
                raise ValueError(error_info)
        field_info_tuple = field_info_tuple[0]
        # print 'tuple is ' + field_info_tuple
        if field_info_tuple == 'FROM(':
            break
        field_info_ret.append([field_name, field_type, field_comment])



    hive_util = HiveSchemaCreate(sql)
    print hive_util.get_field_key_info()
    #
    sys.exit(0)
    # print hive_util.hive_sql_to_hive_schema()
    # # print hive_util.get_table_name()
    print hive_util.hive_sql_to_mysql_scheme()