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
    TLoader* loader;


    vm = VM_New();
    loader = Loader_New(argv[1]);
    if (loader!= NULL) {
        TVM_Load(vm, loader->fCode, loader->fCodeLen);
        TVM_Run(vm);
        TVM_Delete(vm);
    }
    TLoader_Delete(loader);
    return 0;
}

