#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"
#include "unittest.h"

static TInst inst;

static bool
test_mvm_byte_size(TTestContext* ctx)
{
    return assertEqualInt(1, sizeof(mvm_byte), ctx, "mvm_byte size");
}


static bool
test_mvm_half_size(TTestContext* ctx)
{
    return assertEqualInt(2, sizeof(mvm_half), ctx, "mvm_half size");
}


static bool
test_mvm_int_size(TTestContext* ctx)
{
    return assertEqualInt(4, sizeof(mvm_int), ctx, "mvm_int size");
}


static bool
test_inst_size(TTestContext* ctx)
{
    return assertEqualInt(4, sizeof(TInst), ctx, "TInst size");
}


static bool
test_inst_uNull_size(TTestContext* ctx)
{
    return assertEqualInt(4, sizeof(inst.uNull), ctx, "inst.uNull size");
}


static bool
test_inst_uIH_size(TTestContext* ctx)
{
    return assertEqualInt(4, sizeof(inst.uIH), ctx, "inst.uIH size");
}


static bool
test_inst_uI_size(TTestContext* ctx)
{
    return assertEqualInt(2, sizeof(inst.uI), ctx, "inst.uI size");
}

static bool
test_inst_uII_size(TTestContext* ctx)
{
    return assertEqualInt(3, sizeof(inst.uII), ctx, "inst.uII size");
}

static bool
test_inst_uIII_size(TTestContext* ctx)
{
    return assertEqualInt(4, sizeof(inst.uIII), ctx, "inst.uIII size");
}


TestCase cases[] = {
    test_mvm_byte_size,
    test_mvm_int_size,
    test_mvm_half_size,
    test_inst_size,
    test_inst_uNull_size,
    test_inst_uIH_size,
    test_inst_uI_size,
    test_inst_uII_size,
    test_inst_uIII_size,
};

int
main(int argc, const char** argv)
{
    TTestContext ctx;
    int len;
    
    TTestContext_Init(&ctx);
    len = sizeof(cases)/sizeof(TestCase);
    test_runner((TTestContext*)&ctx, cases, len);
    TTestContext_Clean(&ctx);
    return 0;
}


