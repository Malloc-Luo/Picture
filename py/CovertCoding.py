# -*- coding: utf-8 -*-

import os, chardet, codecs, re

#目标编码
TargetCoding = 'utf-8'
#当前工作目录
WorkDir = ''
#文件类型，用于筛选的扩展名
FileType = []
#文件列表
FileList = []

#获取当前目录下指定扩展名的所有文件
def Get_File_List(Dir):

	if Dir == '':
		return 

	dirList = [os.path.join(Dir, f) for f in os.listdir(Dir)]
	fileList = [f for f in dirList if os.path.isfile(f) and os.path.splitext(f)[1] in FileType]
	folderList = [f for f in dirList if os.path.isdir(f)]

	FileList.extend(fileList)

	for d in folderList:
		Get_File_List(d)
	


def Covert_Coding_To_Target():

    for filepath in FileList:
        with open(filepath, 'rb') as f:
    	    data = f.read()
    	    codeType = chardet.detect(data)['encoding']

        if codeType not in (TargetCoding, 'ascii'):
            with codecs.open(filepath, 'r', codeType) as f:
                content = f.read()
            with codecs.open(filepath, 'w', TargetCoding) as f:
                f.write(content)
            print(filepath + '\n')

    		

if __name__ == '__main__':

	WorkDir = str(input('input target folder\n\t:'))
	TargetCoding = str(input('target coding(default to utf-8)\n\t:')).lower()
	FileType = re.split(r'\s+', str(input('file type(filename extension, such as .c .h)\n\t:')))
	os.chdir(WorkDir)
	Get_File_List(WorkDir)
	Covert_Coding_To_Target()

	

