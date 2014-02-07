#!/usr/bin/python
# -*- coding=utf8 -*-


from mvmasm import *


getting_jailed = Block(label='getting_jailed')
land_on = Block(label='land_on')
all = Block('main',[
    op_roll(), 
    op_jump_on_3rd(getting_jailed), 
    op_move_n(), 
    op_jump(land_on)])

p = Program(all)
p.layout()
for b in p.blocks:
    print b, b.seq

print repr(op_roll().assemble())
print repr(p.assemble())

