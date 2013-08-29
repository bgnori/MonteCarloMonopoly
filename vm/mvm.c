#include <stdlib.h>
#include <stdio.h>
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
TVM_Deadbeaf(TVM* self)
{
    int i;

    for(i=0; i< reg_max; i++)
        self->fRegister[i] = 0xdeadbeaf;
}

void
TVM_DumpRegs(TVM* self)
{
    int i, v;

    for(i=0; i< reg_max; i++){
        v = self->fRegister[i];
        printf("%d: %x %d\n", i, v, v);
    }
}

static
int
die(void)
{
    int static r = 0; // stab
    r = (r + 1) % 6;
    return r;
}



void TVM_Run(TVM* self)
{
    TInst inst;
    while(self->fRegister[reg_pc] < self->fCodeLen){
        inst = *(TInst*)(&(self->fRegister[reg_pc]));
        TVM_Exec(self, inst);
    }
}

void
TVM_Load(TVM* self, TInst* code, int len)
{
    self->fCode = code;
    self->fCodeLen = len;
}

void
TVM_Exec(TVM* self, TInst inst)
{
    self->fRegister[reg_pc]++;
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
                    self->fRegister[reg_player0_state+i] = 1; //jailed, jail count 1, about to have first time
                }
                // fire land event, card, go to jail, property and so on.
            }
            break;
        case op_jump_on_doubles:
            if (self->fRegister[reg_dieB] == self->fRegister[reg_dieA]){
                self->fRegister[reg_pc] = inst.fData.uIH.fValue;
            }
            break;
        case op_jump_on_3rd:
            if (self->fRegister[reg_player0_state + self->fRegister[reg_current_player_idx]] == 3){
                self->fRegister[reg_pc] = inst.fData.uIH.fValue;
            }
            break;
        case op_cmp:
            {
                int x, y, dst;
                x = self->fRegister[inst.fData.uIII.fFirst];
                y = self->fRegister[inst.fData.uIII.fSecond];
                dst = inst.fData.uIII.fThird;

                if ( x == y)
                    self->fRegister[dst] = 0;
                if ( x > y)
                    self->fRegister[dst] = 1;
                if ( x < y)
                    self->fRegister[dst] = -1;
            }
            break;
        case op_jump_on_zero:
            if (self->fRegister[self->fRegister[inst.fData.uIH.fIdx]] == 0){
                self->fRegister[reg_pc] = inst.fData.uIH.fValue;
            }
            break;
        case op_jump_on_positive:
            if (self->fRegister[self->fRegister[inst.fData.uIH.fIdx]] > 0){
                self->fRegister[reg_pc] = inst.fData.uIH.fValue;
            }
            break;
        case op_jump_on_negative:
            if (self->fRegister[self->fRegister[inst.fData.uIH.fIdx]] < 0){
                self->fRegister[reg_pc] = inst.fData.uIH.fValue;
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


