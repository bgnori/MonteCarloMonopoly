#ifndef __MVM_H__
#define __MVM_H__

#include <stdint.h>
#include <stdbool.h>

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
    op_iadd,
    op_isub,
    op_sub,
    op_doubles,
    op_roll,
    op_turnend,
    op_move,
    op_bunkrupt,
    op_get_debt,
    op_next,
    op_nop = 0xff,
};

enum {
    reg_zero = 0x00,
    reg_player0_money,
    reg_player1_money,
    reg_player2_money,
    reg_player3_money,
    reg_player4_money,
    reg_player5_money,
    reg_player6_money,
    reg_player7_money,
    reg_player0_pos_state,
    reg_player1_pos_state,
    reg_player2_pos_state,
    reg_player3_pos_state,
    reg_player4_pos_state,
    reg_player5_pos_state,
    reg_player6_pos_state,
    reg_player7_pos_state,
    reg_active_mask,
    reg_current_player_idx,
    reg_dice,
    reg_max,
};

typedef struct {
    mvm_int fRegister[reg_max];
} TVM;

TVM* VM_New(void);
void TVM_Delete(TVM* self);

void TVM_Exec(TVM* self, TInst inst);

#endif
