ruDir = [(1, 1), (1, 0), (1, -1), \
         (0, -1), (-1, -1), (-1, 0), \
         (-1, 1), (0, 1)]
dir_ = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상우하좌
DEAD = 0
ALIVE = 1


def alive_santa():
    return [s for s in santa if santa[s][2] >= ALIVE]


def get_distance(r1, c1, r2, c2):
    return (r2 - r1) ** 2 + (c2 - c1) ** 2


def rudolph_move(turn):
    global rPos
    rx, ry = rPos

    def rud_move_direction(s):
        sx, sy = santa[s][0], santa[s][1]
        if rx == sx:
            direction = [0, int(sy > ry) * 2 - 1]
        elif ry == sy:
            direction = [int(sx > rx) * 2 - 1, 0]
        else:
            direction = [int(sx > rx) * 2 - 1, int(sy > ry) * 2 - 1]
        return direction

    def closest_santa():
        target = 0
        target_dist = 1e9
        for s in alive_santa():
            # print('rpos', rPos, 'sx, sy', santa[s][0], santa[s][1])
            dist = get_distance(*rPos, santa[s][0], santa[s][1])
            # print('s', s, 'dist', dist)
            if dist < target_dist:
                target = s
                target_dist = dist
            elif dist == target_dist:
                if (santa[s][0], santa[s][1]) > (santa[target][0], santa[target][1]):
                    target = s
                    target_dist = dist
        return target

    t = closest_santa()
    # print('t:',t)
    if not t:
        return 1
    dx, dy = rud_move_direction(t)
    rPos = (rx + dx, ry + dy)
    if is_collision(*rPos):
        rudolph_collision(*rPos, dx, dy, turn)
    return 0


def rudolph_collision(i, j, dx, dy, turn):
    s = board[i][j]
    board[i][j] = 0
    santa[s][2] = turn + 1
    score[s] += C
    santa[s][0] += dx * C
    santa[s][1] += dy * C
    cx = santa[s][0]
    cy = santa[s][1]
    cs = s
    if 0 < cx <= N and 0 < cy <= N:
        while True:
            if is_collision(cx, cy):
                cs = santa_interaction(cx, cy, cs)
                cx += dx
                cy += dy
                continue
            elif 0 < cx <= N and 0 < cy <= N:
                board[cx][cy] = cs
            else:
                santa[cs][2] = DEAD
            break
    else:
        santa[cs][2] = DEAD


def santa_collision(i, j, dx, dy, move_s, turn):
    score[move_s] += D
    santa[move_s][0] -= dx * D
    santa[move_s][1] -= dy * D
    santa[move_s][2] = turn + 1
    cx = santa[move_s][0]
    cy = santa[move_s][1]
    cs = move_s
    if 0 < cx <= N and 0 < cy <= N:
        while True:
            if is_collision(cx, cy):
                cs = santa_interaction(cx, cy, cs)
                cx -= dx
                cy -= dy
                continue
            elif 0 < cx <= N and 0 < cy <= N:
                santa[cs][0], santa[cs][1] = cx, cy
                board[cx][cy] = cs
            else:
                santa[cs][2] = DEAD
            break
    else:
        santa[cs][2] = DEAD


def santa_move(turn):
    def santa_move_direction(cs):
        sa, sb = santa[cs][0], santa[cs][1]
        dist = get_distance(*rPos, sa, sb)
        temp_dx, temp_dy = 0, 0
        for da, db in dir_:
            nx = sa + da
            ny = sb + db
            temp_dist = get_distance(*rPos, nx, ny)
            if 0 < nx <= N and 0 < ny <= N \
                    and temp_dist < dist \
                    and not is_collision(nx, ny):
                temp_dx, temp_dy = da, db
                dist = temp_dist
        return temp_dx, temp_dy

    for s in alive_santa():
        # print('turn', turn, santa[s][-1])
        if santa[s][-1] >= turn:
            continue
        sx, sy = santa[s][0], santa[s][1]
        board[sx][sy] = 0
        dx, dy = santa_move_direction(s)
        sx += dx
        sy += dy
        santa[s][0], santa[s][1] = sx, sy
        if rPos == (sx, sy):
            santa_collision(sx, sy, dx, dy, s, turn)
        else:
            board[sx][sy] = s


def is_collision(i, j):
    return board[i][j]


def santa_interaction(i, j, s):
    temp = board[i][j]
    board[i][j] = s
    return temp


def alive_santa_bonus():
    global santa
    for s in santa:
        if santa[s][2] >= ALIVE:
            score[s] += 1
    return


# 판 크기, 턴수, 산타 수, 루돌프 힘, 산타 힘
N, M, P, C, D = map(int, input().split())
rPos = list(map(int, input().split()))
santa = dict()
score = [0] * (P + 1)
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
for _ in range(P):
    idx, r, c = list(map(int, input().split()))
    santa[idx] = [r, c, ALIVE]
    board[r][c] = idx

for k in range(2,M + 2):
    # print(k)
    # print(N, M, P, C, D)
    # print(santa, sep='\n')
    # print(score[1:])
    # board[rPos[0]][rPos[1]] = '@'
    # print(*board, sep='\n')
    # board[rPos[0]][rPos[1]] = 0
    if rudolph_move(k):
        break
    santa_move(k)
    alive_santa_bonus()

print(*score[1:])