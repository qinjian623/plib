#include <stdio.h>
#include <setjmp.h>


#define try { \
        jmp_buf env__; \
        switch(setjmp(env__)){ \
        case 0:
#define catch(x) break; case x:
#define throw(x) longjmp(env__, x)
#define finally break;} 
#define endtry }}
#define endfinally }

void sfunc(void){
    throw(1);
}

int main(int argc, char *argv[])
{
    try{
        printf("asdfasdfasdf hello world\n");
        sfunc();
    }catch(3){
        printf("1111\n");
    }finally{
        printf("finally\n");
    }
    endfinally;
    return 0;
}

