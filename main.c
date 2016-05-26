#include "try_throw.h"

#define FOO_EXCEPTION (1)
#define BAR_EXCEPTION (2)
#define BAZ_EXCEPTION (3)


int
main(int argc, char** argv)
{
    TRY{
        int i = 0;
        printf("In Try Statement\n");
        THROW( BAR_EXCEPTION );
        printf("I do not appear\n");
    }CATCH( FOO_EXCEPTION ){
        printf("Got Foo!\n");
    }CATCH( BAR_EXCEPTION ){
        printf("Got Bar!\n");
    }CATCH( BAZ_EXCEPTION ){
        printf("Got Baz!\n");
    }FINALLY{
        printf("%d\n", i);
        printf("...et in arcadia Ego\n");
    }ETRY;
    return 0;
}

