#include "stdafx.h"
#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
#include<malloc.h>
#include<string.h>

using namespace std;

/*
 * 定义文件结构体
 * 变量包括文件名、文件保护码、打开该文件时的保护码、读写指针、文件长度、指向下一file结构体的指针
 */
typedef struct file
{
	char file_name[20];		//文件名
	bool file_protect[3];	//文件保护码,第一位读，第二位写，第三位执行
	bool open_file_protect[3]; //打开该文件时的保护码,仅在文件打开时有效
	int  read, write;		//读写指针
	int  file_length;		//文件长度
	struct file *next;		//指向下一file结构体的指针
} File;

/*
 * 定义用户与文件的映射结构体
 * 变量包括用户名、指向文件的指针、指向下一个x_map结构体的指针
 */
typedef struct x_map
{
	char userName[20];	//用户名
	File *file;			//指向文件的指针
	struct x_map *next;	//指向下一个x_map结构体的指针
} Map;

/*
 * 定义主文件目录结构体
 * 变量包括文件目录的头指针和尾指针
 */
typedef struct mfd
{
	Map *head, *tail;//头指针和尾指针
} MFD;

/*
 * 定义打开的文件目录结构体
 * 变量包括文件目录的头尾指针、最大容量、目前文件数
 */
typedef struct afd
{
	File *head, *tail;	//头尾指针
	int max_open;		//最大容量
	int current_open;	//目前文件数
	afd();
} AFD;

//进行用户的初始化
void initUser(MFD *mfd);

//进行系统用户的输出
void displayUser(MFD *mfd);

//进行用户的查找
Map * queryUser(char userName[], MFD *mfd);

//进行文件的创建操作
bool createFile(Map *user, char file_name[], bool file_protect[3], int file_length);

//进行文件打开操作
bool openFile(Map *user, char file_name[], AFD *afd, bool open_file_protect[]);

//进行用户文件的显示
void displayUserFile(Map *user);

//进行打开的文件的显示
void displayOpenFile(AFD *afd, Map *user);

//进行文件的读操作
bool readFile(AFD *afd, char file_name[]);

//进行文件的写操作
bool writeFile(AFD *afd, char file_name[]);

//关闭文件
bool closeFile(AFD *&afd, char file_name[]);

//进行文件删除操作
bool deleteFile(Map *&user, char file_name[], AFD *afd);

void dir(MFD * mfd);

///////////////////////////main//////////////////////////////
int main()
{
	MFD * mfd = new MFD;

	if (mfd == NULL)
	{
		exit(0);
	}

	mfd->head = mfd->tail = NULL;
	initUser(mfd);
	displayUser(mfd);

	char userName[20];

	while (true)
	{
		cout << "Please choose user to login : ";
		cin >> userName;

		Map *user = queryUser(userName, mfd);

		if (user == NULL)
		{
			cout << "No such user ! " << endl;
		}
		else
		{
			AFD *afd = new AFD;

			if (afd == NULL) 
			{
				cout << "The memory is not enough ! " << endl;
				exit(0);
			}

			char command[20], file_name[20];
			bool file_protect[3], open_file_protect[3];
			int file_length = 0;

			while (true)
			{
				cout << userName << " >> ";
				cin >> command;
			
				if (strcmp(command, "create") == 0)
				{
					cout << "Please file (file_name file_protect file_length) : ";
					cin >> file_name >> file_protect[0] >> file_protect[1] >> file_protect[2] >> file_length;
					createFile(user, file_name, file_protect, file_length);
					displayUserFile(user);
				}
				else if (strcmp(command, "delete") == 0)
				{
					cout << "Please input the file's name you want to delete : ";
					cin >> file_name;
					deleteFile(user, file_name, afd);
					displayUserFile(user);
				}
				else if (strcmp(command, "open") == 0)
				{
					cout << "Please input the file name you want to open : ";
					cin >> file_name >> open_file_protect[0] >> open_file_protect[1] >> open_file_protect[2];
					openFile(user, file_name, afd, open_file_protect);
					displayOpenFile(afd, user);
				}
				else if (strcmp(command, "dir") == 0)
				{
					dir(mfd);
				}
				else if (strcmp(command, "close") == 0)
				{
					cout << "Please input the file name you want to close : ";
					cin >> file_name;
					closeFile(afd, file_name);
					displayOpenFile(afd, user);
				}
				else if (strcmp(command, "read") == 0)
				{
					cout << "Please input the file you want to read : ";
					cin >> file_name;
					readFile(afd, file_name);
					displayOpenFile(afd, user);
				}
				else if (strcmp(command, "write") == 0)
				{
					cout << "Please input the file you want to write : ";
					cin >> file_name;
					writeFile(afd, file_name);
					displayOpenFile(afd, user);
				}
				else if (strcmp(command, "exit") == 0)
				{
					break;
				}
				else
				{
					cout << "No such command \"" << command << "\"" << endl;
				}
			}
		}
	}
	return 0;
}

/*
 * 初始化用户
 */
void initUser(MFD *mfd)
{
	for (int i = 1; i <= 5; i++)
	{
		Map * m = new Map;

		if (m == NULL)
		{
			exit(0);
		}
		cout << "Please input init user name #" << i << " : ";
		cin >> m->userName;
		m->file = NULL;
		m->next = NULL;
		
		if (mfd->head == NULL)
		{
			mfd->head = mfd->tail = m;
		}
		else
		{
			mfd->tail->next = m;
			mfd->tail = m;
		}
	}
}

/*
 * 展示所有用户
 */
void displayUser(MFD *mfd)
{
	Map *m = mfd->head;
	cout << "user : ";

	while (m)
	{
		cout << m->userName << " ";
		m = m->next;
	}
	cout << endl;
}

/*
 * 检查用户名
 */
Map * queryUser(char userName[], MFD *mfd)
{
	Map *m = mfd->head;
	while (m)
	{
		if (strcmp(userName, m->userName) == 0)
		{
			return m;
		}
		m = m->next;
	}

	return NULL;
}

/*
 * 新建文件
 */
bool createFile(Map *user, char file_name[], bool file_protect[3], int file_length)
{
	File *file = new File;

	if (file == NULL)
	{
		return false;
	}

	strcpy_s(file->file_name, file_name);
	file->file_protect[0] = file_protect[0];
	file->file_protect[1] = file_protect[1];
	file->file_protect[2] = file_protect[2];
	file->file_length = file_length;
	file->read = file->write = 0;
	file->next = NULL;

	if (user->file == NULL)
	{
		user->file = file;
	}
	else
	{
		File *op = user->file, *preOp = NULL;

		while (op)
		{
			if (strcmp(op->file_name, file->file_name) == 0)
			{
				cout << "The file name " << file->file_name
					<< " is already exit ! " << endl;
				return false;
			}
			preOp = op;
			op = op->next;
		}
		preOp->next = file;
	}
	return true;
}

/*
 * 打开文件
 */
bool openFile(Map *user, char file_name[], AFD *afd, bool open_file_protect[])
{
	File *file = afd->head;

	while (file)
	{
		if (strcmp(file_name, file->file_name) == 0)
		{
			cout << "\"" << file_name << "\" is open now! \n";
			return false;
		}
		file = file->next;
	}

	file = user->file;

	while (file)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			break;
		}
		file = file->next;
	}

	if (file)
	{
		File *xfile = new File;

		if (xfile == NULL)
		{
			return false;
		}

		*xfile = *file;

		if (xfile->file_protect[0] >= open_file_protect[0])
		{
			xfile->open_file_protect[0] = open_file_protect[0];
		}
		else
		{
			cout << "no read priority ! " << endl;
			return false;
		}

		if (xfile->file_protect[1] >= open_file_protect[1])
		{
			xfile->open_file_protect[1] = open_file_protect[1];
		}
		else
		{
			cout << "no write priority ! " << endl;
			return false;
		}

		if (xfile->file_protect[2] >= open_file_protect[2])
		{
			xfile->open_file_protect[2] = open_file_protect[2];
		}
		else
		{
			cout << "no excute priority ! " << endl;
			return false;
		}

		xfile->next = NULL;

		if (afd->head == NULL)
		{
			afd->head = afd->tail = xfile;
			afd->current_open += 1;
		}
		else if (afd->current_open < afd->max_open)
		{
			afd->tail->next = xfile;
			afd->tail = xfile;
			afd->current_open += 1;
		}
		else
		{
			cout << "The open file is too many ! " << endl;
			return false;
		}
	}
	else
	{
		cout << "the " << file_name << " is not exit !" << endl;
		return false;
	}

	return false;
}

/*
 * 展示用户信息
 */
void displayUserFile(Map *user)
{
	cout << "The fileList of " << user->userName << endl;
	File *file = user->file;

	while (file)
	{
		cout << file->file_name << " " << file->file_protect[0] << " " << file->file_protect[1] << " " << file->file_protect[2] << " " << file->file_length << endl;
		file = file->next;
	}
}

/* 
 * 展示打开文件的列表
 */
void displayOpenFile(AFD *afd, Map *user)
{
	cout << "The open file of " << user->userName << " : " << endl;
	File *file = afd->head;

	while (file)
	{
		cout << file->file_name << " " << file->file_protect[0] << " " << file->file_protect[1] << " " << file->file_protect[2] << " " << file->file_length << " ";
		cout << "readcout : " << file->read << " writecout : " << file->write << endl;
		file = file->next;
	}
}

/*
 * 读写文件
 */
bool readFile(AFD *afd, char file_name[])
{
	File *file = afd->head;

	while (file)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			if (file->open_file_protect[0])
			{
				file->read++;
				return true;
			}
			else
			{
				cout << "no read priority ! \n" << endl;
				return false;
			}
		}
		file = file->next;
	}

	cout << "no such file ! " << endl;
	return false;
}

bool writeFile(AFD *afd, char file_name[])
{
	File *file = afd->head;
	
	while (file)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			if (file->open_file_protect[1])
			{
				file->write++;
				return true;
			}
			else
			{
				cout << "no write priority ! \n" << endl;
				return false;
			}
		}
		file = file->next;
	}

	cout << "no such file ! " << endl;
	return false;
}

/*
 * 关闭已经打开的文件
 */
bool closeFile(AFD *&afd, char file_name[])
{
	File *&file = afd->head, *preFile = nullptr, *temp = nullptr;

	while (file)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			if (file == afd->tail)
			{
				afd->tail = preFile;
				file = nullptr;
			}
			else if (preFile == nullptr)
			{
				afd->head = file->next;
				file = nullptr;
			}
			else
			{
				temp = preFile->next;
				preFile->next = temp->next;
			}

			afd->current_open--;
			return true;
		}

		preFile = file;
		file = file->next;
	}

	cout << "\"" << file_name << "\"" << "is not opened\n";
	return false;
}

/* 根据文件名删除文件 
 */
bool deleteFile(Map *&user, char file_name[], AFD *afd)
{
	File *&file = afd->head, *prefile = NULL, *temp = NULL;

	while (file != nullptr)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			cout << "\"" << file_name << "\" is opened now, close it frist\n";
			return false;
		}
		file = file->next;
	}

	file = user->file;

	while (file)
	{
		if (strcmp(file->file_name, file_name) == 0)
		{
			if (!file->next)
			{
				file = nullptr;
			}
			else if (prefile == nullptr)
			{
				user->file = file->next;
			}
			else
			{
				temp = prefile->next;
				prefile->next = temp->next;
			}
			return true;
		}

		prefile = file;
		file = file->next;
	}
	return false;
}

afd::afd()
{
	this->current_open = 0;
	this->head = nullptr;
	this->max_open = 5;
	this->tail = nullptr;
}

void dir(MFD * mfd)
{
	Map * map_t = mfd->head;
	File * file_t = nullptr;

	while (map_t)
	{
		file_t = map_t->file;
		cout << map_t->userName << " : " << endl;

		while (file_t)
		{
			cout << "\t" << file_t->file_name << " : " << endl;
			cout << "\t\t" << "protect : " << file_t->file_protect[0] << file_t->file_protect[1] << file_t->file_protect[2] << endl;
			cout << "\t\t" << "file length : " << file_t->file_length << endl;
			file_t = file_t->next;
		}

		if (map_t == mfd->tail)
		{
			break;
		}

		map_t = map_t->next;
	}
}
