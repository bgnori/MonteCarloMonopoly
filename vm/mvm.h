#ifndef __MVM_H__
#define __MVM_H__

#include <stdint.h>

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
    op_nop = 0x00,
    op_iadd,
    op_die = 0xff
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
    reg_player0_pos,
    reg_player1_pos,
    reg_player2_pos,
    reg_player3_pos,
    reg_player4_pos,
    reg_player5_pos,
    reg_player6_pos,
    reg_player7_pos,
    reg_max
};

typedef struct {
    mvm_int fRegister[reg_max];
} TVM;

TVM* VM_New(void);
void TVM_Delete(TVM* self);

void TVM_Exec(TVM* self, TInst inst);

#endif
