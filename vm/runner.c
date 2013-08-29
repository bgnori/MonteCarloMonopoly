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
}

static const char*
test_jump_on_3rd_1(TVM* vm)
{
    TInst inst;
    inst.fOp = op_jump_on_3rd;
    inst.fData.uIH.fValue = 300;
    vm->fRegister[reg_pc] = 0;
    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_player0_state] = 0;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_pc] != 0)
        return __func__;
    return NULL;
}

static const char*
test_jump_on_3rd_2(TVM* vm)
{
    TInst inst;
    inst.fOp = op_jump_on_3rd;
    inst.fData.uIH.fValue = 300;
    vm->fRegister[reg_pc] = 0;
    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_player0_state] = 3;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_pc] != 300)
        return __func__;
    return NULL;
}

static const char*
test_cmp_eq(TVM* vm)
{
    TInst inst;
    inst.fOp = op_cmp;
    inst.fData.uIII.fFirst = reg_r0;
    inst.fData.uIII.fSecond = reg_r1;
    inst.fData.uIII.fThird = reg_r2;
    vm->fRegister[reg_r0] = 0;
    vm->fRegister[reg_r1] = 0;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_r2] != 0)
        return __func__;
    return NULL;
}

static const char*
test_cmp_lt(TVM* vm)
{
    TInst inst;
    inst.fOp = op_cmp;
    inst.fData.uIII.fFirst = reg_r0;
    inst.fData.uIII.fSecond = reg_r1;
    inst.fData.uIII.fThird = reg_r2;
    vm->fRegister[reg_r0] = 0;
    vm->fRegister[reg_r1] = 2;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_r2] != -1)
        return __func__;
    return NULL;
}

static const char*
test_cmp_gt(TVM* vm)
{
    TInst inst;
    inst.fOp = op_cmp;
    inst.fData.uIII.fFirst = reg_r0;
    inst.fData.uIII.fSecond = reg_r1;
    inst.fData.uIII.fThird = reg_r2;
    vm->fRegister[reg_r0] = 0;
    vm->fRegister[reg_r1] = -2;
    TVM_Exec(vm, inst);
    if (vm->fRegister[reg_r2] != 1)
        return __func__;
    return NULL;
}

static const char*
test_land_on_gtj(TVM* vm)
{
    TInst inst;
    inst.fOp = op_land_on;
    vm->fRegister[reg_current_player_idx] = 0;
    vm->fRegister[reg_player0_pos] = 30;
    TVM_Exec(vm, inst);
    if ((vm->fRegister[reg_player0_pos] != 10) ||
            (vm->fRegister[reg_player0_state] != 1))
        return __func__;
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
    test_jump_on_3rd_1,
    test_jump_on_3rd_2,
    test_cmp_eq,
    test_cmp_lt,
    test_cmp_gt,
    test_land_on_gtj,
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
        TVM_Deadbeaf(vm);
        t = cases[i];
        name = t(vm);
        if(name){
            printf("!\n");
            printf("fail, %s\n", name);
            TVM_DumpRegs(vm);
        }else{
            printf(".");
        }
    }

    TVM_Delete(vm);
    return 0;
}


