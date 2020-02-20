#!/usr/bin/env python
# coding=UTF-8
'''
@Author: yang zhiwei
@LastAuthor: yang zhiwei
@Description: 
@CreateTime: 2019-04-23 10:55:34
@LastTime: 2019-05-10 14:07:15
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_nav import Nav
from flask_nav.elements import *

app = Flask('online_cases')
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

nav = Nav()
nav.register_element('top',Navbar(u'测试',
                        View(u'用例','index'),
                        View(u'关于','about'),))
nav.init_app(app)

from online_cases import views, errors, helps