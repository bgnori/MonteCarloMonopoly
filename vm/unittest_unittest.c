
#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"





TestCase cases[] = {};
int
main(int argc, const char** argv)
{
    TTestContext ctx;
    int len;

    TTestContext_Init(&ctx);
    len = sizeof(cases)/sizeof(TestCase);
    test_runner(&ctx, cases, len);
    TTestContext_Clean(&ctx);
    return 0;
}

