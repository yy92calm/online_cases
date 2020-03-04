#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 数据库构造
@CreateTime: 2019-04-23 10:59:02
'''

from datetime import datetime
from online_cases import db

#数据库构造
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    func_name = db.Column(db.String(30))
    func_folder = db.Column(db.String(300))
    report_folder = db.Column(db.String(300))
    func_command = db.Column(db.String(100))
    #0:stop 1:running
    exec_status = db.Column(db.Integer)
    #0:null 1:succ 2:fail
    exec_result = db.Column(db.Integer)
    total_cases = db.Column(db.Integer)
    fail_cases = db.Column(db.Integer)
    error_cases = db.Column(db.Integer)
    skip_cases = db.Column(db.Integer)
    #regex
    result_regex = db.Column(db.String(300))
    #record time
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    cost_time = db.Column(db.String(10))

    def __init__(self,func_name,func_folder,report_folder,func_command,result_regex):
        self.func_name = func_name
        self.func_folder = func_folder
        self.report_folder = report_folder
        self.func_command = func_command
        self.exec_status = 0
        self.exec_result = 0
        self.total_cases = None
        self.fail_cases = None
        self.error_cases = None
        self.skip_cases = None
        self.result_regex = result_regex
        self.start_time = datetime.utcnow()
        self.end_time = datetime.utcnow()
        self.cost_time = None


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    func_name = db.Column(db.String(30))
    log_file = db.Column(db.String(300))
    # 0:null 1:succ 2:fail
    exec_result = db.Column(db.Integer)
    total_cases = db.Column(db.Integer)
    fail_cases = db.Column(db.Integer)
    error_cases = db.Column(db.Integer)
    skip_cases = db.Column(db.Integer)
    record_time = db.Column(db.DateTime)
    cost_time = db.Column(db.String(30))

    def __init__(self, func_name,log_file,exec_result,total_cases,fail_cases,error_cases,skip_cases,cost_time):
        self.func_name = func_name
        self.log_file = log_file
        self.exec_result = exec_result
        self.total_cases = total_cases
        self.fail_cases = fail_cases
        self.error_cases = error_cases
        self.skip_cases = skip_cases
        self.record_time = datetime.utcnow()
        self.cost_time = cost_time
