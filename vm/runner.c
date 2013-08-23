#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"

TInst test_adding = {0x01, 0x00, 0x0001};

static const char*
test_add(TVM* vm)
{

    vm->fMR[0] = 0;
    TVM_Exec(vm, test_adding);
    if (vm->fMR[0] != 1)
        return __func__;
    return NULL;
}

typedef const char* const_char_p;
typedef const_char_p (*test_vm_case)(TVM* vm);
test_vm_case cases[] = {test_add, };



int
main(int argc, char** argv)
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

