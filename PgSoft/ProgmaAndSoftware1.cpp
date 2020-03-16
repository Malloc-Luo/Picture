// ProgmaAndSoftware1.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "stdlib.h"
#include <iostream>

using namespace std;

const int nMaxSize = 15;	

class LinearList
{
public:
	unsigned Length;   //记录当前长度
	int List[nMaxSize];
	void Sort();
	void Out();
	void Insert(int );
	void Delete(int );
	LinearList();
};


int main()
{
	int opdata;
	LinearList mylist = LinearList();

	cout << "\tinsert a data:\n\n";
	cin >> opdata;
	mylist.Insert(opdata);
	mylist.Out();

	cout << "\tdelete a data:\n\n";
	cin >> opdata;
	mylist.Delete(opdata);
	mylist.Out();

	cin.get();
	cin.get();
	return 0;
}

LinearList::LinearList()
{
	this->Length = 0;
	cout << "\tPlease input your linear list :\n\n";

	for (int i = 0; i < 10; i++)
	{
		cin >> this->List[i];
		this->Length++;
	}
	this->Sort();
	this->Out();
}

void LinearList::Out()
{
	cout << endl;

	for (int i = 0; i < this->Length; i++)
	{
		cout << this->List[i] << " _ ";
	}

	cout << endl;
}

//选择排序算法(Selection sort)
void LinearList::Sort()  
{
	int mid;

	for (int i = 0; i < this->Length - 1; i++)
	{
		for (int j = 0; j < this->Length - 1 - i; j++)
		{
			if (this->List[j] > this->List[j + 1])
			{
				mid = this->List[j];
				this->List[j] = this->List[j + 1];
				this->List[j + 1] = mid;
			}
		}
	}
}

//直接插入到list末尾，而后重新排序
void LinearList::Insert(int n)
{
	if (this->Length >= 15) //if linear list is full
	{
		cout << "\tlinear list is full, fail to inster!\n\n";
		return;
	}

	this->List[this->Length++] = n;
	this->Sort();
}

//依次比对，找到第一个相同数据，以此为基准让后续元素迁移一个单位
void LinearList::Delete(int n)
{
	if (this->Length <= 0) //if linear list is empty
	{
		cout << "\tlinear list is empty, fail to delete!\n\n";
		return;
	}

	for (int i = 0; i < this->Length; i++)
	{
		if (this->List[i] == n)
		{
			for (int j = i; j < this->Length - 1; j++)
			{
				this->List[j] = this->List[j + 1];
			}
			this->Length--;
			return;
		}
	}
	//don` t have data n
	cout << "no data is " << n << ", fail to delete!\n";
}

