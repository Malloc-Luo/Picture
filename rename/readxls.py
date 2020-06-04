# -*- coding: utf-8 -*-

'''
对excel内容格式的要求:
内容分为三列: A 列为学生的实验台号, B列为学生姓名, C列为学号
文档中无标题, 只有这三组数据, 如下示意: 
    |  A  |  B  |  C  |
    +-----+-----+-----+
| 1 |  1  |stu1 |20000|
+---+-----+-----+-----+
| 2 |  2  |stu2 |20001|
author: yuqili
'''

import os
import sqlite3
import xlrd
import time

DB = 'stuinfo.db'

def Get_stu_info():
    pass


def Read_from_xls():
    print(__doc__)
    path = input('输入excel表格路径:\n(可直接将文件拖拽至此，文件名及路径当中不可含有空格):')
    data = xlrd.open_workbook(filename = path)
    info = data.sheet_by_index(0)
    infoList = []
    index = 0
    print('一共', info.nrows, '个同学')

    for index in range(info.nrows):
        value = info.row_values(index)
        infoList.append({'name': value[1], 'id': str(int(value[2])), 'seat': str(int(value[0]))})
        index = index + 1

    return infoList


#写入数据库
def Write_into_DB(infoList: list):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try :
        #创建数据表
        cursor.execute('CREATE TABLE IF NOT EXISTS stu(name VARCHAR(10) PRIMARY KEY, id CHAR(8), seat CHAR(2))')
        #填充数据
        for stu in infoList:
            cursor.execute('INSERT INTO stu(name, id, seat) VALUES (?, ?, ?)', ((stu['name'], stu['ID'], stu['seat'])))
    finally:
        cursor.close()
        conn.commit()
        conn.close()


def Read_from_DB():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    info = []
    try:
        cursor.execute('SELECT * FROM stu')
        info = cursor.fetchall()
    finally:
        cursor.close()
        conn.commit()
        conn.close()
    return info


def init_data():
    infoList = Read_from_xls()
    print(infoList)

    if input('确认无误?(y|n): ') in ('n', 'N', 'NO', 'no', 'No'):
        print('检查excel表格并重试..\n即将关闭..')
        time.sleep(2)
        exit(0)
    Write_into_DB(infoList)
    return infoList
    

def init():
    try:
        with open(DB, 'r') as f:
            pass

        info = Read_from_DB()
        return list(map(lambda item: {'name': item[0], 'id': item[1], 'seat': (item[2])}, info))
    except IOError:
        return init_data()
         
        

if __name__ == '__main__':
    L = init()

    print(L)







