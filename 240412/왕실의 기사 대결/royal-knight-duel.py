'''
L x L 체스판
(1, 1)부터 시작
빈칸, 함정, 벽
'''

dir_ = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
L, N, Q = map(int, input().split()) # 보드 크기, 기사 수, 명령 수
'''
board 정보
0: 빈칸
1: 함정
2: 벽
'''
board = [[2] * (L + 2)]
for _ in range(L):
    temp = [2]
    temp.extend(list(map(int, input().split())))
    temp.append(2)
    board.append(temp)
board.append([2] * (L + 2))
knight_board = [[0 for _ in range(L + 2)] for _ in range(L + 2)]
'''
knights: 기사 정보, (r, c, h, w, k)
(r c): 좌측 상단 좌표 
h: 높이 
w: 길이 
k: 초기 체력
'''
knights = {}
knights_status = {}
for i in range(1, N + 1):
    r, c, h, w, health = list(map(int, input().split()))
    knights[i] = [r, c, h, w, health]
    knights_status[i] = 1
    for x in range(r, r + h):
        for y in range(c, c + w):
            knight_board[x][y] = i
'''
왕의 명령
(i, d): i번 기사가 방향 d로 한 칸 이동하기. (기사가 없을 수도 있음)
d: 0123 (위부터 시계방향)

이동한 칸에 기사가 있으면 도미노로 밀려남
다만 기사 뒤에 벽이 있으면 밀리지 않음.
여러 명의 뒤에 벽이 있으면 모든 기사가 밀리지 않음.
사라진 기사에게 명령 내리면 무시. 

밀려난 기사는 w x h 직사각형 내에 존재하는 함정 수만큼 체력이 깎임
체력이 0이 되면 사망, 체스판에서 사라짐.
'''
queries = [list(map(int, input().split())) for _ in range(Q)]
damages = [0 for _ in range(N + 1)]
'''
모든 명령이 수행된 이후 생존한 기사들이 받은 데미지 총합을 구하기.
'''


def knight_move(idx, d):
    # print(idx)
    if knights_status[idx]:
        stack = knight_push_check(idx, d, [idx])
    # print(stack)
    while stack:
        k = stack.pop()
        knight_push(k, d, idx)

def is_wall(x, y):
    if board[x][y] == 2:
        return True
    return False


def is_knight(x, y):
    return knight_board[x][y]


def knight_push_check(i, d, stack):
    dx, dy = dir_[d]
    r, c, h, w, _ = knights[i]
    wall_flag = False
    knight_flag = False
    for x in range(r, r + h):
        for y in range(c, c + w):
            if knight_board[x + dx][y + dy] == i: # 나라면
                continue
            elif is_wall(x + dx, y + dy):  # 벽이라면
                wall_flag = True
            elif k:= is_knight(x + dx, y + dy): # 기사라면
                if k != stack[-1]:
                    stack.append(k)
                knight_flag = True
            else:  # 벽도 아니고 기사도 아니라면
                continue
    if not wall_flag:
        if not knight_flag:
            return stack
        else:
            return knight_push_check(stack[-1], d, stack)
    return []


def knight_push(i, d, idx):
    global damages
    damage = 0
    dx, dy = dir_[d]
    r, c, h, w, health = knights[i]
    for x in range(r, r + h):
        for y in range(c, c + w):
            knight_board[x][y] = 0
    r, c = r + dx, c + dy
    for x in range(r, r + h):
        for y in range(c, c + w):
            knight_board[x][y] = i
            if board[x][y] == 1:
                damage += 1
    # print('knight_board')
    # print(*knight_board, sep='\n')
    if i != idx:
        health -= damage
        damages[i] += damage
    knights[i] = [r, c, h, w, health]
    if health <= 0:
        knights_status[i] = 0
        for x in range(r, r + h):
            for y in range(c, c + w):
                knight_board[x][y] = 0




for idx, di in queries:
    # print(knights)
    knight_move(idx, di)
    # print('board')
    # print(*board, sep='\n')
    # print(idx, di)
    # print(*knight_board, sep='\n')
    # print(knights)
    # print()

total_damage = 0
for i in range(1, N + 1):
    if knights_status[i]:
        total_damage += damages[i]

print(total_damage)