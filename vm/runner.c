#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"

TInst theCode[] = {
    {.fOp=op_nop, {.uNull={{0}}}},
    {.fOp=op_iset, {.uIH={.fIdx=reg_r0, .fValue=0}}},
    {.fOp=op_iset, {.uIH={.fIdx=reg_r1, .fValue=3}}},
    {.fOp=op_nop, {.uNull={{0}}}},
    {.fOp=op_iadd, {.uIH={.fIdx=reg_r0, .fValue=1}}},
    {.fOp=op_cmp, {.uIII={reg_r0, reg_r1, reg_r2}}},
    {.fOp=op_jump_on_positive, {.uIII={reg_r2, 0x0, 3}}},
    {.fOp=op_nop, {.uNull={{0}}}},
    {.fOp=op_dump, },
};

int
main(int argc, const char** argv)
{
    TVM* vm;
    int sz;

    vm = VM_New();
    sz = sizeof(theCode)/sizeof(theCode[0]);

    printf("%d\n", sz);
    TVM_Load(vm, theCode, sz);
    TVM_Run(vm);

    TVM_Delete(vm);
    return 0;
}

