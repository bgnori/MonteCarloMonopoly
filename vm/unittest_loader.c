#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"
#include "loader.h"


typedef struct {
    TTestContext* fBase;
    TLoader* fLoader;
} TTestLoader;


static const char*
test_null(TTestContext* ctx)
{
    return NULL;
};

TestCase cases[] = {
    test_null,
};

int
main(int argc, const char** argv)
{
    TTestLoader ctx;
    int len;

    ctx.fLoader = Loader_New("nullprog");
    len = sizeof(cases)/sizeof(TestCase);

    test_runner((TTestContext*)&ctx, cases, len);

    TLoader_Delete(ctx.fLoader);
    return 0;
}


