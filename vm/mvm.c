#include <stdlib.h>
#include "mvm.h"

TVM* 
VM_New(void)
{
    TVM* p;
    p = malloc(sizeof(TVM));
    return p;
}

void
TVM_Delete(TVM* self)
{
    free(self);
}

void
TVM_Exec(TVM* self, TInst inst)
{
    switch(inst.fOp) {
        case op_nop:
            break;
        case op_iadd:
            self->fRegister[inst.fData.uIH.fIdx] += inst.fData.uIH.fValue;
            break;

        default:
            break;
    }
}

