#include <stdio.h>
#define K 4


typedef int direction;
#define UP 1
#define RIGHT 2
#define LEFT 3
#define DOWN 4

typedef int boolean;
#define true 1;
#define false 0;

int board[K][K];
int cell_width = 6;

void print_board(){
	for (int i = 0; i < K; ++i){
		for (int j = 0; j < K; ++j){
			printf("|------");
		}
		printf("|\n");
		for (int j = 0; j < K; ++j){
			printf("|%5d ", board[i][j]);
		}
		printf("|\n");
		
	}
	for (int j = 0; j < K; ++j){
		printf("|------");
	}
	printf("|\n");
}

void move(direction d){
}

boolean can_move_col(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = 0; j < K; ++j){
			if (j != 0 && board[j][i] != 0){
				if (d == UP){
					return true;
				}
			}
			if (j != 0 && board[j][i] == 0
			    && board[j - 1][i] != 0){
				if (d == DOWN){
					return true;
				}
			}
		}
	}
	return false;
}

boolean can_move_row(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = 0; j < K; ++j){
			if (j != 0 && board[i][j] != 0){
				if (d == LEFT){
					return true;
				}
			}
			if (j != 0 && board[i][j] == 0
			    && board[i][j - 1] != 0){
				if (d == RIGHT){
					return true;
				}
			}
		}
	}
	return false;	
}

boolean can_move(direction d){
	switch (d){
	case UP:
	case DOWN:
		return can_move_col(d);
	case RIGHT:
	case LEFT:
		return can_move_row(d);
	default:
		return false;
	}
}


direction get_key(){
}

int main(){
	/* char c = getchar(); */
	/* printf("%d\n", c); */
	board[1][1] = 2;
	print_board();

	printf("%d\n", can_move(UP));
	printf("%d\n", can_move(DOWN));
	printf("%d\n", can_move(LEFT));
	printf("%d\n", can_move(RIGHT));
}








