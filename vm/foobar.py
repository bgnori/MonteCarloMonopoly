#!/usr/bin/python
# -*- coding=utf8 -*-


from mvmasm import *


all = Block('main',[
    op_roll(), 
    op_jump_on_3rd(
        addr=Block('getting_jailed', [
            op_nop(),
            op_nop(),
            op_nop(),
            op_nop(),
            ])),
    op_move_n(), 
    op_jump(
        addr=Block('land_on', [
            op_nop(),
            op_nop(),
            op_nop(),
            op_nop(),
            ]))
        ])

p = Program(all)
p.layout()
for b in p.blocks:
    print b, b.seq

print repr(op_roll().assemble(0))

b = p.assemble()

disassemble(b)


