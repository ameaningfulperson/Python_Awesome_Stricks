#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import
# -- python protogenesis
# mysql
import pymysql
# os
import sys

# paramiko
import paramiko

# -- customization
from Common_Solution import CommonSolution

# Class
class TheLinuxDriver:

    def __init__(self,os_host,os_user,os_passwd,ssh_port):
        # variables - level 1
        self.host = os_host
        self.username = os_user
        self.password = os_passwd
        self.port = int(ssh_port)

        # display
        #print("主机：", self.host)
        #print("端口：", self.port)
        #print("用户：", self.username)
        #print("密码：", self.password)
        #print("")

        # variables - level 2
        self.Obj_Paramiko_Linux = paramiko.SSHClient()

        # do
        # SSH Session
        self.Obj_Paramiko_Linux.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.Obj_Paramiko_Linux.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)

        # SSH FTP
        self.Obj_Transport = paramiko.Transport((self.host,self.port))
        self.Obj_Transport.connect(username=self.username,password=self.password)
        self.Obj_FTP = paramiko.SFTPClient.from_transport(self.Obj_Transport)

    # 执行Linux命令
    def Linux_executeCommand(self,command_string):

        # variable
        #print("Command is: 【"+command_string+"】")

        # do
        stdin, stdout, stderr = self.Obj_Paramiko_Linux.exec_command(command_string)

        string_command_result = ""
        while True:
            line = stdout.readline()
            if line:
                string_command_result += line
            else:
                break

        return string_command_result

    # 向Linux上，上传文件：通过用户名与口令
    def Linux_File_upload(self,local_file,remote_path):

        # do
        self.Obj_FTP.put(localpath=local_file,remotepath=remote_path)

    # 从Linux上，下载文件：通过用户名与口令
    def Linux_File_download(self,local_path,remote_file):

        # do
        self.Obj_FTP.get(remotepath=remote_file,localpath=local_path)

    def SessionClose(self):
        # 操作完成后，清理资源
        self.Obj_Transport.close()
        self.Obj_Paramiko_Linux.close()
