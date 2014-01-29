#ifndef __MVM_H__
#define __MVM_H__

#include <stdint.h>
#include <stdbool.h>
#include "queue.h"

#define MAXPLAYER 8

typedef unsigned char mvm_byte;
typedef mvm_byte mvm_idx;
typedef int32_t mvm_int;
typedef int16_t mvm_half;

typedef struct {
    mvm_int fStub; // place holder
} TAsset;

typedef struct {
    mvm_byte fOp;
    union {
        struct {
            mvm_byte fNotUsed[3];
        } uNull;
        struct {
            mvm_idx fFirst;
        } uI;
        struct {
            mvm_idx fFirst;
            mvm_idx fSecond;
        } uII;
        struct {
            mvm_idx fIdx;
            mvm_half fValue;
            //mvm_idx fValue;
        } uIH;
        struct {
            mvm_idx fFirst;
            mvm_idx fSecond;
            mvm_idx fThird;
        } uIII;
    } fData;
} TInst;



enum {
    op_die = 0x00,
    op_dump,
    op_iset,
    op_iadd,
    op_isub,
    op_sub,
    op_jump,
    op_jump_on_doubles,
    op_jump_on_3rd,
    op_jump_on_zero,
    op_jump_on_positive,
    op_jump_on_negative,
    op_cmp,
    op_roll,
    op_turnend,
    op_move_n,
    op_bunkrupt,
    op_get_debt,
    op_next,
    op_land_on,
    op_nop = 0xff,
};

enum {
    reg_zero = 0x00,
    reg_pc,
    reg_r0,
    reg_r1,
    reg_r2,
    reg_r3,
    reg_r4,
    reg_r5,
    reg_r6,
    reg_r7,
    reg_player0_money,
    reg_player1_money,
    reg_player2_money,
    reg_player3_money,
    reg_player4_money,
    reg_player5_money,
    reg_player6_money,
    reg_player7_money,
    reg_player0_pos,
    reg_player1_pos,
    reg_player2_pos,
    reg_player3_pos,
    reg_player4_pos,
    reg_player5_pos,
    reg_player6_pos,
    reg_player7_pos,
    reg_player0_state,
    reg_player1_state,
    reg_player2_state,
    reg_player3_state,
    reg_player4_state,
    reg_player5_state,
    reg_player6_state,
    reg_player7_state,
    reg_player0_go_count,
    reg_player1_go_count,
    reg_player2_go_count,
    reg_player3_go_count,
    reg_player4_go_count,
    reg_player5_go_count,
    reg_player6_go_count,
    reg_player7_go_count,
    reg_active_mask,
    reg_current_player_idx,
    reg_dieA,
    reg_dieB,
    reg_doubles,
    reg_max,
};

extern const char* registernames[];


typedef struct {
    mvm_int fRegister[reg_max];
    TInst* fCode;
    int fCodeLen;
} TVM;

TVM* VM_New(void);
void TVM_Delete(TVM* self);
void TVM_Deadbeaf(TVM* self);

void TVM_Load(TVM* self, TInst* code, int len);
void TVM_Exec(TVM* self, TInst inst);
void TVM_Run(TVM* self);
void TVM_Dump(TVM* self);

#endif

