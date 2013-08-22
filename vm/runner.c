#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"


TInst test_adding = {0x01, 0x00, 0x0001};

int
main(int argc, char** argv)
{
    printf("%d\n", add(1, 2));
    TVM* vm;
    vm = VM_New();
    printf("%d\n", vm->fMR[0]);
    TVM_Exec(vm, test_adding);

    printf("%d\n", vm->fMR[0]);
    TVM_Delete(vm);
    return 0;
}


