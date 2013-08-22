#ifndef __MVM_H__
#define __MVM_H__

#include <stdint.h>

typedef char mvm_char;
typedef int16_t mvm_int;

typedef struct {
    mvm_int fStub; // place holder
} TAsset;

typedef struct {
    mvm_char fOp;
    mvm_char fReg;
    mvm_int fValue;
} TInst;

typedef struct {
    mvm_int fMR[8]; //money register
    TAsset* fAR[8]; //asset register
    mvm_char fSrcR; //source Register
    mvm_char fDstR; //destination Register
    mvm_char fDicR[2]; //Dice Register
    mvm_int fAmount; //Amount R
} TVM;

TVM* VM_New(void);
void TVM_Delete(TVM* self);

void TVM_Exec(TVM* self, TInst inst);


int add(int x, int y);

#endif
