#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 命令行，创建/删除数据库，创建测试数据
@CreateTime: 2019-04-23 10:58:04
'''

import click

from online_cases import app, db
from online_cases.models import Project, Record

#初始化数据库:flask initdb
#删除数据库flask initdb --drop
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')

#创建测试数据
@app.cli.command()
@click.option('--count', default=10, help='Quantity of messages,default is 20.')
def forge(count):
    from faker import Faker
    db.drop_all()
    db.create_all()

    fake = Faker()
    click.echo('Forging test datas...')

    for i in range(count):
        project = Project(
            func_name = "testcase1",
            func_folder = "autotest",
            func_command = "mvn clean test",
            report_folder = "target\\surefire-reports\\emailable-report.html",
        )
        db.session.add(project)
        record = Record(
            func_name="testcase1",
            log_file="autotest_2020-02-25-14-55-41_out.log",
            exec_result=fake.random_int(0, 1),
            total_cases=fake.random_int(0, 9),
            fail_cases=fake.random_int(0, 9),
            error_cases=fake.random_int(0, 9),
            skip_cases=fake.random_int(0, 9),
            end_time=None,
        )
        db.session.add(record)
    db.session.commit()
    click.echo('Created %d fake projects.' % count)