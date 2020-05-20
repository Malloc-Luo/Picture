#include "stdafx.h"
#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
#include<malloc.h>
#include<string.h>

using namespace std;

/*
 * �����ļ��ṹ��
 * ���������ļ������ļ������롢�򿪸��ļ�ʱ�ı����롢��дָ�롢�ļ����ȡ�ָ����һfile�ṹ���ָ��
 */
typedef struct file
{
	char file_name[20];		//�ļ���
	bool file_protect[3];	//�ļ�������,��һλ�����ڶ�λд������λִ��
	bool open_file_protect[3]; //�򿪸��ļ�ʱ�ı�����,�����ļ���ʱ��Ч
	int  read, write;		//��дָ��
	int  file_length;		//�ļ�����
	struct file *next;		//ָ����һfile�ṹ���ָ��
} File;

/*
 * �����û����ļ���ӳ��ṹ��
 * ���������û�����ָ���ļ���ָ�롢ָ����һ��x_map�ṹ���ָ��
 */
typedef struct x_map
{
	char userName[20];	//�û���
	File *file;			//ָ���ļ���ָ��
	struct x_map *next;	//ָ����һ��x_map�ṹ���ָ��
} Map;

/*
 * �������ļ�Ŀ¼�ṹ��
 * ���������ļ�Ŀ¼��ͷָ���βָ��
 */
typedef struct mfd
{
	Map *head, *tail;//ͷָ���βָ��
} MFD;

/*
 * ����򿪵��ļ�Ŀ¼�ṹ��
 * ���������ļ�Ŀ¼��ͷβָ�롢���������Ŀǰ�ļ���
 */
typedef struct afd
{
	File *head, *tail;	//ͷβָ��
	int max_open;		//�������
	int current_open;	//Ŀǰ�ļ���
	afd();
} AFD;

//�����û��ĳ�ʼ��
void initUser(MFD *mfd);

//����ϵͳ�û������
void displayUser(MFD *mfd);

//�����û��Ĳ���
Map * queryUser(char userName[], MFD *mfd);

//�����ļ��Ĵ�������
bool createFile(Map *user, char file_name[], bool file_protect[3], int file_length);

//�����ļ��򿪲���
bool openFile(Map *user, char file_name[], AFD *afd, bool open_file_protect[]);

//�����û��ļ�����ʾ
void displayUserFile(Map *user);

//���д򿪵��ļ�����ʾ
void displayOpenFile(AFD *afd, Map *user);

//�����ļ��Ķ�����
bool readFile(AFD *afd, char file_name[]);

//�����ļ���д����
bool writeFile(AFD *afd, char file_name[]);

//�ر��ļ�
bool closeFile(AFD *&afd, char file_name[]);

//�����ļ�ɾ������
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
 * ��ʼ���û�
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
 * չʾ�����û�
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
 * ����û���
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
 * �½��ļ�
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
 * ���ļ�
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
 * չʾ�û���Ϣ
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
 * չʾ���ļ����б�
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
 * ��д�ļ�
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
 * �ر��Ѿ��򿪵��ļ�
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

/* �����ļ���ɾ���ļ� 
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
