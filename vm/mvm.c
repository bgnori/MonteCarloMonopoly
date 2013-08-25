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
        case op_roll:
            self->fRegister[reg_dice] = 3;
            break;
        case op_next:
            {
                int p, mask, bits;
                p = self->fRegister[reg_current_player_idx] + 1;
                bits = 1 << p;
                mask = self->fRegister[reg_active_mask];
                while (! (mask & bits)){
                    p++ ;
                    if (p >= MAXPLAYER)
                        p = 0;
                    bits = 1 << p;
                }
                self->fRegister[reg_current_player_idx] = p;
            }
            break;
        default:
            break;
    }
}


