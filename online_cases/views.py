#!/usr/bin/env python
# coding=UTF-8
'''
@Author: yang zhiwei
@LastAuthor: yang zhiwei
@Description: 视图，用例工程增加、编辑、删除、查看报告 
@CreateTime: 2019-04-23 10:59:23
@LastTime: 2019-05-17 15:20:51
'''

from flask import flash, redirect, url_for, render_template, request
from online_cases import app, db
from online_cases.models import Project
from online_cases.case_process import cmd_process
from online_cases.case_result import case_result
from online_cases.settings import cases_folder
from online_cases.froms import Project_Form
import threading, time, random, codecs, re, os
from online_cases.settings import cases_folder,logs_folder

#默认页面，127.0.0.1:5000
@app.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

#关于页面
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

#get方式调用脚本
@app.route('/run',methods=['GET'])
def check_case():
    id =  request.args.get('id')
    before_run_case(id)
    t= threading.Thread(target=thread_run_case, args=(id,),name=id)
    t.start()
    return redirect(url_for('index'))

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
    #return render_template('report.html',file_path = file_html_data)

#增加项目
@app.route('/add',methods=['GET','POST'])
def add_project():
    project_form = Project_Form()
    if project_form.validate_on_submit():
        func_name = request.form.get("func_name")
        func_folder = request.form.get("func_folder")
        func_command = request.form.get("func_command")
        report_folder = request.form.get("report_folder")
        project = Project(func_name,func_folder,report_folder,func_command)
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
    project_form = Project_Form(func_name=project.func_name,func_folder=project.func_folder,report_folder=project.report_folder,func_command=project.func_command)
    if request.method == "POST":
        project.func_name = request.form.get("func_name")
        project.func_folder = request.form.get("func_folder")
        project.func_command = request.form.get("func_command")
        project.report_folder = request.form.get("report_folder")
        #db.session.update(project)
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        return render_template('update.html',form = project_form)


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
        temp_cmd = cmd_process(project.func_name,"%s" % project.func_command ,os.path.join(cases_folder,project.func_folder),logs_folder)
        outfile = temp_cmd.run_cmd()
        temp_case_result = case_result(outfile)
        case_num,total_time,finish_time = temp_case_result.log_result()
        print case_num,total_time,finish_time

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

        if (finish_time is not None) and len(finish_time) >=1:
            project.end_time = str(finish_time[0])
        else:
            project.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    except Exception,err:
        print err
        project.exec_result = 0
        project.end_time = None
    
    project.exec_status = 0
    db.session.commit()
