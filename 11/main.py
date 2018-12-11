import sys

def parse_board(ls):
    return [[int(i) for i in l.split()] for l in ls]

def sat_line(l):
    result = [0]
    for i in l:
        result.append(result[-1] + i)
    result.append(result[-1])
    return result

def sat_board(ls):
    result = [[0] * (len(ls) + 2)]
    for l in ls:
        this_line = sat_line(l)
        # result.append(this_line)
    # return result
        new_line = []
        for prev, this in zip(result[-1], this_line):
            new_line.append(prev + this)
        result.append(new_line)
    result.append(result[-1][:])
    return result

def print_board(board):
    for l in board:
        for i in l:
            print("%d\t" % i, end='')
        print()
    print()

def rect(board, x1, y1, x2, y2):
    return board[y1][x1] + board[y2][x2] - board[y1][x2] - board[y2][x1]

def find_greatest_3x3(board):
    w = len(board[0])-2
    h = len(board)-2
    mx = -1000000000000
    argmax = None
    for i in range(0, w-2):
        for j in range(0, h-2):
            s = rect(board, i, j, i+3, j+3)
            if s > mx:
                mx = s
                argmax = ((i+1,j+1), (i+4, j+4))
    return mx, argmax

def find_greatest_square(board):
    w = len(board[0])-2
    h = len(board)-2
    mx = -1000000000000
    argmax = None
    for k in range(1, w+1):
        for i in range(0, w-k+1):
            for j in range(0, h-k+1):
                s = rect(board, i, j, i+k, j+k)
                if s > mx:
                    mx = s
                    argmax = ((i+1,j+1), (i+k, j+k), k)
    return mx, argmax

serial_number = 3463
def make_board():
    result = []
    for y in range(1,301):
        line = []
        for x in range(1,301):
            rack_id = x + 10
            power_level = rack_id * y
            power_level += serial_number
            power_level *= rack_id
            power_level = int(power_level / 100) % 10
            power_level -= 5
            line.append(power_level)
        result.append(line)
    return result

if __name__ == '__main__':
    board = make_board()
    sat = sat_board(board)
    print(find_greatest_square(sat))
