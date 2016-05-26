#include <stdio.h>
#include <setjmp.h>

int main(int argc, char *argv[])
{
    {
        jmp_buf env;
        switch(setjmp(env)){
        case 0:
            {   
                // Normal
                int i = 0;
                printf("throw now\n");
                longjmp(env, 2);
            }
            break;
        case 1:
            // Handler
            break;
        case 2:
            // Handler
            printf("Got 2!\n");
            break;
        }
        printf("%d\n", i);
        printf("Finally!\n");
    }
    return 0;
}
