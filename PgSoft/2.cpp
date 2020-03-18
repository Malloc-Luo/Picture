#include "stdafx.h"
#include <stdlib.h>
#include <iostream>
#include <complex>
#include <cstring>

using namespace std;

const int MAX_LEN = 20;		
const int MAX_SIZE = 30;

//Priority list
char priority[][2] = { {'^', 3}, {'*', 2}, {'/', 2}, {'+', 1}, {'-', 1}, {';', 0} };
//if a's priority is higher than b, return true
bool compare_prio(char, char);
//judge
bool isNum(char, int *);

void compute(char *, char *op, char *, char *exp);

void preDealexpression(char[]); //预处理字符串，去掉中间空格，加上分号

class Queue
{
	unsigned front;
	unsigned rear;
	unsigned count;
public:
	char nQueue[MAX_SIZE][MAX_LEN]{ '\0' };
	Queue();
	void InQueue(char[] );
	void OutQueue(char[] );
};

class Stack
{
public:
	char nStack[MAX_SIZE][MAX_LEN]{ '\0' };
	unsigned top;
	Stack();
	char * PushStack(char []);
	char * PopStack(char []);
	char GetTop();
};

int main()
{
	char exp[MAX_LEN]{ '\0' }, x[MAX_LEN]{ '\0' };
	char n1[MAX_LEN]{ '\0' }, n2[MAX_LEN]{ '\0' }, op[MAX_LEN]{ '\0' };
	int num;
	bool cmflag = false;
	Queue expression = Queue();
	Stack NS = Stack(), OS = Stack();
	cin.getline(exp, MAX_LEN);

	preDealexpression(exp); //处理字符串

	//字符串表达式入队
	for (int i = 0; i < MAX_LEN; i++)
	{
		expression.InQueue(&exp[i]);
		exp[i] = '\0';
	}

	OS.PushStack(";");

	for (int i = 0;;i++)
	{
		if (!cmflag)  //如果没有进行出栈则继续出队
		{
			expression.OutQueue(exp);
			cmflag = false;
		}
		if (isNum(exp[0], &num))
		{
			NS.PushStack(exp);
			continue;
		}
		else
		{
			if (compare_prio(exp[0], OS.GetTop()))
			{
				OS.PushStack(exp);
				cmflag = false;
			}
			else if (exp[0] == ';' && OS.top == 1)
			{
				NS.PopStack(x);
				cmflag = false;
				break;
			}
			else
			{
				compute(NS.PopStack(n1), OS.PopStack(op), NS.PopStack(n2), x);
				NS.PushStack(x);
				cmflag = true;
			}
		}
	}

	cout << x << endl;

	system("pause");
	return 0;
}

bool compare_prio(char a, char b)
{
	for (int i = 0; i < 6; i++)
	{
		if (priority[i][0] == a)
		{
			a = priority[i][1];
		}
		if (priority[i][0] == b)
		{
			b = priority[i][1];
		}
	}
	return (a > b);
}

//判断是不是数字，是则true， 否则false且num = NULL
bool isNum(char ch, int *num)
{
	if (ch >= '0' && ch <= '9')
	{
		*num = ch - '0';
		return true;
	}
	else
	{
		num = NULL;
		return false;
	}
}

void compute(char *n1, char *op, char *n2, char *exp)
{
	double re = 0.0;
	double m1 = atof(n1), m2 = atof(n2);

	switch (op[0])
	{
	case '+':	re = m1 + m2;
				break;
	case '-':	re = m1 - m2;
				break;
	case '*':	re = m1 * m2;
				break;
	case '/':	re = m1 / m2;
				break;
	case '^':	re = pow(m1, m2);
				break;
	default:	break;
	}
	sprintf_s(exp, MAX_LEN, "%.4f", re);
}

Queue::Queue()
{
	this->count = 0;
	this->front = 0;
	this->rear = 0;
}

void preDealexpression(char str[])
{
	char mid[30]{'\0'};
	for (int i = 0, j = 0; str[i] != '\0'; i++)
	{
		if (str[i] != ' ')
		{
			mid[j++] = str[i];

			if (str[i + 1] == '\0' && str[i + 1] != ';')  //if dont't have ";", add ";"
			{
				mid[j] = ';';
			}
		}	
	}
	for (int i = 0; i < 20; i++)
	{
		str[i] = mid[i];
	}
}

void Queue::InQueue(char item[])
{
	if (this->count >= MAX_SIZE)
	{
		cout << "\tthe Queue is full, fail to send to queue\n\n";
		return;
	}
//	strcpy_s(this->nQueue[this->rear++], strlen(item) + 1, item);
	this->nQueue[this->rear++][0] = *item;
	this->rear %= MAX_SIZE;
	this->count++; 
}

void Queue::OutQueue(char item[])
{
	if (this->count <= 0)
	{
		cout << "\tthe Queue is empty, fail to delete\n\n";
		return;
	}
	strcpy_s(item, strlen(this->nQueue[this->front]) + 1, this->nQueue[this->front]);
	this->front++;
	this->front %= MAX_SIZE;
	this->count--;
}

Stack::Stack()
{
	this->top = 0;
}

char * Stack::PushStack(char item[])
{
	if (this->top >= MAX_SIZE)
	{
		cout << "\tStack is full, fail to push\n\n";
		return NULL;
	}
	strcpy_s(this->nStack[this->top++], strlen(item) + 1, item);

	return item;
}


char * Stack::PopStack(char item[])
{
	if (this->top <= 0)
	{
		cout << "\tStack is empty, fail to pop\n\n";
		return NULL;
	}
	strcpy_s(item, strlen(this->nStack[this->top - 1]) + 1, this->nStack[this->top - 1]);
	this->top--;

	return item;
}

char Stack::GetTop()
{
	return this->nStack[this->top - 1][0];
}

