


"""
def is3rdRoll(player, _then, _else):
    pass

def nextPlayer(player):
    pass

def then(label, code, addr2ret):
    pos = startseg()
    print label
    print code
    print "op_jump", addr2ret
    endseg()
    return pos

def JumpOn3rd(addr2ret):
    print "op_jump_on_3rd", then("place content here", code, addr2ret)

def LandOn():
    "big switch"
    print "op_goto_jail" #etc

def RollAndMove():
    #reg_current_player_idx 
    print "op_roll"
    JumpOn3rd(next_pc())
    print "op_move_n"
    LandOn()


def whileloop(regname):
    pass
"""

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
    def __init__(self, seq=None):
        if seq is None:
            seq = []
        else:
            assert isinstance(seq, (list, tuple))
            assert any(map(lambda x: isinstance(x, Op), seq))
        self.seq = seq
        self.abspos = None

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


getting_jailed = Block()
land_on = Block()
all = Block([OpRoll(), OpJumpOn3rd(getting_jailed), OpMoveN(), OpJump(land_on)])

p = Program(all)
p.layout()
for b in p.blocks:
    print b.abspos, b.seq


