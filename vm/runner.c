#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"

TInst theCode[] = {
    {op_nop, 0x00, 0x00, 0x00},
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
    TVM_Run();

    TVM_Delete(vm);
    return 0;
}

