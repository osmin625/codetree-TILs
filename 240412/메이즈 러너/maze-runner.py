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

N, M, K = map(int, input().split()) # 미로 크기, 참가자 수, 게임 시간
grid = [['-']] # index가 (1,1)부터 시작하기 때문에 index를 맞추기 위해 삽입.
# 인덱싱 오류에 대한 디버깅을 더 쉽게 하기 위해 문자열로 삽입함.
for _ in range(N):
    temp = ['-'] # 인덱스 맞추기
    temp.extend(list(map(int, input().split()))) # 미로 입력받기
    grid.append(temp)
pos = {} # 사람들의 위치
pos_status = {} # 사람들의 상태 (0: 탈출, 1: 미로 안에 존재)
for i in range(M):
    pos[i] = list(map(int, input().split())) # 위치 정보 입력 받기
    pos_status[i] = 1
gate = list(map(int, input().split())) # 출구 위치. 최종적으로 리턴하는 값
move_ = [0 for _ in range(N)] # 움직인 횟수. 최종적으로 리턴하는 값.
dir_ = {(1, 0), (-1, 0), (0, 1), (0, -1)} # 방향. 상하 > 좌우


def get_distance(x, y): # 두 점 사이의 거리 -> 맨해탄 거리로 계산
    gx, gy = gate
    return abs(gx - x) + abs(gy - y)


def get_alive_pos_items(): # 아직 미로에 남아있는 사람들의 위치 정보 받기
    temp = [p for p in pos if pos_status[p]]
    out = []
    for p in temp:
        out.append((p, pos[p]))
    return out


def find_box(): # 회전 대상 박스 찾기
    boxes = []
    gx, gy = gate
    for i, (tx, ty) in get_alive_pos_items():
        size = max(abs(tx - gx), abs(gy - ty)) + 1
        # 먼저 오른쪽 아래 꼭짓점의 위치를 구하기
        box_end = [max(tx, gx) + 1, max(ty, gy) + 1]
        # 오른쪽 아래 꼭짓점을 기준으로 좌상단으로 박스 생성하기
        box_start = [box_end[0] - size, box_end[1] - size]
        # 박스의 시작 부분을 미로 안으로 조정하기
        if box_start[1] <= 0: # x축 방향으로 미로를 벗어난 경우
            gap = 1 - box_start[1]
            box_end[1] += gap
            box_start[1] += gap
        if box_start[0] <= 0: # y축 방향으로 미로를 벗어난 경우
            gap = 1 - box_start[0]
            box_end[0] += gap
            box_start[0] += gap
        boxes.append((size, box_start, box_end))
    boxes.sort()
    # print(boxes)
    return boxes[0]


def rotate(size, start, end): # 박스를 회전하는 함수
    global gate, grid, pos
    sx, sy = start
    ex, ey = end
    grid[gate[0]][gate[1]] = '.' # 출구 좌표를 쉽게 계산하기 위해 문자열 삽입
    in_box_pos = {} # 박스 내에 존재하는 사람들
    for i, (x, y) in get_alive_pos_items():
        # print(f'{sx} < {x} < {ex}, {sy} < {y} < {ey}')
        if sx <= x < ex and sy <= y < ey: # 박스 내에 존재하면
            if not in_box_pos.get((x, y), 0):
                in_box_pos[(x, y)] = []
            in_box_pos[(x, y)].append(i)
    # 회전한 박스를 담기 위한 임시 공간
    temp = [[0 for _ in range(size)] for _ in range(size)]
    # print(start, end, size)
    # print(*grid, sep='\n')

    # 박스 회전
    for i in range(size):
        for j in range(size):
            # print(ex - j - 1, i + sy, grid[ex - j - 1][i + sy])
            target = grid[ex - j - 1][i + sy]
            if target == '.': # 출구인 경우
                grid[gate[0]][gate[1]] = 0 # 0으로 바꾸고
                gate = [sx + i, sy + j] # 새로운 좌표로 갱신
            elif target == 0: # 사람이 서있을 수 있는 빈 공간인 경우
                if in_box_pos.get((ex - j - 1, i + sy), 0):
                    for idx in in_box_pos[(ex - j - 1, i + sy)]: # 사람의 좌표와 같은 경우
                        pos[idx] = [sx + i, sy + j] # 사람의 좌표 갱신
            temp[i][j] = grid[ex - j - 1][i + sy]

    for i in range(size):
        for j in range(size):
            if temp[i][j]: # 벽인 경우
                grid[sx + i][sy + j] = temp[i][j] - 1 # 내구도 감소
            else: # 빈 공간인 경우
                grid[sx + i][sy + j] = temp[i][j] # 그대로 추가
    # grid[gate[0]][gate[1]] = '.'
    # print(*grid, sep='\n')
    # grid[gate[0]][gate[1]] = 0


def move_pos(): # 사람 움직이기
    global pos, pos_status
    for i, (x, y) in get_alive_pos_items(): # 미로 내에 존재하는 사람에 대해
        dist = get_distance(x, y) # 출구 까지 거리 계산
        for dx, dy in dir_: # 다음 방향
            nx, ny = x + dx, y + dy # 다음 좌표
            # 미로 안에 있고, 벽이 아니고, 출구 까지의 거리가 짧아지는 경우
            if 0 < nx <= N and 0 < ny <= N \
                    and not grid[nx][ny] \
                    and get_distance(nx, ny) < dist:
                # print("move!~~~~~", i)
                # 움직이기
                move_[i] += 1
                pos[i] = [nx, ny]
                # 출구에 도착한 경우
                if pos[i] == gate:
                    pos_status[i] = 0
                break # 한 번밖에 못 움직이기 때문에 break.


# print(*grid, sep='\n')
# print(pos)
# rotate((1,1), (1 + N,1 + N), N)
# print(*grid, sep='\n')
# print(pos)

for i in range(K):
    # print(i)
    # print(pos)
    move_pos()
    # print('move')
    # print(pos)
    # print(pos_status)
    # print()
    if not sum(pos_status.values()):
        break
    size, start, end = find_box()
    # print(start, end, size)
    # grid[gate[0]][gate[1]] = '.'
    # print(*grid, sep='\n')
    # print(pos)
    # grid[gate[0]][gate[1]] = 0
    # print('rotate')
    rotate(size, start, end)
    # grid[gate[0]][gate[1]] = '.'
    # print(*grid, sep='\n')
    # print(pos)
    # grid[gate[0]][gate[1]] = 0
    # print(move_)
    # print()
print(sum(move_))
print(*gate)


'''
3 3 10
0 9 0
9 0 9
0 9 0
1 1
1 3
3 1
2 2
'''