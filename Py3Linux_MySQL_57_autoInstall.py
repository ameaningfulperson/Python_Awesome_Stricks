#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import

# -- python protogenesis
# mysql
import pymysql
# os
import sys

# linux
import paramiko

# -- customization
from Common_Solution import CommonSolution
from ConfigFile_Parser import TheConfigerParser
from Linux_Driver import TheLinuxDriver
from MySQL_Driver import TheMySQLDriver

# variable

# 文件
#file_config_linux="config_linux.conf"

# MySQL

# 主库信息
# current - binlog
#current_binlog_file = ""
# current - pos
#current_pos_id = ""

# class
class mysql_auto_install:

    def __init__(self):

        self.file_config_linux = "config_linux.conf"
        # 主库信息
        # current - binlog
        self.current_binlog_file = ""
        # current - pos
        self.current_pos_id = ""

    # function

    # 对Linux的基本环境做出配置
    def do_linux_config_mysql_install(self,ObjSession,ObjMySQL_Session,mysql_server_id,mysql_isMaster,replication_master_host,mysql_repl_user,mysql_repl_passwd):

        # variable
        # 远端服务器上，MySQL的文件位置
        mysql_path_install_remote = "/software/mysql"
        mysql_file_install_remote = mysql_path_install_remote+"/mysql-percona.tar"

        # do

        # 创建需要的目录结构
        CommonSolution.message_out("normal", message_string="创建目录结构：/{script,software,temp_me,iso}")
        ObjSession.Linux_executeCommand("mkdir /{script/{shell,python},software/{mysql,python},temp_me,iso,backup}")

        # 备份文件：/etc/hosts
        CommonSolution.message_out("normal", message_string="备份文件：/etc/hosts")
        ObjSession.Linux_executeCommand("cp /etc/hosts /backup")

        # 文件：/etc/hosts
        CommonSolution.message_out("normal", message_string="文件：/etc/hosts")
        ObjSession.Linux_File_upload(local_file="linux_file_hosts", remote_path="/etc/hosts")

        # ---> varaible
        string_ip = ObjSession.Linux_executeCommand("ip a | grep -v inet6 | grep inet | grep -v 'host lo' | grep -v 'global virbr' | awk '{print $2}' | cut -d'/' -f1").replace("\n", "")
        string_host = ObjSession.Linux_executeCommand("hostname").replace("\n", "")
        string_record = string_ip+" "+string_host

        # display
        #CommonSolution.message_out("normal", message_string="IP: [" + string_ip + "]")
        #CommonSolution.message_out("normal", message_string="HOST: [" + string_host + "]")

        # ---> do
        ObjSession.Linux_executeCommand("echo \""+string_record+"\" >> /etc/hosts")

        # SELINUX
        CommonSolution.message_out("normal", message_string="SELINUX - 禁用")
        ObjSession.Linux_executeCommand("sed -i '/SELINUX/s/enforcing/disabled/g' /etc/selinux/config")

        # 禁用服务
        # iptables / firewalld
        CommonSolution.message_out("normal", message_string="iptables / firewalld - 禁用")
        ObjSession.Linux_executeCommand("chkconfig firewalld off")

        # 停止
        # iptables / firewalld
        CommonSolution.message_out("normal", message_string="iptables / firewalld - 停止")
        ObjSession.Linux_executeCommand("service firewalld stop")

        # YUM，启用缓存
        CommonSolution.message_out("normal", message_string="YUM - 缓存：启用")
        ObjSession.Linux_executeCommand("sed -i '/keepcache/s/0/1/g' /etc/yum.conf")

        # YUM，配置清华大学YUM源
        CommonSolution.message_out("normal", message_string="YUM/源 - 清华大学")
        ObjSession.Linux_File_upload(local_file="linux_yum_tsinghua",remote_path="/etc/yum.repos.d/tsinghua.repo")

        # YUM，安装RPM包
        CommonSolution.message_out("normal", message_string="YUM - 安装包")
        print(ObjSession.Linux_executeCommand("yum install -y createrepo"))

        # 上传，MySQL安装介质
        CommonSolution.message_out("normal", message_string="MySQL/安装介质 - 上传")
        ObjSession.Linux_File_upload(local_file="software\mysql\Percona-Server-5.7.25-28-rc335905-el7-x86_64-bundle.tar", remote_path=mysql_file_install_remote)

        # 解压，MySQL安装介质
        CommonSolution.message_out("normal", message_string="MySQL/安装介质 - 解压")
        ObjSession.Linux_executeCommand("tar -xf "+mysql_file_install_remote+" -C "+mysql_path_install_remote)

        # MySQL，创建YUM本地源
        CommonSolution.message_out("normal", message_string="MySQL - Create REPO")
        ObjSession.Linux_executeCommand("createrepo "+mysql_path_install_remote)

        # YUM，MySQL本地源
        CommonSolution.message_out("normal", message_string="YUM/源 - 本地")
        ObjSession.Linux_File_upload(local_file="linux_yum_local", remote_path="/etc/yum.repos.d/local.repo")

        # YUM，刷新
        CommonSolution.message_out("normal", message_string="YUM - 刷新")
        ObjSession.Linux_executeCommand("yum makecache")

        # YUM，查看源信息
        CommonSolution.message_out("normal", message_string="YUM - 查看")
        print(ObjSession.Linux_executeCommand("yum repolist"))

        # 安装MySQL，YUM方式
        CommonSolution.message_out("normal", message_string="MySQL - YUM Install")
        ObjSession.Linux_executeCommand("yum install -y Percona-Server-server-57")

        # 备份MySQL配置文件
        CommonSolution.message_out("normal", message_string="MySQL - 配置文件：备份")
        ObjSession.Linux_executeCommand("cp /etc/my.cnf /backup")

        # 修改MySQL的配置
        CommonSolution.message_out("normal",message_string="MySQL - 配置文件：修改")
        ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\# mysql replication' /etc/my.cnf ")
        ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\log-bin=mysql-bin' /etc/my.cnf ")
        ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\relay-log=mysql-relay' /etc/my.cnf ")
        ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\relay_log_purge=off' /etc/my.cnf ")

        # MySQL server_id

        # ---> do
        ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\server-id="+str(mysql_server_id)+"' /etc/my.cnf ")

        # --> display
        print("MySQL【server_id】: ["+str(mysql_server_id)+"]")

        # MySQL is master
        # display
        #print("是否是MySQL复制的主库：", mysql_isMaster)
        #print("")

        if mysql_isMaster=="yes":
            #print("MySQL【角色】：主库")
            ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\# read_only=on' /etc/my.cnf ")

        else:
            #print("MySQL【角色】：从库")
            ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\read_only=on' /etc/my.cnf ")

        # MySQL，设置开机启动
        CommonSolution.message_out("normal", message_string="MySQL - 设置开机启动")
        ObjSession.Linux_executeCommand("chkconfig mysqld on")

        # 启动服务：MySQL
        CommonSolution.message_out("normal", message_string="MySQL - 启动服务")
        ObjSession.Linux_executeCommand("service mysqld start")

        # MySQL，修改口令
        CommonSolution.message_out("normal", message_string="MySQL - 修改口令")

        # --> variable
        string_mysql_passwd_temp = ObjSession.Linux_executeCommand("cat /var/log/mysqld.log | grep 'temporary password' | rev | awk '{print $1}' | rev").replace("\n", "")

        # ---> display
        #print("Temp Password: ["+string_mysql_passwd_temp+"]")
        #print("New Password: [" + ObjMySQL_Session.db_passwd + "]")
        #print("")

        # ---> do
        #ObjSession.Linux_executeCommand("mysqladmin -uroot -p'"+string_mysql_passwd_temp+"' password '"+ObjMySQL_Session.db_passwd+"'")

        # MySQL，主从配置：创建用户
        CommonSolution.message_out("normal", message_string="MySQL - 主从用户：创建")

        string_sql_add_user_repl_1 = "create user '"+mysql_repl_user+"'@'%' identified by '"+mysql_repl_passwd+"'"
        #string_sql_add_user_repl_2 = "grant replication slave on *.* to '"+mysql_repl_user+"'@'%' identified by '"+mysql_repl_passwd+"'"
        string_sql_add_user_repl_2 = "grant replication slave on *.* to '" + mysql_repl_user + "'@'%'"

        #ObjMySQL_Session.MySQL_execute_noSelect(string_command=string_sql_add_user_repl)

        ObjMySQL_Session.MySQL_execute_noSelect(string_command="stop slave")
        ObjMySQL_Session.MySQL_execute_noSelect(string_command="drop user '"+mysql_repl_user+"'@'%'")
        ObjMySQL_Session.MySQL_execute_noSelect(string_command=string_sql_add_user_repl_1)
        ObjMySQL_Session.MySQL_execute_noSelect(string_command="grant replication slave on *.* to 'replme'@'%';")

        # MySQL，配置主从关系
        CommonSolution.message_out("normal", message_string="MySQL - 配置主从关系")

        if mysql_isMaster=="yes":
            #print("MySQL【角色】：主库 - 查看信息")

            # variables an do
            #ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\# read_only=on' /etc/my.cnf ")
            #ObjMySQL_Session.MySQL_select_return_SET(string_sql="show master status",running_mode="all")

            master_binlog_info = ObjMySQL_Session.MySQL_select_return_SET(string_sql="show master status", running_mode="all")[0]

            self.current_binlog_file = master_binlog_info['File']
            self.current_pos_id = master_binlog_info['Position']

            # display
            #print(current_binlog_file," | ",current_pos_id)
            #CommonSolution.message_out("normal", message_string="MySQL - 主库的BINLOG信息是："+current_binlog_file+" | "+current_pos_id)

            #CommonSolution.message_out("normal",
            #                           message_string="MySQL - 主库的BINLOG信息是：" + current_binlog_file + " | " + str(
            #                               current_pos_id))

        else:
            #print("MySQL【角色】：从库")

            # variable and do
            #ObjSession.Linux_executeCommand("sed -i '/\[mysqld_safe\]/i\\read_only=on' /etc/my.cnf ")

            string_change_master = "change master to master_host='"+replication_master_host+"',master_user='"+mysql_repl_user+"',master_password='"+mysql_repl_passwd+"',master_log_file='"+self.current_binlog_file+"',master_log_pos="+str(self.current_pos_id)+";"

            # display
            print("Change To Master is: ["+string_change_master+"]")

            # do
            ObjMySQL_Session.MySQL_execute_noSelect(string_command="stop slave")
            ObjMySQL_Session.MySQL_execute_noSelect(string_command="reset slave all")
            ObjMySQL_Session.MySQL_execute_noSelect(string_command=string_change_master)

            CommonSolution.message_out("normal", message_string="MySQL - 启动从库")
            ObjMySQL_Session.MySQL_execute_noSelect(string_command="start slave")

        #CommonSolution.message_out("normal",
        #                           message_string="MySQL - 主库的BINLOG信息是：" + self.current_binlog_file + " | " + str(self.current_pos_id))

        # 操作完成，关闭资源
        ObjSession.SessionClose()

    # 执行对配置文件的全遍历
    def main_linux(self):
        # variable
        Obj_ConfigParser_Linux = TheConfigerParser(self.file_config_linux)
        sections = Obj_ConfigParser_Linux.getSection()

        #mysql_host_counts = len(sections)
        mysql_server_id = 1

        for section_item in sections:
            # display

            CommonSolution.message_out("section::level:1",message_string=section_item)

            # variable

            # MySQL
            os_host = section_item
            os_user = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="username")
            os_password = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="password")
            os_port = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="ssh_port")

            mysql_user = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item,option="mysql_user").replace("\n", "")
            mysql_passwd = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="mysql_passwd").replace("\n", "")
            mysql_schema = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item,option="schema").replace("\n", "")

            # if MySQL is Master or not
            mysql_repl_master = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="master")

            # where is the Master
            mysql_slavefrom = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="slavefrom")

            mysql_repl_user = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="mysql_repl_user")
            mysql_repl_passwd = Obj_ConfigParser_Linux.getValue_by_section_option(section=section_item, option="mysql_repl_passwd")

            # variable - level2
            ObjSession = TheLinuxDriver(os_host=os_host,ssh_port=os_port,os_user=os_user,os_passwd=os_password)
            ObjMySQL = TheMySQLDriver(db_server=os_host,db_user=mysql_user,db_passwd=mysql_passwd,db_schema=mysql_schema)

            #result = ObjMySQL.MySQL_select_return_SET(string_sql="select user,host from mysql.user",running_mode="all")
            #print(result)

            #ObjMySQL.MySQL_execute_noSelect(string_command="create user adamhuan identified by '';")

            # display
            #print("是否是MySQL复制的主库：",mysql_repl_master)
            #print("")

            # do
            # version -1
            #result=ObjSession.Linux_executeCommand("ifconfig")
            #print(result)

            # version -2
            # 根据循环得到的LINUX信息，执行一些定制化的Linux预配置
            self.do_linux_config_mysql_install(ObjSession,ObjMySQL,mysql_server_id,mysql_repl_master,mysql_slavefrom,mysql_repl_user,mysql_repl_passwd)

            # 自增
            mysql_server_id = mysql_server_id+1

        #Obj_ConfigParser_Linux.writeValue_by_section_option(section="10.158.1.128",option="me",value="allah")

# do

# 入口函数
if __name__ == "__main__":

    # 执行对配置文件的全遍历
    doMySQLInstall = mysql_auto_install()
    doMySQLInstall.main_linux()

# done