#include <stdlib.h>
#include <stdio.h>

#include "2048.h"

int cell_width = 6;
long score = 1000;
int board[K][K];

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

long get_score(){
	return score;
}

void next(boolean incremental, int* current){
	if (incremental){
		(*current)++;
	}else{
		(*current)--;
	}
}
boolean boundry(boolean incremental, int current, int boundry){
	if (incremental){
		return current < boundry;
	}else{
		return current > boundry;
	}
}

int row_iter(int row_start, int row_end, int col_start, int col_end, iter_fun f){
	boolean row_incremental = row_start < row_end? true:false;
	boolean col_incremental = col_start < col_end? true:false;
	for (int i = row_start; boundry(row_incremental, i, row_end);
	     next(row_incremental, &i)){
		for(int j = col_start; boundry(col_incremental, j, col_end);
		    next(col_incremental, &j)){
			boolean need_return = false;
			int ret = (* f)(&i, &j, &need_return);
			if (need_return == true){
				return ret;
			}
		}
	}
	return 0;
}

int col_iter(int row_start, int row_end, int col_start, int col_end, iter_fun f){
	int row_incremental = row_start < row_end? true:false;
	int col_incremental = col_start < col_end? true:false;
	for (int i = col_start; boundry(col_incremental, i, col_end);
	     next(col_incremental, &i)){
		for(int j = row_start; boundry(row_incremental, j, row_end);
		    next(row_incremental, &j)){
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
		return col_iter(0, K, 0, K, can_move_up);
	case DOWN:
		return col_iter(0, K, 0, K, can_move_down);
	case RIGHT:
		return row_iter(0, K, 0, K, can_move_right);
	case LEFT:
		return row_iter(0, K, 0, K, can_move_left);
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
	if (two_cells_can_merge(row, col, row-1, col)){
		board[row-1][col] += board[row][col];
		board[row][col] = 0;
		score += board[row-1][col];
		(*i)--;
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
	if (two_cells_can_merge(row, col, row, col-1)){
		board[row][col] += board[row][col-1];
		board[row][col-1] = 0;
		score += board[row][col];
		(*j)--;
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
		return col_iter(0, K, 0, K, can_merge_up_or_down);
	case LEFT:
	case RIGHT:
		return row_iter(0, K, 0, K, can_merge_right_or_left);
	}
}

void merge_cells(direction d){
	switch (d){
	case UP:
		col_iter(0, K, 0, K, merge_up);
		break;
	case DOWN:
		col_iter(0, K, K-1, -1, merge_down);
		break;
	case RIGHT:
		row_iter(0, K, K-1, -1, merge_right);
		break;
	case LEFT:
		row_iter(0, K, 0, K, merge_left);
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
	return row_iter(0, K, 0, K, is_full_f);
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
	if (can_move(d) || can_merge(d)){
		move(d);
		put_new_number();
	}
	
	if (board_is_full()
	    && !can_merge(UP)
	    && !can_merge(DOWN)
	    && !can_merge(LEFT)
	    && !can_merge(RIGHT)
		){
		return false;
	}
	return true;
}
