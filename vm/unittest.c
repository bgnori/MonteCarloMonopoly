#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"


int
test_runner(TTestContext* ctx, const TestCase* cases, int count)
{
    int i;
    TestCase t;
    const_char_p name;

    for(i=0; i< count; i++){
        t = cases[i];
        name = t(ctx);
        if(name){
            printf("!\n");
            printf("fail, %s\n", name);
            ctx->fOnFail;
            break;
        }else{
            printf(".");
        }
    }
}
