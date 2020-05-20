#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <memory.h>
#include <conio.h>
#include <dir.h>

typedef struct
{
    unsigned * front;
    unsigned * back;
    int f;
    int b;
}Ticket;

Ticket * generate_number(int f, int b);

struct tm get_time();

void timestamp();

int findin(unsigned * array, int len, int n);

void print_number(Ticket * m);

void sort_number(Ticket * m);

int write_into_txt(Ticket * m);

unsigned expection(int f, int b, int g);

char * readAll(long * f_size);

void writeAll(char * buff, long f_size);

int main()
{
    int frontN = 0, backN = 0, groupN = 0;
    long f_size = 0;   /*文件长度*/
    char cmd = 0, * text_buff = readAll(& f_size);
    char * current_path;

    printf("\n\tdefault or self setting?(d/s)\n\t: ");
    scanf("%c", &cmd);

    if (cmd == 'd' || cmd == 'D')
    {
        frontN = 5;
        backN = 2;
        groupN = 3;
    }
    else
    {
        printf("\n\tFront :");
        scanf("%d", &frontN);
        printf("\n\tBack : ");
        scanf("%d", &backN);
        printf("\n\tGroup: ");
        scanf("%d", &groupN);

        frontN = (frontN >= 5 && frontN <= 35) ? frontN : 5;
        backN = (backN >= 2 && backN <= 12) ? backN : 2;
        groupN = (groupN > 0) ? groupN : 1;
    }

    timestamp();

    for (int i = 0; i < groupN; ++i)
    {
        Ticket * m = generate_number(frontN, backN);
        print_number(m);
        write_into_txt(m);
        free(m);
    }
    unsigned money = expection(frontN, backN, groupN);

    FILE * f = fopen("ticket.txt", "a+");
    fprintf(f, "\n\n\t需要花费%d元", 2 * money);
    fclose(f);

    if (text_buff != NULL)
    {
        writeAll(text_buff, f_size);
        free(text_buff);
    }

    printf("\n\n\t需要花费%d元\n\n(按'v'查看文件 ticket.txt中保存的记录)\n\n", 2 * money);
    current_path = getcwd(NULL, 0);

    if (current_path != NULL)
    {
        printf("已计入文件至%s\\ticket.txt\n", current_path);
        free(current_path);
    }
    getchar();

    cmd = getch();
    if (cmd == 'v')
    {
        system("ticket.txt");
    }

    return 0;
}

Ticket * generate_number(int f, int b)
{
    Ticket * m = (Ticket *)malloc(sizeof(Ticket));

    m->front = (unsigned *)malloc(sizeof(int ) * f);
    m->back = (unsigned *)malloc(sizeof(int ) * b);

    memset((void *)m->front, 0, sizeof(int ) * f);
    memset((void *)m->back, 0, sizeof(int ) * b);

    m->f = f;
    m->b = b;

    unsigned * array[] = {m->front, m->back};
    int len[] = {f, b};

    for (int i = 0; i < 2; ++ i)
    {
        int j = 0;
        while (j < len[i])
        {
            srand((unsigned)rand());
            int temp = rand() % (i == 0 ? 35 : 12) + 1;

            if (! findin(array[i], len[i], temp))
            {
                array[i][j] = temp;
                j ++;
            }
        }
    }
    sort_number(m);

    return m;
}

void timestamp()
{
    FILE * f = fopen("ticket.txt", "w");
    struct tm time_now = get_time();
    fprintf(stdout, "\n>%4d-%02d-%02d %02d:%02d:%02d >\n", time_now.tm_year + 1900, time_now.tm_mon + 1, time_now.tm_mday, time_now.tm_hour, time_now.tm_min, time_now.tm_sec);
    fprintf(f, "\n>%4d-%02d-%02d %02d:%02d:%02d >\n", time_now.tm_year + 1900, time_now.tm_mon + 1, time_now.tm_mday, time_now.tm_hour, time_now.tm_min, time_now.tm_sec);
    fclose(f);
}

struct tm get_time()
{
    time_t now = time(NULL);
    return * localtime(& now);
}

/*
 * 找到了返回1，否则返回0
 */
int findin(unsigned * array, int len, int n)
{
    for (int i = 0; i < len; ++i)
    {
        if (array[i] == n)
        {
            return 1;
        }
    }
    return 0;
}

void print_number(Ticket * m)
{
    printf("\n   ");

    for (int i = 0; i < m->f; ++i)
    {
        printf("%02d  ", m->front[i]);
    }

    printf("    ");

    for (int i = 0; i < m->b; ++i)
    {
        printf("%02d  ", m->back[i]);
    }
}

void sort_number(Ticket * m)
{
    unsigned temp;
    unsigned * array[] = {m->front, m->back};
    int len[] = {m->f, m->b};

    for (int k = 0; k < 2; k ++)
    {
        for (int i = 0; i < len[k] - 1; i++)
        {
            int min = i;
            for (int j = i; j < len[k]; j++)
            {
                if (array[k][j] < array[k][min])
                {
                    min = j;
                }
            }
            temp = array[k][i];
            array[k][i] = array[k][min];
            array[k][min] = temp;
        }
    }
}

int write_into_txt(Ticket * m)
{
    FILE * f = fopen("ticket.txt", "a+");

    if (f == NULL)
    {
        return 0;
    }
    fseek(f, 0L, SEEK_END);
    fputc('\n', f);

    for (int i = 0; i < m->f; i++)
    {
        fprintf(f, "%02d  ", m->front[i]);
    }

    fputs("\t", f);

    for (int i = 0; i < m->b; i++)
    {
        fprintf(f, "%02d  ", m->back[i]);
    }
    fclose(f);

    return 1;
}

unsigned expection(int f, int b, int g)
{
    int array[] = {f, b};
    unsigned re = 1;

    for (int i = 0; i < 2; i++)
    {
        int up = 1, down = 1;
        int times = array[i] < 10 ? array[i] - 5 : 5;

        for (int j = 1; j <= times; ++j)
        {
            up *= (array[i] - j + 1);
            down *= j;
        }

        re *= (up / down);
    }

    return re * g;
}

char * readAll(long * f_size)
{
    FILE * f = fopen("ticket.txt", "r+");

    if (f == NULL)
    {
        return NULL;
    }

    fseek(f, 0L, SEEK_END);
    * f_size = ftell(f);

    char * buff = (char *)malloc(sizeof(char) * (* f_size));

    rewind(f);
    fread(buff, sizeof(char), * f_size, f);
    fclose(f);

    return buff;
}

void writeAll(char * text, long f_size)
{
    FILE * f = fopen("ticket.txt", "a+");

    if (f != NULL)
    {
        fwrite(text, sizeof(char), f_size, f);
    }
    else
    {
        return;
    }

    fclose(f);
}
