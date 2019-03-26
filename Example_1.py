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
from Excel_Parser import TheMSExcelParser
from MySQL_Driver import TheMySQLDriver

# variable

# 文件
file_mysql_driver = "config_database.conf"
file_excel_config = "config_excel.conf"

file_excel = u"随便找个Excel写进来吧"

# 数据库
db_mysql=""

# function

# 根据参数文件配置创建数据库连接
def MySQL_return_connect_by_Config():

    # MySQL
    cp_mysql_driver = TheConfigerParser(file_mysql_driver)

    db_server = cp_mysql_driver.getValue_by_section_option(section="mysql", option="db_server")
    db_user = cp_mysql_driver.getValue_by_section_option(section="mysql", option="db_user")
    db_passwd = cp_mysql_driver.getValue_by_section_option(section="mysql", option="db_passwd")
    db_schema = cp_mysql_driver.getValue_by_section_option(section="mysql", option="db_schema")

    obj_mysql = TheMySQLDriver(db_server=db_server,db_user=db_user,db_passwd=db_passwd,db_schema=db_schema)

    # display
    #CommonSolution.message_out(type="notify", message_string="服务器： " + db_server)
    #CommonSolution.message_out(type="notify", message_string="用户名：" + db_user)
    #CommonSolution.message_out(type="notify", message_string="密码：" + db_passwd)
    #CommonSolution.message_out(type="notify", message_string="数据库：" + db_schema)

    # define
    #db_mysql = obj_mysql

    # return
    return obj_mysql

# Excel
def Excel_return_Data_by_Config():

    # variable
    obj_excel = TheMSExcelParser(file_excel=file_excel,file_config=file_excel_config)

    # return
    return obj_excel

# main
if __name__ == "__main__":
    # 获取数据库连接
    db_mysql = MySQL_return_connect_by_Config()

    # 使用数据库连接
    sql_result = db_mysql.MySQL_select_return_SET(string_sql="select user,host from mysql.user",running_mode="many",lines=4)

    # display
    CommonSolution.message_out(type="section::level:1",message_string="MySQL - 结果集")
    print(sql_result)

    # Excel
    obj_excel = Excel_return_Data_by_Config()
    col_data = obj_excel.column_data_one_sheet(sheet_name="BGP",column_name="company_name")
    cell_data = obj_excel.cell_data_by_rowNum_colName(sheet_name="BGP",rowNum=195,colNmae="company_name")

    # display
    CommonSolution.message_out(type="section::level:1",message_string="Excel - 结果集")
    print(col_data)
    print(cell_data)

# finished