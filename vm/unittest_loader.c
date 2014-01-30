#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "unittest.h"
#include "loader.h"

#define assertEqualInst(a, b, c, m) _assertEqualInst((a), (b), (c), (m), __LINE__, __func__, __FILE__)

bool _assertEqualInst(const TInst* expected, const TInst* actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename);

bool 
_assertEqualInst(const TInst* expected, const TInst* actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename)
{
    if(expected->uIII.fOp != actual->uIII.fOp){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }

    if(expected->uIII.fFirst != actual->uIII.fFirst){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }

    if(expected->uIII.fSecond != actual->uIII.fSecond){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }

    if(expected->uIII.fThird != actual->uIII.fThird){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }

    return true;
}



static bool
test_null(TTestContext* ctx)
{
    TLoader* loader;
    FILE* stream;
    loader = Loader_New();
    if (!assertNotNull(loader, ctx, "loader is null")) return false;
    if (!assertEqualInt(-1, loader->fCodeLen, ctx, "Unexpected data, not -1 fCodeLen")) return false;
    TLoader_Load(loader, "nullprog");
    stream = loader->fStream;
    if (!assertNull(loader->fCode, ctx, "Unexpected data, not null fCode")) return false;
    if (!assertEqualInt(0, loader->fCodeLen, ctx, "Unexpected data, not 0 fCodeLen")) return false;
    if (!assertNotEqualInt(EOF, ftell(stream), ctx, "Bad Stream state")) return false;
    TLoader_Delete(loader);
    if (!assertEqualInt(EOF, ftell(stream), ctx, "Bad Stream state, post close")) return false;
    printf("test_null\n");
    return true;
};

static bool
test_oneOp(TTestContext* ctx)
{
    TLoader* loader;
    FILE* stream;
    TInst expected;
    expected.uIII.fOp = 0;
    expected.uIII.fFirst = 0;
    expected.uIII.fSecond = 0;
    expected.uIII.fThird = 0;

    loader = Loader_New();
    assert(loader);
    if (!assertNotNull(loader, ctx, "loader is null")) return false;
    TLoader_Load(loader, "oneOp");
    stream = loader->fStream;
    if (!assertNotNull(stream, ctx, "stream is null")) return false;
    if (!assertNotNull(loader->fCode, ctx, "Unexpected data, not null fCode")) return false;
    if (!assertEqualInt(1, loader->fCodeLen, ctx, "Unexpected data, not 0 fCodeLen")) return false;
    if (!assertNotEqualInt(EOF, ftell(stream), ctx, "Bad Stream state")) return false;

    if (!assertEqualInst(&expected, &loader->fCode[0], ctx, "Unexpected Inst, not 0x0")) return false;

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


