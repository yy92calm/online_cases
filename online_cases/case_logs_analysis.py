#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 日志结果正则匹配，获取用用例数及时间
@CreateTime: 2020-03-03 11:27:28
'''

import re

class log_analysis:
    def __init__(self, result,regex):
        self.outfile = result
        self.regex = regex

    def __del__(self):
        self.outfile = None
        self.regex = None

    def log_result(self):
        case_num = None
        with open(self.outfile,"rb") as log_file:
            # 解析日志文件获取测试结果
            result = log_file.read()
            case_num_str = re.findall(self.regex, result)
            if len(case_num_str) > 0:
                case_num = case_num_str[0]
                print case_num
                if len(case_num_str) < 4:
                    for i in range(len(case_num),4):
                        case_num.append('0')
            else:
                case_num = ['0','0','0','0']
        return case_num
