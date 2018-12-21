#!/usr/bin/env pypy3
# 9:31AM
#  
#

import time
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

def cpp_addr(a, b, c):
    return '  %s = %s + %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def cpp_addi(a, b, c):
    return '  %s = %s + %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_mulr(a, b, c):
    return '  %s = %s * %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def cpp_muli(a, b, c):
    return '  %s = %s * %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_banr(a, b, c):
    return '  %s = %s & %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def cpp_bani(a, b, c):
    return '  %s = %s & %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_borr(a, b, c):
    return '  %s = %s | %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def cpp_bori(a, b, c):
    return '  %s = %s | %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_setr(a, b, c):
    return '  %s = %s;' % (reg_to_var(c), reg_to_var(a))
def cpp_seti(a, b, c):
    return '  %s = %s;' % (reg_to_var(c), a)
def cpp_setr(a, b, c):
    return '  %s = %s;' % (reg_to_var(c), reg_to_var(a))
def cpp_seti(a, b, c):
    return '  %s = %s;' % (reg_to_var(c), a)
def cpp_gtir(a, b, c):
    return '  %s = %s > %s;' % (reg_to_var(c), a, reg_to_var(b))
def cpp_gtri(a, b, c):
    return '  %s = %s > %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_gtrr(a, b, c):
    return '  %s = %s > %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))
def cpp_eqir(a, b, c):
    return '  %s = %s == %s;' % (reg_to_var(c), a, reg_to_var(b))
def cpp_eqri(a, b, c):
    return '  %s = %s == %s;' % (reg_to_var(c), reg_to_var(a), b)
def cpp_eqrr(a, b, c):
    return '  %s = %s == %s;' % (reg_to_var(c), reg_to_var(a), reg_to_var(b))

cpp_opcodes = {
    "eqir": cpp_eqir,
    "gtrr": cpp_gtrr,
    "gtri": cpp_gtri,
    "eqri": cpp_eqri,
    "eqrr": cpp_eqrr,
    "gtir": cpp_gtir,
    "setr": cpp_setr,
    "banr": cpp_banr,
    "bani": cpp_bani,
    "seti": cpp_seti,
    "borr": cpp_borr,
    "mulr": cpp_mulr,
    "addr": cpp_addr,
    "muli": cpp_muli,
    "addi": cpp_addi,
    "bori": cpp_bori
    } 

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


instructions = []
ip = int(f[0].split()[1])

try:
    cmd = sys.argv[1]
except IndexError:
    cmd = 'run'

if cmd == 'compile':
    print("// IP: %s" % reg_to_var(ip))
    print(open("preamble.cc").read())
    print ("  static const void* instructions[] = {")
    for i in range(len(f[1:])):
        print("    &&l%d" % i, end='')
        if i != len(instructions)-1:
            print(",")
        else:
            print()
    print("  };");
    print("  n_instructions = %d;" % len(f[1:]))

    for i,l in enumerate(f[1:]):
        l = l.split()
        print("l%d: %s" % (i, cpp_opcodes[l[0]](int(l[1]), int(l[2]), int(l[3]))))
        print("  goto done;")
        instructions.append((l[0], int(l[1]), int(l[2]), int(l[3])))
    print(open("postamble.cc").read())
    exit(0)
elif cmd == 'disassemble':
    for i,l in enumerate(f[1:]):
        l = l.split()
        print("%3d: %s" % (i, cpp_opcodes[l[0]](int(l[1]), int(l[2]), int(l[3]))))
    exit(0)
else:
    print("will run!")
    for i,l in enumerate(f[1:]):
        l = l.split()
        instructions.append((l[0], int(l[1]), int(l[2]), int(l[3])))

reg0_value = int(sys.argv[2])
state = [reg0_value,0,0,0,0,0]
def run():
    ticks = 0
    changed = False
    n = len(instructions)
    while True:
        cip = state[ip]
        if cip >= n:
            break
        ci = instructions[cip]
        opcodes[ci[0]](0, ci[1], ci[2], ci[3], state)
        state[ip] += 1
        ticks+=1
    print(ticks)
run()
