#!/usr/bin/python
# -*- coding=utf8 -*-

from struct import pack


_op_enum = -1

def op_enum():
    global _op_enum
    _op_enum += 1
    return _op_enum


class Op(object):
    def assemble(self):
        pass

    def __init__(self, first=None, second=None, third=None, idx=None, value=None):
        self.fFirst = first or 0
        self.fSecond = second or 0
        self.fThird= third or 0
        self.fIdx = idx or 0
        self.fValue = value or 0



class uNull(Op):
    fmt = 'Bxxx' # must match with union uNull in mvm.h
    def assemble(self):
        return pack(self.fmt, self.__byte__)

class op_die(uNull):
    __byte__ = op_enum()

class op_nop(uNull):
    __byte__ = op_enum()

class op_dump(uNull):
    __byte__ = op_enum()

class op_roll(uNull):
    __byte__ = op_enum()

class op_move_n(uNull):
    __byte__ = op_enum()

class op_goto_jail(uNull):
    __byte__ = op_enum()

class op_next(uNull):
    __byte__ = op_enum()

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

class op_cmp(uIII):
    __byte__ = op_enum()


class uIH(Op):
    fmt = 'BBH'
    def assemble(self):
        return pack(self.fmt, self.__byte__, self.fIdx, self.fValue)

class op_iset(uIH):
    __byte__ = op_enum()

class op_iadd(uIH):
    __byte__ = op_enum()

class op_isub(uIH):
    __byte__ = op_enum()

class op_jump(uIH):
    __byte__ = op_enum()

class op_jump_on_doubles(uIH):
    __byte__ = op_enum()

class op_jump_on_3rd(uIH):
    __byte__ = op_enum()

class op_jump_on_zero(uIH):
    __byte__ = op_enum()

class op_jump_on_positive(uIH):
    __byte__ = op_enum()

class op_jump_on_negative(uIH):
    __byte__ = op_enum()

class op_jump_on_pos(uIH):
    __byte__ = op_enum()


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

    def assemble(self):
        assert self.positioned()
        return ''.join(op.assemble() for op in self.seq)


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

    def assemble(self):
        assert self.blocks
        return ''.join(b.assemble() for b in self.blocks)


_d = dict(locals())

ops = [y for y in sorted((op for op in _d.values() if hasattr(op, "__byte__")), key=lambda x:x.__byte__)]

del _d

if __name__ == "__main__":
    """generate opnum.h"""

    print "#ifndef __OPNUM_H__"
    print "#define __OPNUM_H__"
    print "enum {"
    for op in ops:
        print "    %s = %d, "%(op.__name__ , op.__byte__)
    print "};"
    print "#endif"


