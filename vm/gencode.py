#!/usr/bin/python
# -*- coding=utf8 -*-


class Op(object):
    pass

class uNull(Op):
    pass

class OpRoll(uNull):
    pass

class OpMoveN(uNull):
    pass

class uI(Op):
    pass

class uII(Op):
    pass

class uIII(Op):
    pass

class uIH(Op):
    def __init__(self, I, H):
        self.fValue = H
        self.fIdx = I

class OpJump(uIH):
    def __init__(self, H):
        self.fValue = H

class OpJumpOn3rd(uIH):
    def __init__(self, H):
        self.fValue = H


class Block(object):
    def __init__(self, label=None, seq=None):
        self.label = label
        if seq is None:
            seq = []
        else:
            assert isinstance(seq, (list, tuple))
            assert any(map(lambda x: isinstance(x, Op), seq))
        self.seq = seq
        self.abspos = None

    def __repr__(self):
        return "<Block object %s, %d, %d>"%(self.label, self.abspos, len(self))

    def __len__(self):
        return len(self.seq)

    def deps(self):
        for op in self.seq:
            if hasattr(op, "fValue"):
                x = op.fValue
                if isinstance(x, Block):
                    yield x

    def positioned(self):
        return self.abspos is not None

    def ready(self):
        '''what's wrong with return all(x.positioned() for x in self.deps()) ???'''
        for x in self.deps():
            if not x.positioned():
                return False
        return True

    def place(self, pos):
        self.abspos = pos


class Program(object):
    def __init__(self, root):
        self.root = root
        self.blocks = []

    def layout(self):
        self.pos = 0
        self.visit(self.root)

    def visit(self, b):
        if not b.ready():
            for c in b.deps():
                self.visit(c)
        b.abspos = self.pos
        self.blocks.append(b)
        self.pos += len(b)


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


