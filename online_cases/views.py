#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 视图，用例工程增加、编辑、删除、查看报告 
@CreateTime: 2019-04-23 10:59:23
'''

from flask import flash, redirect, url_for, render_template, request
from datetime import datetime
from online_cases import app, db
from online_cases.models import Project,Record
from online_cases.case_process import cmd_process
from online_cases.case_result import case_result
from online_cases.case_logs_analysis import log_analysis
from online_cases.froms import Project_Form
import threading, codecs, os
from online_cases.settings import cases_folder,logs_folder

#默认页面，127.0.0.1:5000
@app.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

#历史运行记录页面
@app.route('/history', methods=['GET'])
def history():
    func_name = request.args.get('func_name')
    records = Record.query.filter_by(func_name=func_name).order_by(Record.id.desc()).all()
    return render_template('history.html',records=records)

#关于页面
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

#get方式调用脚本
@app.route('/run',methods=['GET'])
def check_case():
    id =  request.args.get('id')
    if check_run_flag(id):
        before_run_case(id)
        t= threading.Thread(target=thread_run_case, args=(id,),name=id)
        t.start()
        return redirect(url_for('index'))
    else:
        return "任务运行中,请稍等"

#查看网页格式报告
@app.route('/report',methods=['GET'])
def show_report():
    func_folder = request.args.get('func_folder')
    report_folder = request.args.get('report_folder')
    file_path = str(cases_folder)+"\\"+str(func_folder)+"\\"+str(report_folder)
    file_path = file_path.replace("\\","/")
    #指向其他报告地址
    if not os.path.exists(file_path):
        return redirect(report_folder)
    #获取设置的HTML报告内容
    with codecs.open(file_path, 'r', encoding='GB2312') as file_html:
        file_html_data = file_html.read()
    file_html.close()
    return file_html_data

#查看log日志报告
@app.route('/log',methods=['GET'])
def show_log():
    log_file = request.args.get('log_file')
    file_path = str(log_file)
    file_path = file_path.replace("\\","/")
    print file_path
    #获取设置的报告内容
    with codecs.open(file_path, 'r', encoding='utf-8') as file_log:
        file_data = file_log.readlines()
    file_log.close()
    #return file_data
    return render_template('log.html',lines=file_data)

#增加项目
@app.route('/add',methods=['GET','POST'])
def add_project():
    project_form = Project_Form()
    if project_form.validate_on_submit():
        func_name = request.form.get("func_name")
        func_folder = request.form.get("func_folder")
        func_command = request.form.get("func_command")
        report_folder = request.form.get("report_folder")
        result_regex = request.form.get("result_regex")
        project = Project(func_name,func_folder,report_folder,func_command,result_regex)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            flash("参数有误或者不完整")
    return render_template('add.html',form = project_form)

#删除项目
@app.route('/del',methods=['GET'])
def del_project():
    id = request.args.get('id')
    project = Project.query.filter_by(id=id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))

#更新项目
@app.route('/update',methods=['GET','POST'])
def update_project():
    id = request.args.get('id')
    project = Project.query.filter_by(id=id).first()
    project_form = Project_Form(func_name=project.func_name,func_folder=project.func_folder,report_folder=project.report_folder,func_command=project.func_command,result_regex=project.result_regex)
    if request.method == "POST":
        project.func_name = request.form.get("func_name")
        project.func_folder = request.form.get("func_folder")
        project.func_command = request.form.get("func_command")
        project.report_folder = request.form.get("report_folder")
        project.result_regex = request.form.get("result_regex")
        #db.session.update(project)
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        return render_template('update.html',form = project_form)

def check_run_flag(id):
    project = Project.query.filter_by(id=id).first()
    if (project.exec_status == 1):
        return False
    elif(project.exec_status == 0):
        return True

#运行前清空数据
def before_run_case(id):
    project = Project.query.filter_by(id=id).first()
    project.exec_status = 1
    project.exec_result = 0
    project.total_cases = None
    project.fail_cases = None
    project.error_cases = None
    project.skip_cases = None
    project.end_time = None
    db.session.commit()

#子线程调用并分析结果
def thread_run_case(id):
    project = Project.query.filter_by(id=id).first()
    print project.func_command,os.path.join(cases_folder,project.func_folder)

    try:
        #temp_cmd = cmd_process(project.func_name,"%s" % project.func_command ,".\\cases\\%s" % project.func_folder,".\\logs")
        project.start_time = datetime.utcnow()
        temp_cmd = cmd_process(project.func_name,"%s" % project.func_command ,os.path.join(cases_folder,project.func_folder),logs_folder)
        outfile = temp_cmd.run_cmd()
        temp_case_result = log_analysis(outfile,project.result_regex)
        case_num = temp_case_result.log_result()
        #temp_case_result = case_result(outfile)
        #case_num,total_time,finish_time = temp_case_result.log_result()

        print case_num

        if (case_num is not None) and len(case_num) >= 4:
            project.total_cases = int(case_num[0])
            project.fail_cases = int(case_num[1])
            project.error_cases = int(case_num[2])
            project.skip_cases = int(case_num[3])
            if int(case_num[1]) > 0 :
                project.exec_result = 2
            elif int(case_num[1]) == 0 :
                project.exec_result = 1
        else:
            project.exec_result = 0


    except Exception,err:
        print err
        project.exec_result = 0


    project.exec_status = 0
    project.end_time = datetime.utcnow()
    project.cost_time = (project.end_time - project.start_time).seconds;
    record = Record(project.func_name,outfile,project.exec_result,project.total_cases,project.fail_cases,project.error_cases,project.skip_cases,project.cost_time)
    db.session.add(record)
    db.session.commit()
