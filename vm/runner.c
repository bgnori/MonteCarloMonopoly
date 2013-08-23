#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"


static const char*
test_iadd(TVM* vm)
{
    TInst test_adding;
    test_adding.fOp = op_iadd;
    test_adding.fData.uIH.fIdx = 0x00;
    test_adding.fData.uIH.fValue = 0x0001;

    vm->fRegister[0] = 0;
    TVM_Exec(vm, test_adding);
    if (vm->fRegister[0] != 1)
        return __func__;
    return NULL;
}

typedef const char* const_char_p;
typedef const_char_p (*test_vm_case)(TVM* vm);
test_vm_case cases[] = {test_iadd, };


int
main(int argc, const char** argv)
{
    TVM* vm;
    int i, len;
    const_char_p name;
    test_vm_case t;

    vm = VM_New();
    len = sizeof(cases)/sizeof(test_vm_case);

    for(i = 0; i < len; i++){
        t = cases[i];
        name = t(vm);
        if(name){
            printf("!\n");
            printf("fail, %s\n", name);
        }else{
            printf(".");
        }
    }

    TVM_Delete(vm);
    return 0;
}

