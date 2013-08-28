#include <stdlib.h>
#include <stdio.h>

#include "mvm.h"


static const char*
test_iadd(TVM* vm)
{
    TInst inst;
    inst.fOp = op_iadd;
    inst.fData.uIH.fIdx = 0x00;
    inst.fData.uIH.fValue = 0x0001;

    vm->fRegister[0] = 0;
    TVM_Exec(vm, inst);
    if (vm->fRegister[0] != 1)
        return __func__;
    return NULL;
}

static const char*
test_next1(TVM* vm)
{
    TInst inst;
    inst.fOp = op_next;

    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_active_mask] = 1+2+4+8;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_current_player_idx] != 1)
        return __func__;
    return NULL;
}

static const char*
test_next2(TVM* vm)
{
    TInst inst;
    inst.fOp = op_next;

    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_active_mask] = 1+4+8;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_current_player_idx] != 2)
        return __func__;
    return NULL;
}

static const char*
test_next3(TVM* vm)
{
    TInst inst;
    inst.fOp = op_next;

    vm->fRegister[reg_current_player_idx] = 3;
    vm->fRegister[reg_active_mask] = 1+2+4+8;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_current_player_idx] != 0)
        return __func__;
    return NULL;
}

static const char*
test_next4(TVM* vm)
{
    TInst inst;
    inst.fOp = op_next;

    vm->fRegister[reg_current_player_idx] = 3;
    vm->fRegister[reg_active_mask] = 2+4+8;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_current_player_idx] != 1)
        return __func__;
    return NULL;
}

static const char*
test_move_n_1(TVM* vm)
{
    TInst inst;
    inst.fOp = op_move_n;

    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_player0_pos] = 0;
    vm->fRegister[reg_dieA] = 1;
    vm->fRegister[reg_dieB] = 2;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_player0_pos] != 3)
        return __func__;
    return NULL;
}

static const char*
test_move_n_2(TVM* vm)
{
    TInst inst;
    inst.fOp = op_move_n;

    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_player0_pos] = 39;
    vm->fRegister[reg_dieA] = 1;
    vm->fRegister[reg_dieB] = 2;
    vm->fRegister[reg_player0_money] = 100;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_player0_money] != 300)
        return __func__;
    return NULL;
}

static const char*
test_jump_on_double_1(TVM* vm)
{
    TInst inst;
    inst.fOp = op_jump_on_doubles;
    inst.fData.uIH.fValue = 300;

    vm->fRegister[reg_pc] = 0;
    vm->fRegister[reg_dieA] = 1;
    vm->fRegister[reg_dieB] = 2;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_pc] != 0)
        return __func__;
    return NULL;
}

static const char*
test_jump_on_double_2(TVM* vm)
{
    TInst inst;
    inst.fOp = op_jump_on_doubles;
    inst.fData.uIH.fValue = 300;

    vm->fRegister[reg_pc] = 0;
    vm->fRegister[reg_dieA] = 1;
    vm->fRegister[reg_dieB] = 1;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_pc] != 300)
        return __func__;
    return NULL;

    return NULL;
}


typedef const char* const_char_p;
typedef const_char_p (*test_vm_case)(TVM* vm);
test_vm_case cases[] = {
    test_iadd, 
    test_next1, 
    test_next2, 
    test_next3, 
    test_next4,
    test_move_n_1,
    test_move_n_2,
    test_jump_on_double_1,
    test_jump_on_double_2,
};


int
main(int argc, const char** argv)
{
    TVM* vm;
    int i, len;
    const_char_p name;
    test_vm_case t;

    vm = VM_New();
    len = sizeof(cases)/sizeof(test_vm_case);

    for(i = 0; i < len; i++){
        t = cases[i];
        name = t(vm);
        if(name){
            printf("!\n");
            printf("fail, %s\n", name);
        }else{
            printf(".");
        }
    }

    TVM_Delete(vm);
    return 0;
}

