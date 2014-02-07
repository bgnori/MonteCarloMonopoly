#!/usr/bin/python
# -*- coding=utf8 -*-

from struct import pack, unpack


_op_enum = -1

def op_enum():
    global _op_enum
    _op_enum += 1
    return _op_enum


class Op(object):
    def assemble(self, offset):
        pass

    def __init__(self, **kw):
        self.values = kw

class uNull(Op):
    fmt = 'Bxxx' # must match with union uNull in mvm.h
    def assemble(self, offset):
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
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__,
                self.values["first"])

class uII(Op):
    fmt = 'BBBx'
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__,
                self.values["first"], self.values["second"])


class uIII(Op):
    fmt = 'BBBB'
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__,
                self.values["first"], self.values["second"], self.values["third"])

class op_cmp(uIII):
    __byte__ = op_enum()


class uIH(Op):
    fmt = 'BBH'
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__,
                self.values["idx"], self.values["value"])

class op_iset(uIH):
    __byte__ = op_enum()

class op_iadd(uIH):
    __byte__ = op_enum()

class op_isub(uIH):
    __byte__ = op_enum()



class uXA(Op):
    fmt = 'BxH'
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__, self.values["addr"].relpos+offset)

class op_jump(uXA):
    __byte__ = op_enum()

class op_jump_on_doubles(uXA):
    __byte__ = op_enum()

class op_jump_on_3rd(uXA):
    __byte__ = op_enum()

#class op_jump_on_pos(uXA):
#    __byte__ = op_enum()


class uIA(Op):
    fmt = 'BBH'
    def assemble(self, offset):
        return pack(self.fmt, self.__byte__, self.values["idx"], self.values["addr"].relpos+offset)

class op_jump_on_zero(uIA):
    __byte__ = op_enum()

class op_jump_on_positive(uIA):
    __byte__ = op_enum()

class op_jump_on_negative(uIA):
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
        self.relpos = None

    def __repr__(self):
        return "<Block object %s, %d, %d>"%(self.label, self.relpos, len(self))

    def __len__(self):
        return len(self.seq)

    def deps(self):
        for op in self.seq:
            t = op.values.get("addr", None)
            if t is not None and isinstance(t, Block):
                yield t

    def positioned(self):
        return self.relpos is not None

    def ready(self):
        '''what's wrong with return all(x.positioned() for x in self.deps()) ???'''
        for x in self.deps():
            if not x.positioned():
                return False
        return True

    def assemble(self, offset):
        assert self.positioned()
        return ''.join(op.assemble(offset) for op in self.seq)


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
        b.relpos = self.pos
        self.blocks.append(b)
        self.pos += len(b)

    def assemble(self):
        assert self.blocks
        code = []
        info = []
        infolen = len(self.blocks) + 1
        #print infolen
        for b in self.blocks:
            c = b.assemble(infolen)
            code.append(c)
            info.append(pack("I", len(c)/4))

        return pack("I", len(self.blocks)) + ''.join(info) + ''.join(code)


_d = dict(locals())

ops = [y for y in sorted((op for op in _d.values() if hasattr(op, "__byte__")), key=lambda x:x.__byte__)]

del _d


def disassemble(bs):
    chunk = [bs[x:x+4] for x in range(0, len(bs), 4)]
    infolen = unpack("I", chunk[0])[0]
    print infolen
    info = [unpack("I", chunk[i])[0] for i in range(1, infolen+1)]

    offset = infolen + 1

    for n, c in enumerate(info):
        print "block %4d starts %4d, length = %4d "%(n, offset, c)
        for i in range(offset, offset+c):
            w = unpack("BBBB", chunk[i])
            print "%20s(%4d), %4d %4d %4d"%((ops[w[0]].__name__,) + w)
        offset += c



if __name__ == "__main__":
    """generate opnum.h"""

    print "#ifndef __OPNUM_H__"
    print "#define __OPNUM_H__"
    print "enum {"
    for op in ops:
        print "    %s = %d, "%(op.__name__ , op.__byte__)
    print "};"
    print "#endif"


