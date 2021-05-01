# -*- coding: utf-8 -*-
# 改的更好用了
# 使用方式：
# ① 编码转换
# cvt -f [target folder] -t [file type] -c [target coding]
# ② 帮助
# cvt help 或 cvt -h
#
# for example:
# cvt -f D:\Folder -t .c .h .cpp .hpp -c utf-8

import os, chardet, codecs, re, sys
from functools import reduce

"""
Help Doc
    命令格式 cvt -f [target folder] -t [file type] -c [target coding]
    举例  cvt -f D:\\Folder -t .c .h .cpp .hpp -c utf-8
    注意，必须使用绝对路径，且路径中最好不要有空格
"""

if len(sys.argv) != 1:
    argv = reduce(lambda s1, s2: s1 + ' ' + s2, sys.argv)
else:
    targetfolder = str(input('文件夹路径(Folder path)$ '))
    filetype = str(input('文件扩展名(File extension)$ '))
    targetcoding = str(input('目标编码格式(Target coding)$ '))


print(argv)      