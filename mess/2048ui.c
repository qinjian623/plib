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

void init_score_win(){
	score_win = newwin(3, 20, 0, 0);
	box(score_win, 0, 0);
	mvwprintw(score_win, 1, 1, "  Score: %ld", get_score());
	wrefresh(score_win);
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

void display_score(){
	mvwprintw(score_win, 1, 1, "  Score: %ld", get_score());
	wrefresh(score_win);
}

void display_board(){
	for (int i = 0; i < K; ++i){
		for (int j = 0; j < K; ++j){
			int idx = index(board[i][j]);
			WINDOW* win = board_win[i][j];
			wattron(win, COLOR_PAIR(idx)); 
			mvwprintw(win, 0, 0, "%2d", board[i][j]);
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
	getchar();
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
/* 	WINDOW *win = newwin(80, 80, 1, 1); */
/* 	wborder(win, '|', '|', '-', '-', '+', '+', '+', '+'); */
/* 	wrefresh(win); */
/* 	get_key(); */
/* 	for (int i = 1; i < 12; ++i){ */
/* 		wattron(win, COLOR_PAIR(i)); */
/* 		wprintw(win, "ASDFJKL:\n"); */
/* 		wattroff(win, COLOR_PAIR(i)); */
/* 	} */
/* 	wrefresh(win); */
/* 	box(win, 0, 0); */
/* 	wrefresh(win); */
	
/* 	while(1){ */
/* 		direction d = get_key(); */
/* 		switch(d){ */
/* 		case UP: */
/* 			printw("UP\n"); */
/* 			break; */
/* 		case DOWN: */
/* 			printw("DOWN\n"); */
/* 			break; */
/* 		case LEFT: */
/* 			printw("LEFT\n"); */
/* 			break; */
/* 		case RIGHT: */
/* 			printw("RIGHT\n"); */
/* 			break; */
/* 		default: */
/* 			goto L; */
/* 		} */
/* 	} */
	
/* L:	y = getmaxy(stdscr); */
/* 	x = getmaxx(stdscr); */
/* 	printw("%d, %d", y, x); */
/* 	refresh(); */
/* 	getchar(); */

	
/* 	getchar(); */
	endwin();
	return 0;
}







