import sys

def read_points(ls):
    result = []
    for l in ls:
        l = l.split(', ')
        result.append((int(l[0]), int(l[1])))
    return result

def center(points, bound):
    return list((p[0] - bound[0][0] + 1, p[1] - bound[1][0] + 1) for p in points)

def find_bounds(l):
    min_x = min(a[0] for a in l)
    min_y = min(a[1] for a in l)
    max_x = max(a[0] for a in l)
    max_y = max(a[1] for a in l)
    return (min_x, max_x), (min_y, max_y)
infinity = 1000000

def constant_board(w, h, v):
    board = []
    for _ in range(h):
        board.append([v] * w)
    return board

def empty_board(w, h):
    return constant_board(w, h, 0)

def infinity_board(w, h):
    return constant_board(w, h, infinity)
    
def write_board(l):
    (min_x, max_x), (min_y, max_y) = find_bounds(l)
    return empty_board(max_x - min_x + 2, max_y - min_y + 2)

def board_weights(w, h):
    board = []
    board.append([infinity] * w)
    for v in range(h):
        board.append([infinity] + ([1] * w) + [infinity])
    board.append([infinity] * w)
    return board
   
def l1_distance_board(w, h, point):
    result = empty_board(w, h)
    for x in range(w):
        for y in range(h):
            result[y][x] = abs(point[0] - x) + abs(point[1] - y)
    return result

def pprint_board(board):
    for l in board:
        for v in l:
            print("% 3d " % v, end='')
        print()

def update_board(distances, index, argclosest, closest):
    w = len(distances[0])
    h = len(distances)
    for x in range(w):
        for y in range(h):
            if distances[y][x] < closest[y][x]:
                argclosest[y][x] = index
                closest[y][x] = distances[y][x]

def count_regions(distances, indices, points):
    d = {}
    w = len(indices[0])
    h = len(indices)
    weights = board_weights(w, h)
    for x in range(w):
        for y in range(h):
            i = indices[y][x]
            count = 0
            for p in points:
                dist = abs(p[0] - x) + abs(p[1] - y)
                if dist == distances[y][x]:
                    count += 1
            if count == 1:
                d[i] = d.get(i, 0) + weights[y][x]
    result = list((chr(k + 65), v) for (k, v) in d.items()
                  if v < infinity)
    result.sort(key=lambda v:-v[1])
    return result

def add_board(board1, board2):
    return list(list(a + b for (a, b) in zip(la, lb))
                for (la, lb) in zip(board1, board2))

# 6.1
if __name__ == '__main-6.1__':
    l = read_points(sys.stdin.readlines())
    print(l)
    bounds = find_bounds(l)
    w = bounds[0][1] - bounds[0][0] + 2
    h = bounds[1][1] - bounds[1][0] + 2
    l = center(l, bounds)
    argclosest_board = constant_board(w, h, -1)
    closest_board = constant_board(w, h, infinity)
    for i, p in enumerate(l):
        update_board(l1_distance_board(w, h, p),
                     i,
                     argclosest_board,
                     closest_board)
    print(count_regions(closest_board, argclosest_board, l))

# 6.2
if __name__ == '__main__':
    l = read_points(sys.stdin.readlines())
    print(l)
    bounds = find_bounds(l)
    w = bounds[0][1] - bounds[0][0] + 2
    h = bounds[1][1] - bounds[1][0] + 2
    l = center(l, bounds)
    total = empty_board(w, h)
    for i, p in enumerate(l):
        d = l1_distance_board(w, h, p)
        total = add_board(d, total)
    count = 0
    for x in range(w):
        for y in range(h):
            if total[y][x] < 10000:
                count += 1
    print(count)
    #     # pprint_board(argclosest_board)
    #     # print()
    #     return 
    #     update_board(l1_distance_board(closest_board, p),
    #                  i,
    #                  argclosest_board,
    #                  closest_board)
    # print(count_regions(closest_board, argclosest_board, l))
    
