#!/usr/bin/python
# -*- coding=utf8 -*-

from struct import pack


_op_enum = -1

def op_enum():
    global _op_enum
    _op_enum += 1
    return _op_enum


class Op(object):
    __name__ = None

    def assemble(self):
        pass

    def __init__(self, first=None, second=None, third=None, idx=None, value=None):
        self.fFirst = first
        self.fSecond = second
        self.fThird= third
        self.fIdx = idx
        self.fValue = value



class uNull(Op):
    fmt = 'Bxxx' # must match with union uNull in mvm.h
    def assemble(self):
        return pack(self.fmt, self.__byte__)

class OpNop(uNull):
    __byte__ = op_enum()

class OpRoll(uNull):
    __byte__ = op_enum()

class OpMoveN(uNull):
    __byte__ = op_enum()
    pass

class uI(Op):
    fmt = 'BBxx'
    def assemble(self):
        return pack(self.fmt, self.__byte__, self.fFirst)

class uII(Op):
    fmt = 'BBBx'
    def assemble(self):
        return pack(self.fmt, self.__byte__, self.fFirst, self.fSecond)

class uIII(Op):
    fmt = 'BBBB'
    def assemble(self):
        return pack(self.fmt, self.__byte__, self.fFirst, self.fSecond, self.fThird)

class uIH(Op):
    fmt = 'BBH'
    def assemble(self):
        return pack(self.fmt, self.__byte__, self.fIdx, self.fValue)

class OpJump(uIH):
    __byte__ = op_enum()
    __name__ = "op_jump"

class OpJumpOn3rd(uIH):
    __byte__ = op_enum()
    __name__ = "op_jump_on_3rd"


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



