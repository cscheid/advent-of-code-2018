# 7:33PM
#   7:52PM
#   8:09PM

import sys

def addr(opc, a, b, c, reg):
    reg[c] = reg[a] + reg[b]

def addi(opc, a, b, c, reg):
    reg[c] = reg[a] + b

def mulr(opc, a, b, c, reg):
    reg[c] = reg[a] * reg[b]

def muli(opc, a, b, c, reg):
    reg[c] = reg[a] * b

def banr(opc, a, b, c, reg):
    reg[c] = reg[a] & reg[b]

def bani(opc, a, b, c, reg):
    reg[c] = reg[a] & b

def borr(opc, a, b, c, reg):
    reg[c] = reg[a] | reg[b]

def bori(opc, a, b, c, reg):
    reg[c] = reg[a] | b

def setr(opc, a, b, c, reg):
    reg[c] = reg[a]

def seti(opc, a, b, c, reg):
    reg[c] = a

def gtir(opc, a, b, c, reg):
    reg[c] = 1 if a > reg[b] else 0

def gtri(opc, a, b, c, reg):
    reg[c] = 1 if reg[a] > b else 0

def gtrr(opc, a, b, c, reg):
    reg[c] = 1 if reg[a] > reg[b] else 0

def eqir(opc, a, b, c, reg):
    reg[c] = 1 if a == reg[b] else 0

def eqri(opc, a, b, c, reg):
    reg[c] = 1 if reg[a] == b else 0

def eqrr(opc, a, b, c, reg):
    reg[c] = 1 if reg[a] == reg[b] else 0
    
##############################################################################
# solved this by hand from the original possible instruction list, FWIW

opcodes = {
    5: eqir,
    13: gtrr,
    8: gtri,
    9: eqri,
    4: eqrr,
    10: gtir,
    6: setr,
    15: banr,
    1: bani,
    3: seti,
    11: borr,
    14: mulr,
    12: addr,
    0: muli,
    2: addi,
    7: bori
}    

instructions = [addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr]

possible_instructions = list(instructions[:] for i in range(16))

def check_inst(inst_f, bef, inst_code, after):
    bef = bef[:]
    inst_f(inst_code[0], inst_code[1], inst_code[2], inst_code[3], bef)
    if bef == after:
        return True
    return False

f = (l for l in sys.stdin.readlines())

##############################################################################

samples = 0
total = 0
reg = [0,0,0,0]
try:
    while True:
        l = next(f)
        if l.startswith('Before:'):
            l1 = l.strip()
            state_before = l1[:-1].split(',')
            state_before = [int(state_before[0][-1])] + [int(i) for i in state_before[1:]]
            inst = [int(i) for i in next(f).strip().split()]
            l3 = next(f).strip()
            state_after = l3[:-1].split(',')
            state_after = [int(state_after[0][-1])] + [int(i) for i in state_after[1:]]
            next(f)
            print(possible_instructions[inst[0]])
            possible_instructions[inst[0]] = list(
                inst_f for inst_f in possible_instructions[inst[0]] if check_inst(inst_f, state_before, inst, state_after))
            print(possible_instructions[inst[0]])
            print("-")
        else:
            inst = list(int(i) for i in l.strip().split())
            opcodes[inst[0]](inst[0], inst[1], inst[2], inst[3], reg)
except StopIteration:
    print(reg)
