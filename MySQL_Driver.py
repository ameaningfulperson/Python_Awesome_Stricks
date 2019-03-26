#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import
# -- python protogenesis
# mysql
import pymysql
# os
import sys

# -- customization
from Common_Solution import CommonSolution
from ConfigFile_Parser import TheConfigerParser

# class
class TheMySQLDriver:

    # 实例的构造函数
    # 在构造实例的时候，需要给出MySQL连接需要的信息
    def __init__(self,db_server,db_user,db_passwd,db_schema):

        # variable - 一级
        self.db_server = db_server
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_schema = db_schema

        # display
        #CommonSolution.message_out(type="notify", message_string="服务器： " + db_server)
        #CommonSolution.message_out(type="notify", message_string="用户名：" + db_user)
        #CommonSolution.message_out(type="notify", message_string="密码：" + db_passwd)
        #CommonSolution.message_out(type="notify", message_string="数据库：" + db_schema)

        # variable - 二级
        self.db = self.MySQL_return_db()
        self.cursor = self.MySQL_return_cursor()

        pass

    # 返回数据库连接对象
    def MySQL_return_db(self):

        # variable
        connect_string = ""

        db = pymysql.connect(self.db_server, self.db_user, self.db_passwd, self.db_schema)

        # return
        return db

    # 返回操作数据库的游标对象
    def MySQL_return_cursor(self):

        # variable
        cursor = self.db.cursor(pymysql.cursors.DictCursor)

        # return
        return cursor

    # 关闭数据库的时候，清理数据库的各种资源
    # 1. 会话连接
    def MySQL_close(self):

        # do
        self.db.close()

    # 查询：
    # 查询模式：
    # ALL,      所有记录
    # ONE,      只有一条记录
    # MANY,NUM, 返回多行记录，由调用时指定条目
    def MySQL_select_return_SET(self,string_sql="",running_mode="",lines=0):

        # variable
        result_set = ""

        # do
        try:

            # 执行SQL命令：查询
            self.cursor.execute(string_sql)

            if running_mode == "all":
                result_set = self.cursor.fetchall()

            elif running_mode == "one":
                result_set = self.cursor.fetchone()

            elif running_mode == "many":
                result_set = self.cursor.fetchmany(lines)

            else:
                CommonSolution.message_out(type="error",message_string="指定结果集的获取模式[running_mode]")

        except:

            # variable
            error_info = sys.exc_info()

            # display
            CommonSolution.message_out(type="error", message_string="无法执行SQL")
            print(error_info[0]," : ",error_info[1])

        #finally:

            # 不管成功还是失败，总要关闭数据库会话连接
            #self.MySQL_close()

        # return
        return result_set

    # 查询是否成功
    def MySQL_select_isSuccess(self,result_set):

        # variable
        isSuccess = False

        # do
        if result_set:
            isSuccess = True

        # return
        return isSuccess

    # 执行SQL：增删改
    def MySQL_execute_noSelect(self,string_command):

        # variable
        isSuccess = False

        # do
        try:
            # 执行SQL
            self.cursor.execute(string_command)

            # 数据库：手动提交
            self.db.commit()

            # 修改状态标识
            isSuccess = True

        except:

            # variable
            error_info = sys.exc_info()

            # display
            CommonSolution.message_out(type="error", message_string="无法执行SQL")
            print(error_info[0], " : ", error_info[1])

            # 数据库：回滚操作
            self.db.rollback()

        #finally:

            # 不管成功还是失败，总要关闭数据库会话连接
            #self.MySQL_close()

        # return
        return isSuccess
