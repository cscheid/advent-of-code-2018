# 8:14AM
#  8:54AM
#  
board = []
board.append(3)
board.append(7)
elf1 = 0
elf2 = 1

improvements = 0
while True:
    v1 = board[elf1]
    v2 = board[elf2]
    s = v1 + v2
    l = list(int(c) for c in str(s))
    board.extend(l)
    elf1 = (elf1 + (1 + v1)) % len(board)
    elf2 = (elf2 + (1 + v2)) % len(board)
    v1 = board[elf1]
    v2 = board[elf2]
    improvements += 1
    if board[-7:-1] == [0, 8, 4, 6, 0, 1]:
        print(len(board)-7)
        exit(1)
    if board[-6:] == [0, 8, 4, 6, 0, 1]:
        print(len(board)-6)
        exit(1)
    if improvements % 1000000 == 0:
        print("\r                                \r%d \t%s \t%s" % (improvements, elf1, elf2), end='')

    
