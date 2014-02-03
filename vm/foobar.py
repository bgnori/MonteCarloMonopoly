#!/usr/bin/python
# -*- coding=utf8 -*-


from mvmasm import Block, OpRoll, OpJumpOn3rd, OpMoveN, OpJump, Program


getting_jailed = Block(label='getting_jailed')
land_on = Block(label='land_on')
all = Block('main',[
    OpRoll(), 
    OpJumpOn3rd(getting_jailed), 
    OpMoveN(), 
    OpJump(land_on)])

p = Program(all)
p.layout()
for b in p.blocks:
    print b, b.seq

print repr(OpRoll().assemble())
