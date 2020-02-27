#!/usr/bin/env python
# coding=UTF-8
'''
@Author: David Yang
@Description: 命令行方式调用用例，并将过程日志存以模块_时间命名储在log文件夹
@CreateTime: 2019-04-25 10:42:03
'''

import shlex, subprocess, time, logging
from threading import Timer
import signal, re, os, platform


class cmd_process:
    def __init__(self,name,cmd,folder,log_folder):
        self.name = name
        self.cmd = cmd
        self.folder = "%s" % folder
        self.log_folder = "%s" % log_folder
        self.timeout = 1200
        #self.is_timeout = False
    
    def __del__(self):
        self.name = None
        self.cmd = None
        self.folder = None
        self.log_folder = None
        self.timeout = None
        #self.is_timeout = None
    
    #计时器回调，用于关闭阻塞或异常进程（linux生效，windows暂无办法）
    def timeout_callback(self,p):
        print "timeout call back"
        print p.pid
        try:
            os.killpg(p.pid,signal.SIGKILL)
        except Exception as error:
            print error

    #命令行调用，输出日志文件
    def run_cmd(self):
        temp_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        outfile = "%s\\%s\\%s_%s_out.log" % (self.log_folder,self.name,self.name,temp_time)
        errfile = "%s\\%s\\%s_%s_err.log" % (self.log_folder,self.name,self.name,temp_time)
        outfile = outfile.replace("\\","/")
        errfile = errfile.replace("\\","/")
        print outfile,errfile
        if not os.path.exists(self.log_folder+"/"+self.name):
            os.mkdir(self.log_folder+"/"+self.name)
        stdout = open(outfile, 'wb')
        stderr = open(errfile, 'wb')
        cmd = shlex.split(self.cmd)
        cwd = self.folder.replace("\\","/")
        print cmd,cwd

        if platform.system().lower() == 'windows':
            p = subprocess.Popen(cmd, stdout=stdout.fileno(), stderr=stderr.fileno(), cwd=cwd, shell=True)
        elif platform.system().lower() == 'linux':
            p = subprocess.Popen(cmd, stdout=stdout.fileno(), stderr=stderr.fileno(), cwd=cwd)
            my_timer = Timer(self.timeout, self.timeout_callback, [p])
            my_timer.start()

        print p.pid
        try:
            while p.poll() == None:
                time.sleep(5)
        finally:
            print "run over"
            if platform.system().lower() == 'linux':
                my_timer.cancel()
            stdout.flush()
            stderr.flush()
            stdout.close()
            stderr.close()

        return outfile

if __name__ == "__main__":
    #temp_cmd = cmd_process("client","mvn clean test","..\\cases\\TYRZ_AUTOTEST\\UcmSdk_Test_Smoke","..\\logs")
    temp_cmd = cmd_process("client","dir","..\\cases\\TYRZ_AUTOTEST\\UcmSdk_Test_Smoke","..\\logs")
    temp_cmd.run_cmd()
