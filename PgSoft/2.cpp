#include "stdafx.h"
#include <stdlib.h>
#include <iostream>
#include <complex>
#include <cstring>

using namespace std;

const int MAX_LEN = 30;		
const int MAX_SIZE = 30;

//Priority list
const char priority[][2] = { {'^', 3}, {'*', 2}, {'/', 2}, {'+', 1}, {'-', 1}, {';', 0} };
//if a's priority is higher than b, return true
bool compare_prio(char, char);
//judge
inline bool isNum(char ch) {return (ch >= '0' && ch <= '9');}

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
	Stack() { this->top = 0; }
	char * PushStack(char []);
	char * PopStack(char []);
	char GetTop() const { return this->nStack[this->top - 1][0]; }
};

int main()
{
	char exp[MAX_LEN]{ '\0' }, x[MAX_LEN]{ '\0' };
	char n1[MAX_LEN]{ '\0' }, n2[MAX_LEN]{ '\0' }, op[MAX_LEN]{ '\0' };
	bool cmflag = false;
	Queue expression = Queue();
	Stack NS = Stack(), OS = Stack();
	cout << "\n\tinput a expression:\n\n\t";
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
		}
		if (isNum(exp[0]))
		{
			NS.PushStack(exp);
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

	cout << "\n\tresult is " << x << endl << endl;

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
	sprintf_s(exp, MAX_LEN, "%g", re);
}

Queue::Queue()
{
	this->count = 0;
	this->front = 0;
	this->rear = 0;
}

void preDealexpression(char str[])
{
	char mid[MAX_LEN]{'\0'};
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
	for (int i = 0; i < MAX_LEN; i++)
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
