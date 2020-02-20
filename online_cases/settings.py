#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 配置文件 
@CreateTime: 2019-04-23 10:59:17
'''

import os
import sys

from online_cases import app

#sqlite数据库配置
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
cases_folder = os.path.join(os.path.dirname(app.root_path), 'cases')
logs_folder = os.path.join(os.path.dirname(app.root_path), 'logs')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

CSRF_ENABLED = True
SECRET_KEY = '123456yy'
