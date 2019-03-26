#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import
# -- python protogenesis
import configparser

# -- customization
from Common_Solution import CommonSolution

class TheConfigerParser(object):

    # 实例构造函数
    def __init__(self,file_name):

        # variable - 一级
        # 需要解析的配置文件
        self.file_config = file_name

        # variable - 二级
        # 直接根据构造类的时候给的文件路径（文件名）创建ConfigParser对象
        self.obj_ConfigParser = configparser.ConfigParser()

        # do
        # 开始加载目标配置文件内容
        # 格式化字符集，避免出现中文乱码的情况
        self.obj_ConfigParser.read(self.file_config,encoding="utf-8")

        # display
        #CommonSolution.message_out(type="notify",message_string="配置文件：【" + file_name + "】")

    # 根据给的section和option的名字，获取option的值
    def getValue_by_section_option(self,section,option):

        # variable
        result = ""

        # do
        if self.obj_ConfigParser.has_option(section=section,option=option):
            result = self.obj_ConfigParser.get(section=section,option=option)
        else:
            CommonSolution.message_out(type="error",message_string="没有找到指定SECTION的指定OPTION")

        # 判断是否是数字
        if result.isdigit():
            result = eval(result)

        # return
        #return eval(result)
        return result

    # 返回所有section的列表
    def getSection(self):

        # variable
        section_list = self.obj_ConfigParser.sections()

        # return
        return section_list

    # 在指定的section下添加option
    def writeValue_by_section_option(self, section, option, value):

        # do

        self.obj_ConfigParser.set(section=section,option=option,value=value)
        self.obj_ConfigParser.write(open(self.file_config,"w"))
