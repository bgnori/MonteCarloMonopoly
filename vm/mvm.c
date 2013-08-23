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
        case 0x00:
            break;
        case 0x01:
            self->fMR[inst.fReg] += inst.fValue;
            break;

        default:
            break;
    }
}

