import sys
si = sys.stdin.readline
class Santa:
    def __init__(self, r, c):
        # 산타의 행, 열 위치
        self.r = r
        self.c = c
        # 산타가 얻은 점수
        self.score = 0
        # 언제까지 기절하는 지
        self.faint = -1
        # 생존 여부
        self.alive = True
# input
n, m, p, C, D = map(int, si().split())
rudolf = list(map(int, si().split()))  # 루돌프의 위치
santas = [None for _ in range(p)]  # 각 산타의 위치
for _ in range(p):
    idx, r, c = map(int, si().split())
    idx -= 1
    santas[idx] = Santa(r, c)
dirs = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1))
def get_dist(r1, c1, r2, c2):
    return (r1 - r2) * (r1 - r2) + (c1 - c2) * (c1 - c2)
def get_dist_rudolf_and_santa(s: Santa):
    return get_dist(rudolf[0], rudolf[1], s.r, s.c)
def move_rudolf() -> int:
    # 1. 가장 가까운 산타 찾기
    tgt = None
    for i in range(p):
        if not santas[i].alive:  # 탈락한 산타면 무시하기
            continue
        if tgt is None:
            tgt = santas[i]
        else:
            # 지금까지 알던 최단거리
            d1 = get_dist_rudolf_and_santa(tgt)
            # 새롭게 만난 산타와의 거리
            d2 = get_dist_rudolf_and_santa(santas[i])
            if d1 > d2:
                tgt = santas[i]
            elif d1 == d2 and (tgt.r < santas[i].r or (tgt.r == santas[i].r and tgt.c < santas[i].c)):
                tgt = santas[i]
    # 2. 이동 방향 정하기
    direction, dist = 0, 0
    for d in range(8):
        # 루돌프가 d 번 방향으로 갔을 때의 위치
        nr, nc = rudolf[0] + dirs[d][0], rudolf[1] + dirs[d][1]
        new_dist = get_dist(nr, nc, tgt.r, tgt.c)
        if d == 0 or dist > new_dist:
            direction = d
            dist = new_dist
    # 3. 해당 방향으로 이동 하기
    rudolf[0] += dirs[direction][0]
    rudolf[1] += dirs[direction][1]
    return direction
def conflict(arrive_r, arrive_c, direction, dist, current_turn):
    # 만약 (arrive_r, arrive_c) 에서 충돌이 일어났다면, 산타를 direction 방향으로 dist 만큼 밀어내는 함수
    
    # 1. 충돌이 일어났는 지 확인
    for i in range(p):
        if not santas[i].alive:
            continue
        if arrive_r == santas[i].r and arrive_c == santas[i].c:
            dr, dc = dirs[direction]
            nr = santas[i].r + dr * dist  # 도착하는 위치 좌표
            nc = santas[i].c + dc * dist
            # 도착하는 위치에 대해 연쇄적인 상호작용
            # 내가 도착할 위치에 있는 산타를, 나랑 똑같은 방향으로, 1만큼 밀어줘
            conflict(nr, nc, direction, 1, current_turn)
            # 도착할 위치가 깨끗해졌으니, 이동하자!
            santas[i].r = nr
            santas[i].c = nc
            # 기절 여부
            if rudolf == [arrive_r, arrive_c]:
                santas[i].faint = current_turn + 1
                santas[i].score += dist
            # 탈락 여부 확인
            if santas[i].r < 1 or santas[i].c < 1 or santas[i].r > n or santas[i].c > n:
                santas[i].alive = False
def santa_exist(r, c) -> bool:
    for i in range(p):
        if santas[i].r == r and santas[i].c == c:
            return True
    return False
def move_santa(s: Santa) -> int:
    # 1. 루돌프를 향해 이동하기
    tgt = Santa(rudolf[0], rudolf[1])
    # 2. 이동 방향 정하기
    direction, dist = -1, get_dist(s.r, s.c, tgt.r, tgt.c)
    for d in range(4):
        # 산타가 d 번 방향으로 갔을 때의 위치
        nr, nc = s.r + dirs[d][0], s.c + dirs[d][1]
        new_dist = get_dist(nr, nc, tgt.r, tgt.c)
        if dist > new_dist and not santa_exist(nr, nc):
            direction = d
            dist = new_dist
    if direction != -1:
        # 3. 해당 방향으로 이동 하기
        s.r += dirs[direction][0]
        s.c += dirs[direction][1]
    return direction
# simulation
for turn in range(m):
    # 1. 루돌프 이동
    rudolf_direction = move_rudolf()
    # 2. 충돌이 일어났다면, 산타를 밀어내기
    conflict(rudolf[0], rudolf[1], rudolf_direction, C, turn)
    # 3. 산타 0 ~ (P - 1)번 순서로 이동
    for i in range(p):
        if not santas[i].alive:
            continue
        if santas[i].faint >= turn:  # 아직 기절해있다면, 이동 X
            continue
        # 3-1. 산타 이동하기
        direction = move_santa(santas[i])
        if direction == -1:  # 산타가 이동하지 않은 경우
            continue
        # 3-2. 매 이동 마다 충돌이 일어났다면, 산타를 밀어내기
        conflict(rudolf[0], rudolf[1], direction ^ 2, D, turn)
    # 4. 살아남은 산타의 점수 증가
    alive_cnt = 0
    for i in range(p):
        if santas[i].alive:
            santas[i].score += 1
            alive_cnt += 1
    # 5. 모든 산타가 탈락했다면, 즉시 게임 종료
    if alive_cnt == 0:
        break
for i in range(p):
    # i 번째 산타의 점수 출력하기
    print(santas[i].score, end=' ')