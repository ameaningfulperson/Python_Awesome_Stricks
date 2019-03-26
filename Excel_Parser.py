#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import
# -- python protogenesis
import xlrd

# -- customization
from Common_Solution import CommonSolution
from ConfigFile_Parser import TheConfigerParser

# variable
#file_excel = "config_excel.conf"

class TheMSExcelParser:

    # 构造函数
    def __init__(self,file_excel,file_config):
        # variable - 一级
        self.file_excel = file_excel

        # variable - 二级
        self.obj_excel = xlrd.open_workbook(self.file_excel)
        self.list_excel_sheets = self.obj_excel.sheet_names()

        # variable - 三级
        self.cp_excel = TheConfigerParser(file_config)

    # 列

    # 获取一个sheet的一列的值
    def column_data_one_sheet(self,sheet_name,column_name):

        # variable
        sheetData = self.obj_excel.sheet_by_name(sheet_name)
        colId = self.cp_excel.getValue_by_section_option(sheet_name,column_name)

        # do
        colData = sheetData.col_values(int(colId))

        # return
        return colData

    # 单元格
    def cell_data_by_rowNum_colName(self,sheet_name,rowNum,colNmae):

        # variable
        sheetData = self.obj_excel.sheet_by_name(sheet_name)
        colId = self.cp_excel.getValue_by_section_option(sheet_name, colNmae)

        # do
        cellData = sheetData.cell(rowNum,colId)

        # return
        return cellData

    pass
