# -*- coding: utf-8 -*-

'''
\t欢迎使用学委助手！
如果想更新学生信息数据: 请先删除该文件相同目录下 stuinfo.db 文件，然后再次启动程序
'''

import os
import re
from readxls import init

tips = '''tips:  可以按照你输入的模板改名，模板的格式:  
        object1 + object2 + object3 + .. + option_object + ..
        例如输入一个模板: 
            班级 + 姓名 + 学号 + .doc + .docx
        其中的 姓名(NAME, name), 学号(ID, id), 座位(SEAT, seat), 班级(CLASS, class)为保留关键字
        输入这些关键字之后会自动替换为相关内容。当然，也可以是自定义内容
        option_object为文件扩展名，如  .pptx  .pdf 等，用于筛选此类文件改名
        模板中可以包含任意个参数，但必须包含 姓名 和至少一个文件扩展名(文件扩展名可以以任意顺序置于任意位置)
        '''

__author__ = 'yuqi'
__version = '3.0'

#文件扩展名
exName = []
#输入模板
template = []
#标准模板
stdTemplate = []

Class = ''

#记录当前运行目录
path = os.getcwd()
#获取先前目录
prpath = ''

try:
    with open('Rename.bat', 'r') as f:
        prpath = os.path.split(f.read())[0]
except IOError:
    prpath = path
finally:
    os.chdir(prpath)

try:
    with open('INI.stu', 'r') as f:
        Class = f.readline()
except :
    Class = input('你的班级(如自动化1801或者自1801): ')
    print('如果要修改班级名请用记事本打开目录下 INI.stu 进行修改，或者删掉该文件')
    with open('INI.stu', 'w') as f:
        f.write(Class)

print(__doc__)
#初始化
Stus = init()


#获取Stus中学生姓名
def getName():
    return [stu['name'] for stu in Stus if stu['seat'] != '0']

def noyourfile():
    nl = getName()
    if len(nl) == 0:
        print('\n都交了\n')
        return
    print('\n还有%d位同学没交\n'% len(nl), nl)


#获取命名模板，返回一个list
def getTemplate(t):
    return re.split(r'\s*\+\s*', t)

def getform(t):
    if t in ('姓名', 'name', 'NAME'):
        return 'name'
    elif t in ('学号', 'id', 'ID'):
        return 'id'
    elif t in ('座位', 'seat', 'SEAT'):
        return 'seat'
    elif t in ('班级', 'class', 'CLASS'):
        return 'class'
    elif re.match(r'^\.\w+', t):
        exName.append(t)
        return 'ex'
    else:
        return t

def tranTostd(tamp):
    return [getform(t) for t in tamp]

def getFileList(ex):
    return [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1] in ex)]

#检查模板是否合法
def check(t):
    return ('name' in t) and (len(exName) != 0)

#处理模板生成文件名
def genFilename(stu):
    fname = ''
    for t in stdTemplate:
        if t == 'class':
            fname = fname + Class
        elif t in ('name', 'id', 'seat'):
            fname = fname + stu[t]
        elif t != 'ex': 
            fname = fname + t
    return fname


def genBat():
    print('请复制文件目录下Rename.bat使用\n')
    try:
        with open('Rename.bat', 'r'):
            pass
    except:
        path = os.path.abspath('.')
        path = os.path.join(path, 'rename.exe')
        with open('Rename.bat', 'w+') as f:
            f.write(path)


if __name__ == '__main__':

    print(tips)
    #切回当前目录
    os.chdir(path)
   
    template = getTemplate(input('输入模板:\n'))
    stdTemplate = tranTostd(template)
    
    if check(stdTemplate) == False:
        raise Exception('模板中必须包含 姓名 项，且至少有一个扩展名')

    fileList = getFileList(exName)

    for stu in Stus:
        for fn in fileList:
            if fn.find(stu['name']) != -1:
                thisname = genFilename(stu) + '.' + fn.split('.')[1]
                fileList.remove(fn)
                stu['seat'] = '0'
                os.rename(fn, thisname)
                break

    noyourfile()
    #切回之前目录
    os.chdir(prpath)
    genBat()
   
input('\n\npress anyone to continue...')


