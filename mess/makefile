love: 2048ui.o 2048.o
	gcc -g -std=c99 -o 2048 2048ui.o 2048.o -lncurses
	rm *.o
	echo "ALL DONE!!!!\n"
2048ui.o: 2048ui.c
	gcc -g -std=c99 -c 2048ui.c
2048.o:2048.h 2048.c
	gcc -g -std=c99 -c 2048.c

