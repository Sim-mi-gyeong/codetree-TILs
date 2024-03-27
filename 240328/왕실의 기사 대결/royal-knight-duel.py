import sys
from collections import deque

input = sys.stdin.readline

l, n, q = map(int, input().split())
graph = [[0] * (l + 1)]
for _ in range(1, l + 1):
    graph.append([0] + list(map(int, input().split())))


class Knight:
    def __init__(self, num, x, y, h, w, k):
        self.num = num
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.k = k
        self.damage = 0

    def position(self, map):
        if self.k <= 0:
            return map
        for i in range(self.x, self.x + self.h):
            for j in range(self.y, self.y + self.w):
                map[i][j] = self.num
        return map

    def move(self, dir):
        self.x += dx[dir]
        self.y += dy[dir]

    def hurt(self):
        for i in range(self.x, self.x + self.h):
            for j in range(self.y, self.y + self.w):
                if graph[i][j] == 1:
                    self.damage += 1
                    self.k -= 1


knights = [0]

for num in range(1, n + 1):
    r, c, h, w, k = map(int, input().split())

    knight = Knight(num, r, c, h, w, k)
    knights.append(knight)

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def bfsChain(turn, num, d):

    knightGraph = [[0] * (l + 1) for _ in range(l + 1)]
    for i in range(1, n + 1):
        knightGraph = knights[i].position(knightGraph)

    # i 번 기사의 이동 가능 여부
    moves = [0] * (n + 1)
    q = deque()

    moves[num] = 1
    q.append(num)

    while q:
        k = q.popleft()
        knight = knights[k]

        for i in range(knight.x, knight.x + knight.h):
            for j in range(knight.y, knight.y + knight.w):
                r, c = i, j
                while 1:
                    r += dx[d]
                    c += dy[d]

                    # 격자를 벗어나는 경우 제외
                    if r < 1 or r > l or c < 1 or c > l:
                        return

                    # d 번 방향으로 이동했을 때, 다른 기사가 존재하지 않지만, 벽이 존재하는 경우
                    if knightGraph[r][c] == 0:
                        if graph[r][c] == 2:
                            return
                        break

                    if moves[knightGraph[r][c]] == 0:
                        moves[knightGraph[r][c]] = 1
                        q.append(knightGraph[r][c])

    # 한 명의 기사에게 명령함으로 인해, 여러 기사들이 이동해야 하는지 체크가 완료된 경우
    for i in range(1, n + 1):
        if not moves[i]:
            continue

        # 명령을 받은 기사 이동
        knights[i].move(d)

        # 명령 받지 않은, 영향을 받아 이동해야 하는 기사 대미지
        if i != num:
            knights[i].hurt()


# 생존한! 기사들이 총 받은 대미지의 ₩
for turn in range(1, q + 1):
    # i번 기사에게, 방향 d로 한칸 이동
    i, d = map(int, input().split())

    # 각 기사의 생존 여부 확인
    if knights[i].k <= 0:
        continue

    # 각 기사를 이동시키는 명령 수행
    bfsChain(turn, i, d)

ans = 0
for i in range(1, n + 1):
    if knights[i].k >= 1:
        ans += knights[i].damage

print(ans)