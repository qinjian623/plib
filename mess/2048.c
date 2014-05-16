#include <stdlib.h>
#include <stdio.h>

#include "2048.h"

int cell_width = 6;
long score = 1000;
int board[K][K];

long get_score(){
	return score;
}


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
	return 0;
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
	return 0;
}

int can_move_up(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (row != 0 && board[row][col] != 0
		&& board[row - 1][col] == 0){
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
	if (col != 0 && board[row][col-1]==0
	    &&board[row][col] != 0){
		*need_return = true;
		return true;
	}	
}

boolean can_move(direction d){
	switch (d){
	case UP:
		return col_iter(0, 0, can_move_up);
	case DOWN:
		return col_iter(0, 0, can_move_down);
	case RIGHT:
		return row_iter(0, 0, can_move_right);
	case LEFT:
		return row_iter(0, 0, can_move_left);
	default:
		return false;
	}
}

int merge_up(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row+1, col)){
		board[row][col] += board[row+1][col];
		board[row+1][col] = 0;
		score += board[row][col];
		(*i)++;
	}
}

int merge_down(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row+1, col)){
		board[row+1][col] += board[row][col];
		board[row][col] = 0;
		score += board[row+1][col];
		(*i)++;
	}
}

int merge_left(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row, col+1)){
		board[row][col] += board[row][col+1];
		board[row][col+1] = 0;
		score += board[row][col];
		(*j)++;
	}
}

int merge_right(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row, col+1)){
		board[row][col+1] += board[row][col];
		board[row][col] = 0;
		score += board[row][col+1];
		(*j)++;
	}
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

boolean two_cells_can_merge(int row0, int col0,
			    int row1, int col1){
	if (row0 >= K || col0 >= K || row1 >= K || col1 >= K){
		return false;
	}else{
		if (board[row0][col0] != 0 &&
		    board[row0][col0] == board[row1][col1]){
			return true;
		}else{
			return false;
		}
	}
}

int can_merge_up_or_down(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row + 1, col)){
		(*need_return) = true;
		return true;
	}
}
int can_merge_right_or_left(int* i, int* j, boolean* need_return){
	int row = *i;
	int col = *j;
	if (two_cells_can_merge(row, col, row, col + 1)){
		(*need_return) = true;
		return true;
	}
}

boolean can_merge(direction d){
	switch(d){
	case UP:
	case DOWN:
		return col_iter(0, 0, can_merge_up_or_down);
	case LEFT:
	case RIGHT:
		return row_iter(0, 0, can_merge_right_or_left);
	}
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
		col_iter(0, 0, merge_up);
		break;
	case DOWN:
		col_iter(0, 0, merge_down);
		//merge_cells_col(d);
		break;
	case RIGHT:
		row_iter(0, 0, merge_right);
		break;
	case LEFT:
		row_iter(0, 0, merge_left);
		//merge_cells_row(d);
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

boolean loop(direction d){
	boolean cmo = can_move(d);
	boolean cme = can_merge(d);
	
	/* if (!cmo){ */
	/* 	printf("Can't move...\n"); */
	/* } */
	/* if (!cme){ */
	/* 	printf("Can't merge...\n"); */
	/* } */
	if (cmo || cme){
		move(d);
		put_new_number();
	}
	
	if (board_is_full()){
		return false;
	}
	//print_board();
	return true;
}


