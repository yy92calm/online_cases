#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 日志结果匹配，获取用用例数及时间
@CreateTime: 2020-03-03 11:27:28
'''

import re
from bs4 import BeautifulSoup


class log_analysis:
    def __init__(self, result,regex):
        self.outfile = result
        self.regex = regex

    def __del__(self):
        self.outfile = None
        self.regex = None

    def log_result(self):
        case_num = None
        total_time = None
        finish_time = None
        for line in open(self.outfile):
            # 解析HTML获取结果
            if "<html" in line:
                soup_string = BeautifulSoup(line, "html.parser")
                case_string = soup_string.find("a").attrs['href']
                name_str = case_string.split("/")[-1]
                succ = name_str.split("_")[3]
                case_num = re.findall(r"\d+\d*", name_str.split("_")[-1])
                case_num.insert(0, '%s' % succ)
                case_num.insert(2, '0')
                case_num.insert(3, '0')
                break
            # 解析日志文件获取测试结果
            result = line.replace(" ", '')
            case_num_str = re.findall(r"Testsrun:(.+?)\n", result)
            if len(case_num_str) > 0:
                case_num = re.findall(r"\d+\d*", case_num_str[0])

            total_time_str = re.findall(r"Totaltime:(.+?)\n", result)
            if len(total_time_str) > 0:
                total_time = re.findall(r"\d+\:+\d*", total_time_str[0])

            finish_time_str = re.findall(r"Finishedat:(.+?)\n", result)
            if len(finish_time_str) > 0:
                finish_time = finish_time_str

        return case_num, total_time, finish_time


if __name__ == "__main__":
    test_string = "Tests run: 1086, Failures: 1041, Errors: 0, Skipped: 45\n"
    test_case = log_analysis(test_string)
    print test_case.log_result()
