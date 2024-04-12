'''
미로 탈출
N x N
좌상단 1, 1

참가자
1초에 한 칸 이동
출구에 가까워지게 한 칸 이동 가능
우선순위: 상하 > 좌우
움직이지 못하면 움직이지 않음.
한 칸에 두 명 이상 가능

미로
이동이 끝난 후 회전
한 명 이상의 참가자와 출구를 포함하는 가장 작은 정사각형 찾음
여러개인 경우 r,c 좌표가 작은 것이 우선됨.(더 높이 있는 것, 더 왼쪽에 있는 것)
정사각형은 시계 방향으로 90도 회전.
내부의 모든 벽은 내구도가 1씩 깎임.

K초 동안 반복
K초 전에 모든 참가자 탈출 시 게임 끝.
모든 참가자의 이동 거리의 합과 출구 좌표를 출력.
'''

N, M, K = map(int, input().split())
grid = [['-']]
for _ in range(N):
    temp = ['-']
    temp.extend(list(map(int, input().split())))
    grid.append(temp)
pos = {}
pos_status = {}
for i in range(M):
    pos[i] = list(map(int, input().split()))
    pos_status[i] = 1
gate = list(map(int, input().split()))
move_ = [0 for _ in range(N)]
dir_ = {(1, 0), (-1, 0), (0, 1), (0, -1)}


def get_distance(x, y):
    gx, gy = gate
    return abs(gx - x) + abs(gy - y)


def get_alive_pos_items():
    temp = [p for p in pos if pos_status[p]]
    out = []
    for p in temp:
        out.append((p, pos[p]))
    return out


def find_box():
    temp_pos = get_alive_pos_items()
    temp_pos.sort(key=lambda x: x[1])
    min_dist = 21
    tx, ty = 0, 0
    gx, gy = gate
    for i, (x, y) in temp_pos:
        dist = get_distance(x, y)
        if dist < min_dist:
            min_dist = dist
            tx, ty = x, y
    size = max(abs(tx - gx), abs(gy - ty)) + 1
    box_end = [max(tx, gx) + 1, max(ty, gy) + 1]
    box_start = [box_end[0] - size, box_end[1] - size]
    if box_start[1] <= 0:
        gap = 1 - box_start[1]
        box_end[1] += gap
        box_start[1] += gap
    if box_start[0] <= 0:
        gap = 1 - box_start[0]
        box_end[0] += gap
        box_start[0] += gap
    return box_start, box_end, size


def rotate(start, end, size):
    global gate, grid, pos
    sx, sy = start
    ex, ey = end
    grid[gate[0]][gate[1]] = '.'
    for i, (x, y) in get_alive_pos_items():
        # print(f'{sx} < {x} < {ex}, {sy} < {y} < {ey}')
        if sx <= x < ex and sy <= y < ey:
            grid[x][y] = str(i)
    temp = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            # print(ex - j - 1, i + sy, grid[ex - j - 1][i + sy])
            target = grid[ex - j - 1][i + sy]
            if target == '.':
                grid[gate[0]][gate[1]] = 0
                gate = [sx + i, sy + j]
            elif type(target) is str:
                grid[ex - j - 1][i + sy] = 0
                pos[int(target)] = [sx + i, sy + j]
            temp[i][j] = grid[ex - j - 1][i + sy]

    for i in range(size):
        for j in range(size):
            if temp[i][j]:
                grid[sx + i][sy + j] = temp[i][j] - 1
            else:
                grid[sx + i][sy + j] = temp[i][j]


def move_pos():
    global pos, pos_status
    for i, (x, y) in get_alive_pos_items():
        dist = get_distance(x, y)
        for dx, dy in dir_:
            nx, ny = x + dx, y + dy
            if 0 < nx <= N and 0 < ny <= N \
                    and not grid[nx][ny] \
                    and get_distance(nx, ny) < dist:
                # print("move!~~~~~", i)
                move_[i] += 1
                pos[i] = [nx, ny]
                if pos[i] == gate:
                    pos_status[i] = 0
                break


for i in range(K):
    # print(i)
    # print(pos)
    move_pos()
    # print('move')
    # print(pos)
    start, end, size = find_box()
    # print(start, end, size)
    grid[gate[0]][gate[1]] = '.'
    # print(*grid, sep='\n')
    # print(pos)
    grid[gate[0]][gate[1]] = 0
    # print('rotate')
    rotate(start, end, size)
    grid[gate[0]][gate[1]] = '.'
    # print(*grid, sep='\n')
    # print(pos)
    grid[gate[0]][gate[1]] = 0
    # print(move_)
    # print()
print(sum(move_))
print(*gate)