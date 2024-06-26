from collections import deque

'''
LxL 체스판
좌상단 (1, 1)
빈칸, 함정, 벽

기사
직사각형(정사각형 가능)
왕의 명령에 따라 상하좌우 1칸 움직임.
다른 기사 밀치기 가능 -> 다른 기사가 물러날 공간이 있어야 함.
체력이 0이 되면 체스판에서 사라짐
사라진 기사는 명령 무시.

대결(밀치기)
이동한 곳에 놓여진 함정 개수만큼 피해

 생존한 기사들이 받은 데미지 총합
'''
dir_ = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
L, N, Q = map(int, input().split())  # 보드 크기, 기사 수, 명령 수
board = [[2 for _ in range(L + 2)]]
for _ in range(L):
    temp = [2]
    temp.extend(list(map(int, input().split())))
    temp.append(2)
    board.append(temp)
board.append([2 for _ in range(L + 2)])
r_ = {}
c_ = {}
h_ = {}
w_ = {}
health = {}
damage = {}
# print(*board, sep='\n')
for i in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    r_[i] = r
    c_[i] = c
    h_[i] = h
    w_[i] = w
    health[i] = k
    damage[i] = 0

query = [list(map(int, input().split())) for _ in range(Q)]
is_wall = {i: 0 for i in range(1, N + 1)}


def get_alive_knight():
    return [i for i in range(1, N + 1) if health[i] > 0]


def get_pushed_knight(idx, d):
    dx, dy = dir_[d]
    knights = []
    visited = [0 for _ in range(N + 1)]
    visited[idx] = 1
    q = deque([idx])
    while q:
        i = q.popleft()
        for x in range(r_[i], r_[i] + h_[i]):
            for y in range(c_[i], c_[i] + w_[i]):
                nx, ny = x + dx, y + dy
                # 기사의 이웃한 칸이
                if nx in [r_[i] - 1, r_[i] + h_[i]] \
                        or ny in [c_[i] - 1, c_[i] + w_[i]]:
                    if nx in [r_[i] - 1, r_[i] + h_[i]] \
                            and ny in [c_[i] - 1, c_[i] + w_[i]]:
                        continue
                    # 살아 있는 기사 k의 범위에 포함된다면
                    for k in get_alive_knight():
                        if r_[k] <= nx < r_[k] + h_[k] \
                                and c_[k] <= ny < c_[k] + w_[k]\
                                and not visited[k]:
                            # knight와 q에 기사 추가
                            visited[k] = 1
                            knights.append(k)
                            q.append(k)
    return knights


def knight_wall_check(i, d):
    global is_wall
    dx, dy = dir_[d]
    for x in range(r_[i], r_[i] + h_[i]):
        for y in range(c_[i], c_[i] + w_[i]):
            nx, ny = x + dx, y + dy
            # 기사의 이웃한 칸이
            if nx in [r_[i] - 1, r_[i] + h_[i]] \
                    or ny in [c_[i] - 1, c_[i] + w_[i]]:
                # 벽이라면
                if board[nx][ny] == 2:
                    is_wall[i] = 1
                    return


def knight_move(i, d):
    dx, dy = dir_[d]
    r_[i] += dx
    c_[i] += dy
    # 데미지 계산하기
    damage[i] = 0
    for x in range(r_[i], r_[i] + h_[i]):
        for y in range(c_[i], c_[i] + w_[i]):
            if board[x][y] == 1:
                damage[i] += 1
    health[i] -= damage[i]


def knight_attack(i, d):
    dx, dy = dir_[d]
    r_[i] += dx
    c_[i] += dy


prev_health = health.copy()
for i, d in query:
    # print('---', i, d)
    # print(health)
    if health[i] <= 0:
        continue
    knights = get_pushed_knight(i, d)
    # print(knights)
    # print(r_)
    # print(c_)
    # print()
    knight_wall_check(i, d)
    for k in knights:
        knight_wall_check(k, d)

    if not any(is_wall.values()):  # 벽이 없다면
        knight_attack(i, d)
        for k in knights:
            knight_move(k, d)  # 목록에 포함된 모든 나이트 밀기
    else:
        for i in range(1, N + 1):
            is_wall[i] = 0

# print(damage)
# print(health)
ans = [prev_health[i] - health[i] for i in range(1, N + 1) if health[i] > 0]
print(sum(ans))

'''
4 4 19
1 0 0 0
1 0 0 0
0 2 0 0
1 1 0 0
3 1 2 1 10
1 2 2 1 10
1 3 1 1 10
4 2 1 2 1
1 0
1 0
1 1
1 1
2 2
2 1
2 2
2 3
2 0
2 0
2 1
2 3
1 2
2 1
2 2
3 3
3 3
3 3
3 2

4 3 11 
2 0 0 1
0 0 2 0
0 2 0 0
1 1 0 2
4 1 1 1 10
1 3 1 1 1
4 2 1 1 10
1 0
1 0
1 1
1 0
1 1
1 1
1 2
1 2
1 3
1 2
1 3


5 6 1
0 0 0 0 1
0 0 0 0 1
0 0 0 0 1
0 0 0 0 1
0 0 0 2 1
2 1 2 1 10
1 2 2 1 10
1 3 2 1 10
3 2 2 1 10
4 3 2 1 10
2 4 2 1 10
1 1

4 6 2
1 0 0 1
1 0 0 1
1 0 0 1
1 0 0 1
1 1 4 1 10
1 2 1 1 10
1 3 1 1 1
2 3 1 1 10
3 3 1 1 10
4 3 1 1 10
1 1
3 3
'''