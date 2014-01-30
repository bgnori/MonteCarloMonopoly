
#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"



static bool
test_addmessage(TTestContext* ctx)
{
    TTestContext_AddMessage(ctx, "foo");
    return assertEqualStr("foo", ctx->fMessages[0], ctx, "foo == foo");
}

TestCase cases[] = {
    test_addmessage,
};

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

