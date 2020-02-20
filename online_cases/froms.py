#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 
@CreateTime: 2019-05-05 16:05:22
'''

from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class Project_Form(Form):
    func_name = StringField(u'功能名称',validators=[DataRequired(message=u"功能名称不能为空")])
    func_folder = StringField(u'执行目录',validators=[DataRequired(message=u"目录不能为空")])
    report_folder = StringField(u'报告地址',validators=[DataRequired(message=u"报告地址不能为空")])
    func_command = StringField(u'执行命令',validators=[DataRequired(message=u"执行命令不能为空")])
    submit = SubmitField(u'提交')