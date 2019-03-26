#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import
# -- python protogenesis
import os
import sys

# -- customization

class CommonSolution(object):

    # 实例构造函数
    def __init__(self):
        pass

    # 专门负责对外输出信息的方法
    # 目标：格式化输出
    def message_out(type="", message_string=""):
        # type, 定义输出目标的类型
        # 范围：类
        if type == "class":
            print("ccccccccccccccccccccccccccccc")
            print("msg [class] --> 【" + message_string + "】")
            print("ccccccccccccccccccccccccccccc")
            print("")
            pass

        # 范围：函数
        if type == "def":
            print("ddddddddddddddddddddddddddddd")
            print("msg [def] --> 【" + message_string + "】")
            print("ddddddddddddddddddddddddddddd")
            print("")
            pass

        # 类型：提示 - 为了排错
        if type == "notify":
            print("$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("msg [notify] --> 【" + message_string + "】")
            print("")
            pass

        # 类型：异常 - 为了排错
        if type == "error":
            print("!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("msg [error] --> 【" + message_string + "】")
            print("")
            pass

        # 类型：段落 - 一级
        if type == "section::level:1":
            print(")))))))))))))))))))))))))))))))))))))")
            print("msg [section::lv.1] ---> 【" + message_string + "】")
            print("")
            pass

        # 类型：段落 - 二级
        if type == "section::level:2":
            print("##########################")
            print("msg [section::lv.2] ---> 【" + message_string + "】")
            print("")
            pass

        if type == "normal":
            print("msg [normal] ---> 【" + message_string + "】")
            print("")
            pass

        pass
