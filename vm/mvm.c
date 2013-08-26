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

static
int
die(void)
{
    int static r = 0; // stab
    r = (r + 1) % 6;
    return r;
}


void
add_byte_2_reg(int* reg, mvm_byte add, int at)
{
    *((mvm_byte*)reg + at) = add;
}

void
and_byte_2_reg(int* reg, mvm_byte mask, int at)
{
    *((mvm_byte*)reg + at) &= mask;
}

void
TVM_Progress(TVM* self)
{
    TInst inst;
    TVM_Exec(self, inst);

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
            self->fRegister[reg_dieA] = die();
            self->fRegister[reg_dieB] = die();
            if(self->fRegister[reg_dieA] == self->fRegister[reg_dieB])
                self->fRegister[reg_doubles] ++;
            break;
        case op_move_n:
            {
                int i;
                int pos;
                int d;
                i = self->fRegister[reg_current_player_idx];
                pos = self->fRegister[reg_player0_pos+i];
                d = self->fRegister[reg_dieA] + self->fRegister[reg_dieB];
                pos = pos + d;
                if (pos >= 40) {
                    pos -= 40;
                    self->fRegister[reg_player0_go_count+i] += 1;
                    self->fRegister[reg_player0_money + i] += 200; // do this with instruction?
                }
                self->fRegister[reg_player0_pos+i] = pos;
                // land on 
                // doubles, 
            }
            break;
        case op_land_on:
            {
                int pos;
                int i;
                i = self->fRegister[reg_current_player_idx];
                pos = self->fRegister[reg_player0_pos+i];
                if (pos == 30){ // go to jail
                    self->fRegister[reg_player0_pos+i] = 10; //jail
                    self->fRegister[reg_player0_state+i] = 1; //jailed
                }
                // fire land event, card, go to jail, property and so on.
            }
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


