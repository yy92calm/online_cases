#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 异常页面
@CreateTime: 2019-04-23 16:57:06
'''

from flask import render_template
from online_cases import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500