# -*- coding: utf-8 -*-

"""读取准备导入数据库的excel文件"""

import xlrd


def row_encode(row_data):
    ret = []
    for data in row_data:
        try:
            data = data.encode('utf-8')
        except AttributeError:
            data = str(int(data))
        ret.append(data)
    return ret


def read_sheet(sheet):
    return [sheet.row_values(i) for i in range(sheet.nrows)]


def read_xls(workbook, sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    return read_sheet(sheet)[1:]
