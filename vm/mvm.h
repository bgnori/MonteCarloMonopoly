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
};

typedef struct {
    mvm_int fRegister[8];
} TVM;

TVM* VM_New(void);
void TVM_Delete(TVM* self);

void TVM_Exec(TVM* self, TInst inst);


int add(int x, int y);

#endif
