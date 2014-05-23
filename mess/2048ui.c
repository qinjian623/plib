#include <ncurses.h>
#include <math.h>
#include "2048.h"

extern int board[K][K];
WINDOW* score_win;
WINDOW* board_win[K][K];

int index(int v){
	if (v == 1 || v == 0){
		return 0;
	}
	return 1 + index(v/2);
}

direction get_key(){
	int ch = getch();
	direction ret = -1;
	switch(ch){
	case KEY_LEFT:
		ret = LEFT;break;
	case KEY_RIGHT:
		ret = RIGHT;break;
	case KEY_UP:
		ret = UP;break;
	case KEY_DOWN:
		ret = DOWN;break;
	}
	return ret;
}

void display_score(){
	mvwprintw(score_win, 1, 1, "  Score: %ld", get_score());
	wrefresh(score_win);
}

void init_score_win(){
	score_win = newwin(3, 20, 0, 0);
	box(score_win, 0, 0);
	display_score();
}

void init_board_win(){
	for (int i = 0; i < K; ++i){
		for (int j = 0; j < K; ++j){
			board_win[i][j] = newwin(1, 4, 5 + 2*i, 4*j);
			//box(board_win[i][j], 0, 0);
			wrefresh(board_win[i][j]);
		}
	}
}

void display_board(){
	for (int i = 0; i < K; ++i){
		for (int j = 0; j < K; ++j){
			int idx = index(board[i][j]);
			WINDOW* win = board_win[i][j];
			wattron(win, COLOR_PAIR(idx)); 
			mvwprintw(win, 0, 0, "%4d", board[i][j]);
			wattroff(win, COLOR_PAIR(idx));
			wrefresh(win);
		}
	}
}

void init_board_color(){
	if (has_colors == FALSE){
		endwin();
		return;
	}
	start_color();
	init_pair(0, COLOR_WHITE, COLOR_BLACK);
	init_pair(1, COLOR_RED, COLOR_BLACK);
	init_pair(2, COLOR_YELLOW, COLOR_BLACK);
	init_pair(3, COLOR_GREEN, COLOR_BLACK);
	init_pair(4, COLOR_BLUE, COLOR_BLACK);
	init_pair(5, COLOR_MAGENTA, COLOR_BLACK);
	init_pair(6, COLOR_CYAN, COLOR_BLACK);
	init_pair(7, COLOR_RED, COLOR_YELLOW);
	init_pair(8, COLOR_GREEN, COLOR_YELLOW);
	init_pair(9, COLOR_BLUE, COLOR_YELLOW);
	init_pair(10, COLOR_MAGENTA, COLOR_YELLOW);
	init_pair(11, COLOR_CYAN, COLOR_YELLOW);
}

void init(){
	initscr();
	init_board_color();
	raw();
	keypad(stdscr, TRUE);
	noecho();

	get_key();
	init_board_win();
	init_score_win();
}

void redisplay(){
	display_board();
	display_score();
}

int main(){
	direction d;
	init();
	put_new_number();
	put_new_number();

	while(1){
		redisplay();
		d = get_key();
		if (d < 0){
			break;
		}
		if (!loop(d)){
			break;
		}
	}
	getch();
	endwin();
	printf("Final Score = %ld\n", get_score());
	return 0;
}
