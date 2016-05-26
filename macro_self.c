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
int main(int argc, char *argv[])
{
    try{
        throw(1);
    }catch(1){
        printf("1111\n");
    }/*finally{
        printf("finally\n");
        }*/
    endtry;
    return 0;
}

