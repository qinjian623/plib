#ifndef HCORE
#define HCORE

#define K 4

typedef int direction;
#define UP 1
#define RIGHT 2
#define LEFT 3
#define DOWN 4

typedef int boolean;
#define true 1
#define false 0

typedef int (*iter_fun)(int*, int*, boolean*);
extern int board[K][K];

void put_new_number();
long get_score();
boolean loop(direction d);
#endif
