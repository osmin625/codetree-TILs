'''
빵
사람 m명
m번째 사람은 m분에 집에서 스폰함.
스폰된 사람은 편의점을 향해 1칸 움직임
최단거리로 이동해야 함.
우선 순위: 상 좌 우 하

벽으로 바뀌는 것
누군가가 도달한 편의점
누군가가 출발한 베이스캠프

사람 수와 베이스 수는 다름.
'''

from collections import deque

dir_ = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # 상 좌 우 하
n, m = map(int, input().split())  # 격자 크기, 사람 수(= 편의점 수)
grid = [list(map(int, input().split())) for _ in range(n)]
'''
0: 빈 공간
1: 베이스캠프
2: 벽(출발한 베이스캠프)
2: 벽(도착한 편의점)
'''
store = []
status_ = [0 for _ in range(m)]
'''
0: 대기 상태
1: 움직이는 상태
2: 편의점에 도착한 상태
'''
time = 0
pos = [[-1, -1] for _ in range(m)]
for i in range(m):
    sx, sy = map(int, input().split())
    store.append((sx - 1, sy - 1))


def spawn(t):
    '''
    사람 t가 목표하는 편의점과 가장 가까운 베이스캠프에서 스폰됨.
    '''
    visited = [[0 for _ in range(n)] for _ in range(n)]
    bases = []
    sx, sy = store[t]

    def get_base_dist(sx, sy):
        q = deque([(sx, sy)])
        dist = 0
        while q:
            for _ in range(len(q)):
                # print(q)
                x, y = q.popleft()
                if grid[x][y] == 1:
                    bases.append((dist, x, y))
                for dx, dy in dir_:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n:  # 격자 내부
                        if grid[nx][ny] != 2:  # 벽이 아니라면
                            if not visited[nx][ny]:
                                visited[nx][ny] = 1
                                q.append((nx, ny))
            dist += 1
        return

    get_base_dist(sx, sy)
    bases.sort()
    bx, by = bases[0][1], bases[0][2]
    pos[t][0], pos[t][1] = bx, by
    grid[bx][by] = 2  # base to wall
    status_[t] = 1
    return


def get_move_pos():
    out = []
    for i in range(m):
        if status_[i] == 1:
            out.append(i)
    return out


def move(i):
    traceback = [[0 for _ in range(n)] for _ in range(n)]
    visited = [[0 for _ in range(n)] for _ in range(n)]
    q = deque([pos[i]])
    px, py = pos[i]
    visited[px][py] = 1
    path = []
    while q:
        x, y = q.popleft()
        if (x, y) == store[i]:
            break
        for dx, dy in dir_:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if not visited[nx][ny]:
                    if grid[nx][ny] != 2:
                        visited[nx][ny] = 1
                        q.append((nx, ny))
                        traceback[nx][ny] = (x, y)

    cx, cy = store[i]
    while True:
        if cx == px and cy == py:
            break
        path.append((cx, cy))
        cx, cy = traceback[cx][cy]

    px, py = path.pop()
    pos[i] = [px, py]
    return


def store_to_wall():
    for i in range(m):
        x, y = pos[i]
        if tuple(pos[i]) == store[i]:
            grid[x][y] = 2
            status_[i] = 2


def in_store_cnt():
    cnt = 0
    for i in range(m):
        if status_[i] == 2:
            cnt += 1
    return cnt


while True:
    # print(*grid, sep='\n')
    # print(status_)
    for i in get_move_pos():
        # print(store[i])
        # print(pos[i])
        # print('move')
        move(i)  # 1
        # print(pos[i])
        # print('---')
    store_to_wall()  # 2
    if in_store_cnt() == m:
        break
    if time < m:
        spawn(time)  # 3
    time += 1

print(time + 1)