'''
N x M 격자
모든 위치 포탑 존재
포탑
공격력이 0 이하가 되면 파괴됨.
공격력 == 체력
최초에 부서진 포탑 존재.

매 턴
가장 약한 포탑 선택 -> 공격력 N + M만큼 증가
'''
from heapq import heapify
from collections import deque
dir_ = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우 하 좌 상
bomb_ = [(-1, -1), (-1, 0), (-1, 1),
         (0, -1), (0, 1),
         (1, -1), (1, 0), (1, 1)]  # 폭격의 범위


def get_weakest_potab():
    '''
    가장 약한 포탑
    1. 공격력이 가장 낮은 포탑
    2. 가장 최근에 공격한 포탑
    3. 포탑 위치의 행, 열 합이 가장 큰 포탑
    4. 열 값이 가장 큰 포탑
    '''
    cand = []
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0:  # 생존한 포탑 대상
                cand.append((grid[i][j], -attack_log[i][j], -(i + j), -j, i, j))
    heapify(cand)
    return (cand[0][-2:])


# def get_potab_count():

def get_strongest_potab():
    cand = []
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0:  # 생존한 포탑 대상
                cand.append((-grid[i][j], attack_log[i][j], (i + j), j, i))
    heapify(cand)
    # print(*cand, sep='\n')
    return (cand[0][-1], cand[0][-2])


def razer(weak, strong):
    '''
    레이저 공격의 경로가 중요해보임.
    stack을 활용하는 dfs로 구현.
    판을 벗어나면 반대편으로 나옴
    '''
    wx, wy = weak
    sx, sy = strong
    q = deque([weak])
    trace_back = [[0 for _ in range(M)] for _ in range(N)]
    visited = [[0 for _ in range(M)] for _ in range(N)]
    can_attack = False
    while q:
        x, y = q.popleft()
        if (x, y) == (sx, sy):
            can_attack = True
            break
        for dx, dy in dir_:
            nx, ny = x + dx, y + dy
            if nx < 0:
                nx += N
            if ny < 0:
                ny += M
            nx, ny = nx % N, ny % M
            if not visited[nx][ny]:
                if grid[nx][ny] > 0:
                    visited[nx][ny] = 1
                    trace_back[nx][ny] = (x, y)
                    q.append((nx, ny))
    if can_attack:
        # print('back')
        # print(*trace_back, sep='\n')
        # print('---')
        grid[sx][sy] -= grid[wx][wy]  # 도착지 피해량
        cx, cy = sx, sy
        while True:
            cx, cy = trace_back[cx][cy]
            if (cx, cy) == (wx, wy):
                break
            grid[cx][cy] -= grid[wx][wy] // 2  # 경유지 피해량
            damaged[cx][cy] = 1  # 피해 입은 좌표들
        return True
    else:
        return False


def potan(weak, strong):
    '''
    판을 벗어나면 반대편으로 나옴.
    공격자는 영향을 받지 않음.
    꼭짓점에 포격 받는 경우 확인.
    '''
    wx, wy = weak
    sx, sy = strong
    grid[sx][sy] -= grid[wx][wy]
    for dx, dy in bomb_:
        nx, ny = sx + dx, sy + dy
        if nx < 0:
            nx += N
        if ny < 0:
            ny += M
        nx, ny = nx % N, ny % M
        if grid[nx][ny] > 0 and (nx, ny) != (wx, wy):
            grid[nx][ny] -= grid[wx][wy] // 2
            damaged[nx][ny] = 1


def power_up(weak, strong):
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0 \
                    and not damaged[i][j] \
                    and (i, j) not in [weak, strong]:
                grid[i][j] += 1


def potab_dead():
    for i in range(N):
        for j in range(M):
            if grid[i][j] <= 0:
                grid[i][j] = 0


def get_potab_alive():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0:
                cnt += 1
    return cnt


N, M, K = map(int, input().split())  # grid 크기, 턴 수
grid = [list(map(int, input().split())) for _ in range(N)]
attack_log = [[0 for _ in range(M)] for _ in range(N)]

for k in range(1, K + 1):
    # print(k)
    damaged = [[0 for _ in range(M)] for _ in range(N)]
    # 부서지지 않은 포탑 1 개일 때 즉시 종료.
    if get_potab_alive() == 1:
        break
    wp = get_weakest_potab()
    sp = get_strongest_potab()
    grid[wp[0]][wp[1]] += N + M
    # print('weak', wp, grid[wp[0]][wp[1]])
    # print('strong', sp)

    attack_log[wp[0]][wp[1]] = k
    if not razer(wp, sp):
        potan(wp, sp)
    # potab_dead()
    power_up(wp, sp)
    # print(*grid, sep='\n')
    # print('--------')
ax, ay = get_strongest_potab()
print(grid[ax][ay])

'''
4 4 100
10 0 0 50
0 0 0 0
0 0 50 50
50 0 50 90

4 4 100
1 50 0 0
50 50 0 0
0 0 50 50
0 0 50 1000
'''