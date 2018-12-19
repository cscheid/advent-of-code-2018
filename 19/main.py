#!/usr/bin/env pypy3
#  8:31
#   8:44
#   9:58AM

import sys

f = list(l.strip() for l in sys.stdin.readlines())

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

def reg_to_var(v):
    return chr(ord('a') + v)

def disassemble_addr(a, b, c):
    return '%s = %s + %s' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def disassemble_addi(a, b, c):
    return '%s = %s + %s' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_mulr(a, b, c):
    return '%s = %s * %s' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def disassemble_muli(a, b, c):
    return '%s = %s * %s' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_banr(a, b, c):
    return '%s = %s & %s' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def disassemble_bani(a, b, c):
    return '%s = %s & %s' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_borr(a, b, c):
    return '%s = %s | %s' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def disassemble_bori(a, b, c):
    return '%s = %s | %s' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_setr(a, b, c):
    return '%s = %s' % (reg_to_var(c), reg_to_var(a))
def disassemble_seti(a, b, c):
    return '%s = %s' % (reg_to_var(c), a)
def disassemble_setr(a, b, c):
    return '%s = %s' % (reg_to_var(c), reg_to_var(a))
def disassemble_seti(a, b, c):
    return '%s = %s' % (reg_to_var(c), a)
def disassemble_gtir(a, b, c):
    return '%s = 1 if %s > %s else 0' % (reg_to_var(c), a, reg_to_var(b))
def disassemble_gtri(a, b, c):
    return '%s = 1 if %s > %s else 0' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_gtrr(a, b, c):
    return '%s = 1 if %s > %s else 0' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def disassemble_eqir(a, b, c):
    return '%s = 1 if %s == %s else 0' % (reg_to_var(c), a, reg_to_var(b))
def disassemble_eqri(a, b, c):
    return '%s = 1 if %s == %s else 0' % (reg_to_var(c), reg_to_var(a), b)
def disassemble_eqrr(a, b, c):
    return '%s = 1 if %s == %s else 0' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))

opcodes = {
    "eqir": eqir,
    "gtrr": gtrr,
    "gtri": gtri,
    "eqri": eqri,
    "eqrr": eqrr,
    "gtir": gtir,
    "setr": setr,
    "banr": banr,
    "bani": bani,
    "seti": seti,
    "borr": borr,
    "mulr": mulr,
    "addr": addr,
    "muli": muli,
    "addi": addi,
    "bori": bori
    } 

dis_opcodes = {
    "eqir": disassemble_eqir,
    "gtrr": disassemble_gtrr,
    "gtri": disassemble_gtri,
    "eqri": disassemble_eqri,
    "eqrr": disassemble_eqrr,
    "gtir": disassemble_gtir,
    "setr": disassemble_setr,
    "banr": disassemble_banr,
    "bani": disassemble_bani,
    "seti": disassemble_seti,
    "borr": disassemble_borr,
    "mulr": disassemble_mulr,
    "addr": disassemble_addr,
    "muli": disassemble_muli,
    "addi": disassemble_addi,
    "bori": disassemble_bori
    } 


state = [1,0,0,0,0,0] # 0] * 6
instructions = []
print(f[0])
ip = int(f[0].split()[1])
print("# IP: %s" % reg_to_var(ip))
for i,l in enumerate(f[1:]):
    l = l.split()
    print("%2d: %s" % (i, dis_opcodes[l[0]](int(l[1]), int(l[2]), int(l[3]))))
    instructions.append((l[0], int(l[1]), int(l[2]), int(l[3])))

def run():
    ticks = 0
    changed = False
    while True:
        for i in range(1000000):
            if state[ip] >= len(instructions):
                return
            if state[ip] == 1:
                print(state)
                exit(1)
            ci = instructions[state[ip]]
            old_state_1 = state[1]
            opcodes[ci[0]](0, ci[1], ci[2], ci[3], state)
            if state[1] != old_state_1 and not changed:
                print("Changed!", ci, old_state_1, state)
                # state[1] = 10551373
                changed = True
                
                # d1 = state[1] - old_state_1
                # exit(1)
            # if state[5] == 9999:
            #     state[5] = 10551375
            #     # state[1] = 10551364 # state[2] - 12 + 1# 2 * state[4]
            state[ip] += 1
            ticks += 1
        print(ci, state, ticks)
        # YOLOOOO
        # state[2] = 10000
        # print(ci, state)

run()
print(state)
