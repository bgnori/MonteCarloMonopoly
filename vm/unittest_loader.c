#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"
#include "loader.h"



static bool
test_null(TTestContext* ctx)
{
    TLoader* loader;
    FILE* stream;
    loader = Loader_New("nullprog");
    stream = loader->fStream;
    if (!assertNull(loader->fCode, ctx, "Unexpected data, not null fCode")) return false;
    if (!assertEqualInt(0, loader->fCodeLen, ctx, "Unexpected data, not 0 fCodeLen")) return false;
    if (!assertNotEqualInt(EOF, ftell(stream), ctx, "Bad Stream state")) return false;
    TLoader_Delete(loader);
    if (!assertEqualInt(EOF, ftell(stream), ctx, "Bad Stream state, post close")) return false;
    return true;
};

static bool
test_oneOp(TTestContext* ctx)
{
    TLoader* loader;
    FILE* stream;
    loader = Loader_New("oneOp");
    stream = loader->fStream;
    if (!assertNotNull(loader->fCode, ctx, "Unexpected data, not null fCode")) return false;
    if (!assertEqualInt(1, loader->fCodeLen, ctx, "Unexpected data, not 0 fCodeLen")) return false;
    if (!assertNotEqualInt(EOF, ftell(stream), ctx, "Bad Stream state")) return false;
    TLoader_Delete(loader);
    if (!assertEqualInt(EOF, ftell(stream), ctx, "Bad Stream state, post close")) return false;
    return true;
};


TestCase cases[] = {
    test_null,
    test_oneOp,
};

int
main(int argc, const char** argv)
{
    TTestContext ctx;
    TTestContext_Init(&ctx);
    test_runner(&ctx, cases, sizeof(cases)/sizeof(TestCase));
    TTestContext_Clean(&ctx);
    return 0;
}


