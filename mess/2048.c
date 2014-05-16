#include <stdlib.h>
#include <stdio.h>

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

int board[K][K];
int cell_width = 6;

int row_iter(int row_start, int col_start, iter_fun f){
	for (int i = row_start; i < K; ++i){
		for(int j = col_start; j < K; ++j){
			boolean need_return = false;
			int ret = (* f)(&i, &j, &need_return);
			if (need_return == true){
				return ret;
			}
		}
	}
}

int col_iter(int row_start, int col_start, iter_fun f){
	for (int i = col_start; i < K; ++i){
		for(int j = row_start; j < K; ++j){
			boolean need_return = false;
			int ret = (*f)(&j, &i, &need_return);
			if (need_return == true){
				return ret;
			}
		}
	}
}

int can_move_up(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (row != 0 && board[row][col] != 0){
		*need_return = true;
		return true;
	}
}

int can_move_down(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (row != 0 && board[row][col] == 0
	    && board[row-1][col] != 0){
		*need_return = true;
		return true;
	}	
}

int can_move_right(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (col != 0 && board[row][col] == 0
		&& board[row][col - 1] != 0){
		*need_return = true;
		return true;
	}	
}

int can_move_left(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (col != 0 && board[row][col] != 0){
		*need_return = true;
		return true;
	}	
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

boolean can_move(direction d){
	switch (d){
	case UP:
		return col_iter(0, 0, can_move_up);
	case DOWN:
		return col_iter(0, 0, can_move_down);
		//return can_move_col(d);
	case RIGHT:
		return row_iter(0, 0, can_move_right);
	case LEFT:
		return row_iter(0, 0, can_move_left);
		//return can_move_row(d);
	default:
		return false;
	}
}
boolean can_merge(direction d){
	
}
int print_board_f(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (col == 0){
		for (int k = 0; k < K; ++k){
			printf("|------");
		}
		printf("|\n");
	}
	printf("|%5d ", board[row][col]);
	if (col == K-1){
		printf("\n");
	}
	if (row == K-1 && col == K-1){
		for (int k = 0; k < K; ++k){
			printf("|------");
		}
		printf("|");
	}
	return 0;
}

void print_board(){
	printf ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	row_iter(0, 0, print_board_f);
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
				j++;
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
				j++;
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
				j--;
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
				j--;
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







boolean is_full_f(int* i, int* j, boolean* need_return){
	if (board[*i][*j] == 0){
		(*need_return) = true;
		return false;
	}
	if ((*i) == (*j) && (*i) == (K -1)){
		(*need_return) = true;
		return true;
	}
}

boolean board_is_full(){
	return row_iter(0, 0, is_full_f);
}



boolean move(direction d){
	fill_empty_cells(d);
	merge_cells(d);
	fill_empty_cells(d);
	return true;
}


direction get_key(){
	int c = getchar();
	c = getchar();
	c = getchar();
	printf("%d\n", c);
	while(1){
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
			continue;
		}
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
	boolean moved = move(d);
	if (!moved){
		return true;
	}
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
