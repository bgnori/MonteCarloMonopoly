#include <stdlib.h>
#include <stdio.h>
#include "mvm.h"

const char* registernames[] = {
    "reg_zero",
    "reg_pc",
    "reg_r0",
    "reg_r1",
    "reg_r2",
    "reg_r3",
    "reg_r4",
    "reg_r5",
    "reg_r6",
    "reg_r7",
    "reg_player0_money",
    "reg_player1_money",
    "reg_player2_money",
    "reg_player3_money",
    "reg_player4_money",
    "reg_player5_money",
    "reg_player6_money",
    "reg_player7_money",
    "reg_player0_pos",
    "reg_player1_pos",
    "reg_player2_pos",
    "reg_player3_pos",
    "reg_player4_pos",
    "reg_player5_pos",
    "reg_player6_pos",
    "reg_player7_pos",
    "reg_player0_state",
    "reg_player1_state",
    "reg_player2_state",
    "reg_player3_state",
    "reg_player4_state",
    "reg_player5_state",
    "reg_player6_state",
    "reg_player7_state",
    "reg_player0_go_count",
    "reg_player1_go_count",
    "reg_player2_go_count",
    "reg_player3_go_count",
    "reg_player4_go_count",
    "reg_player5_go_count",
    "reg_player6_go_count",
    "reg_player7_go_count",
    "reg_active_mask",
    "reg_current_player_idx",
    "reg_dieA",
    "reg_dieB",
    "reg_doubles",
    "reg_max",
};

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
TVM_Dump(TVM* self)
{
    int i;
    TInst inst;

    printf("Registers: \n");
    for (i = 0 ; i < reg_max; i++){
        printf("%30s: %08x\n", registernames[i], self->fRegister[i]);
    }

    printf("code: \n");
    for (i = 0 ; i < self->fCodeLen; i ++ ){
        inst = self->fCode[i];
        printf("%4d: %04x %04x %04x %04x\n", i, 
                inst.uIII.fOp, 
                inst.uIII.fFirst,
                inst.uIII.fSecond,
                inst.uIII.fThird);
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

static void
TVM_Fetch(TVM* self, TInst* inst, int pc)
{
    *inst = *((TInst*)(&(self->fCode[pc])));
}


void
TVM_Run(TVM* self)
{
    TInst inst;
    while(self->fRegister[reg_pc] < self->fCodeLen){
        TVM_Fetch(self, &inst, self->fRegister[reg_pc]);
        printf("%d %x\n", self->fRegister[reg_pc], inst);
        self->fRegister[reg_pc]+=1;
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
    switch(inst.uNull.fOp) {
        case op_die:
            exit(0);
            break;
        case op_dump:
            TVM_Dump(self);
            break;
        case op_nop:
            break;
        case op_iset:
            self->fRegister[inst.uIH.fIdx] = inst.uIH.fValue;
            break;
        case op_iadd:
            self->fRegister[inst.uIH.fIdx] += inst.uIH.fValue;
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
                // get sallary.
            }
            break;
        case op_goto_jail:
            {
                int pos;
                int i;
                i = self->fRegister[reg_current_player_idx];
                pos = self->fRegister[reg_player0_pos+i];
                self->fRegister[reg_player0_pos+i] = 10; //jail
                self->fRegister[reg_player0_state+i] = 1; //jailed, jail count 1, about to have first time
            }
        case op_jump:
            {
                self->fRegister[reg_pc] = inst.uIH.fValue;
            }
            break;
        case op_jump_on_doubles:
            if (self->fRegister[reg_dieB] == self->fRegister[reg_dieA]){
                self->fRegister[reg_pc] = inst.uIH.fValue;
            }
            break;
        case op_jump_on_3rd:
            if (self->fRegister[reg_player0_state + self->fRegister[reg_current_player_idx]] == 3){
                self->fRegister[reg_pc] = inst.uIH.fValue;
            }
            break;
        case op_cmp:
            {
                int x, y, dst;
                x = self->fRegister[inst.uIII.fFirst];
                y = self->fRegister[inst.uIII.fSecond];
                dst = inst.uIII.fThird;

                if ( x == y)
                    self->fRegister[dst] = 0;
                if ( x > y)
                    self->fRegister[dst] = 1;
                if ( x < y)
                    self->fRegister[dst] = -1;
            }
            break;
        case op_jump_on_zero:
            if (self->fRegister[self->fRegister[inst.uIH.fIdx]] == 0){
                self->fRegister[reg_pc] = inst.uIH.fValue;
            }
            break;
        case op_jump_on_positive:
            if (self->fRegister[self->fRegister[inst.uIH.fIdx]] > 0){
                self->fRegister[reg_pc] = inst.uIH.fValue;
            }
            break;
        case op_jump_on_negative:
            if (self->fRegister[self->fRegister[inst.uIH.fIdx]] < 0){
                self->fRegister[reg_pc] = inst.uIH.fValue;
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


