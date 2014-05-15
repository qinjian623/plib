#include <stdlib.h>
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
	printf ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
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
void merge_cells_col(direction d){
	for(int i = 0; i < K; ++i){
		for (int j = 0; j < K - 1; ++j){
			if (board[j][i] == board[j + 1][i]){
				switch(d){
				case UP:
					board[j][i] += board[j+1][i];
					board[j+1][i] = 0;
					j++;
					break;
				case DOWN:
					board[j+1][i] += board[j][i];
					board[j][i] = 0;
					j++;
					break;
				}
			}
		}
	}
}
void merge_cells_row(direction d){
	for(int i = 0; i < K; ++i){
		for (int j = 0; j < K - 1; ++j){
			if (board[i][j] == board[i][j+1]){
				switch(d){
				case LEFT:
					board[i][j] += board[i][j+1];
					board[i][j+1] = 0;
					j++;
					break;
				case RIGHT:
					board[i][j+1] += board[i][j];
					board[i][j] = 0;
					j++;
					break;
				}
			}
		}
	}
}
void merge_cells(direction d){
	switch (d){
	case UP:
	case DOWN:
		merge_cells_col(d);
		break;
	case RIGHT:
	case LEFT:
		merge_cells_row(d);
		break;
	default:
		return;
	}
}
/* TODO 这里的处理比较复杂 */
void fill_empty_cells_up(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = 0, k = 1; k < K; ++k){
			if (board[j][i] != 0){
				j++;
				continue;
			}
			if (board[k][i] != 0){
				board[j][i] = board[k][i];
				board[k][i] = 0;
			}
		}
	}
}
/* TODO 这里的处理比较复杂 */
void fill_empty_cells_left(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = 0, k = 1; k < K; ++k){
			if (board[i][j] != 0){
				j++;
				continue;
			}
			if (board[i][k] != 0){
				board[i][j] = board[i][k];
				board[i][k] = 0;
			}
		}
	}
}
/* TODO 这里的处理比较复杂 */
void fill_empty_cells_down(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = K - 1 , k = K - 2; k >= 0; --k){
			if (board[j][i] != 0){
				j--;
				continue;
			}
			if (board[k][i] != 0){
				board[j][i] = board[k][i];
				board[k][i] = 0;
			}
		}
	}
}
/* TODO 这里的处理比较复杂 */
void fill_empty_cells_right(direction d){
	for (int i = 0; i < K; ++i){
		for(int j = K - 1 , k = K - 2; k >= 0; --k){
			if (board[i][j] != 0){
				j--;
				continue;
			}
			if (board[i][k] != 0){
				board[i][j] = board[i][k];
				board[i][k] = 0;
			}
		}
	}
}

void fill_empty_cells(direction d){
	switch(d){
	case UP:
		fill_empty_cells_up(d);
		break;
	case DOWN:
		fill_empty_cells_down(d);
		break;
	case LEFT:
		fill_empty_cells_left(d);
		break;
	case RIGHT:
		fill_empty_cells_right(d);
		break;
	}
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

void move(direction d){
	merge_cells(d);
	if (can_move(d)){
		fill_empty_cells(d);
	}else{
		return;
	}
}



boolean board_is_full(){
	for (int i = 0; i < K; ++i){
		for (int j = 0; j < K; ++j){
			if (board[i][j] == 0){
				return false;
			}
		}
	}
	return true;
}



direction get_key(){
	int c = getchar();
	c = getchar();
	c = getchar();
	printf("%d\n", c);
	getchar();
	switch(c){
	case 65:
		return UP;
	case 66:
		return DOWN;
	case 67:
		return RIGHT;
	case 68:
		return LEFT;
	default:
		return -1;
	}
}

void put_new_number(){
	while(1){
		int i = rand()%K;
		int j = rand()%K;
		if (board[i][j] == 0){
			int value = rand()%10? 2: 4;
			board[i][j] = value;
			return;
		}
	}
}

boolean loop(){
	direction d = get_key();
	move(d);
	if (board_is_full()){
		return false;
	}else{
		put_new_number();
	}
	print_board();
	return true;
}


int main(){
	for (int i = 0; i < K; ++i){
		board[1][i] = 2;
	}

	print_board();

	/* printf("%d\n", can_move(UP)); */
	/* printf("%d\n", can_move(DOWN)); */
	/* printf("%d\n", can_move(LEFT)); */
	/* printf("%d\n", can_move(RIGHT)); */
	while(1){
		if (!loop()){
			return 0;
		}
	}
	/* merge_cells(LEFT); */
	/* fill_empty_cells(LEFT); */
	/* put_new_number(); */
	/* print_board(); */
	
	/* merge_cells(UP); */
	/* fill_empty_cells(UP); */
	/* put_new_number(); */
	/* print_board(); */

	/* merge_cells(DOWN); */
	/* fill_empty_cells(DOWN); */
	/* print_board(); */

	/* merge_cells(LEFT); */
	/* fill_empty_cells(LEFT); */
	/* print_board(); */
	
	
}
