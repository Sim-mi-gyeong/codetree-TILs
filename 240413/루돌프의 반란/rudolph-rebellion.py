import sys

input = sys.stdin.readline

# 루돌프 움직임
# 위, 오른쪽 위, 오른쪽, 오른쪽 아래, 아래, 왼쪽 아래, 왼쪽, 왼쪽 위
dx_rudolf = [-1, -1, 0, 1, 1, 1, 0, -1]
dy_rudolf = [0, 1, 1, 1, 0, -1, -1, -1]

# 산타 움직임
# 상우하좌
dx_santa = [-1, 0, 1, 0]
dy_santa = [0, 1, 0, -1]


class Rudolf:
    def __init__(self, x, y, power, dir):
        self.x = x
        self.y = y
        self.power = power
        self.dir = dir

    def move(self, nd):
        self.x += dx_rudolf[nd]
        self.y += dy_rudolf[nd]
        self.dir = nd


# die : 죽음 여부
# shock_turn : 기절한 턴
class Santa:
    def __init__(self, num, x, y, power, score, dir, die, shock_turn):
        self.num = num
        self.x = x
        self.y = y
        self.power = power
        self.score = score
        self.dir = dir  # 산타의 방향
        self.die = die  # 죽었는지 여부
        self.shock_turn = shock_turn  # 루돌프와 충돌하여 기절한 턴 번호

    def move(self, nx, ny, nd):

        # 이동 전 위치 초기화
        graph[self.x][self.y] = 0

        self.x = nx
        self.y = ny
        self.dir = nd

        # 이동 후 번호 기록
        graph[self.x][self.y] = self.num


n, m, p, c, d = map(int, input().split())

graph = [[0] * (n + 1) for _ in range(n + 1)]
sx, sy = map(int, input().split())  # 루돌프 위치
rudolf = Rudolf(sx, sy, c, 0)

# p명의 산타 번호와 위치

### TC 1번은 산타 순서대로 입력 받으니까!!!!!!!!! 번호 == santas 에서 인덱스
### TC 2번은 산타 순서대로 입력 받지 X -> dict 형태로?
# santas = dict()
santas = [None for _ in range(p + 1)]  # 각 산타의 위치
for _ in range(p):
    num, x, y = map(int, input().split())
    graph[x][y] = num
    # score : 0, dir : 0, die : False, shock_turn : 0 초기화
    santa = Santa(num, x, y, d, 0, 0, False, -1)
    santas[num] = santa


# src_santa_num 산타가 (next_x, next_y) 로 밀려나려고 할 때,
# 그 위치에 다른 산타(target_santa_num)가 있는 경우 연쇄적으로 1칸씩 밀려남
def interaction(type, src_santa_num, target_santa_num, next_x, next_y, dir):

    if type == 0:
        new_next_x = next_x + dx_rudolf[dir]
        new_next_y = next_y + dy_rudolf[dir]

    elif type == 1:
        new_next_x = next_x + dx_santa[dir]
        new_next_y = next_y + dy_santa[dir]

    # # 그것과는 별개로 나는(최초 밀려난 산타) 이동
    # santas[src_santa_num].move(next_x, next_y, dir)

    # 밀려나게 될 산타가 범위 벗어나는 경우
    if new_next_x < 1 or new_next_x > n or new_next_y < 1 or new_next_y > n:
        santas[target_santa_num].die = True
        return

    # 밀려나는 산타가 이동하게 된 위치에 또 산타가 있는 경우
    if graph[new_next_x][new_next_y] != 0:
        interaction(
            type,
            target_santa_num,
            graph[new_next_x][new_next_y],
            new_next_x,
            new_next_y,
            dir,
        )
    else:
        santas[target_santa_num].move(new_next_x, new_next_y, dir)

    # 그것과는 별개로 나는(최초 밀려난 산타) 이동
    santas[src_santa_num].move(next_x, next_y, dir)


# 루돌프에 의해 밀려난건지 -> type -> 0
# 산타에 의해 밀려난건지 -> type : 1
# 에 따라 dx 가 달라짐
def conflict(type, score, num, x, y, dir):
    # 얻을 점수(=밀려날 칸 수), 밀려날 산타 번호, 위치 x, 위치 y, 밀려날 방향

    # 밀려가게 될 예정이므로, 위치 초기화
    graph[x][y] = 0

    # 루돌프에 의해서 충돌이 발생했는데 -> 이후 상호작용이 일어나는 경우는 TC 1번에 X

    if type == 0:
        next_x = santas[num].x + dx_rudolf[dir] * score
        next_y = santas[num].y + dy_rudolf[dir] * score

    elif type == 1:
        next_x = santas[num].x + dx_santa[dir] * score
        next_y = santas[num].y + dy_santa[dir] * score

    if next_x < 1 or next_x > n or next_y < 1 or next_y > n:
        santas[num].die = True
        return

    # 밀려난 칸에 다른 산타가 있는 경우
    if graph[next_x][next_y] != 0:
        interaction(type, num, graph[next_x][next_y], next_x, next_y, dir)

    else:
        santas[num].move(next_x, next_y, dir)


def move_rudolf(turn):

    # 8방향 중 1칸 이동을 위해 탈락하지 않은, 가장 가까운 산타 찾기
    # 1~p번 산타들 간 가장 가까운?

    min_dist = int(1e9)
    min_dist_santa = []
    for i in range(1, p + 1):
        # 탈락한 산타는 X
        if santas[i].die:
            continue
        target_x, target_y = santas[i].x, santas[i].y

        dist = (rudolf.x - target_x) ** 2 + (rudolf.y - target_y) ** 2

        min_dist_santa.append((dist, i, target_x, target_y))

    # 목표 산타 찾기
    # r 좌표 큰 > c 좌표 큰 산타 찾기
    min_dist_santa = sorted(min_dist_santa, key=lambda x: (x[0], -x[2], -x[3]))
    target_santa = min_dist_santa[0]

    # 목표 산타와 8방향 중 가장 가까원지는 방향으로 한 칸 돌진
    min_dist = int(1e9)
    min_dir = 0
    target_num, target_x, target_y = target_santa[1], target_santa[2], target_santa[3]
    for d in range(8):
        next_x, next_y = rudolf.x + dx_rudolf[d], rudolf.y + dy_rudolf[d]
        if next_x < 1 or next_x > n or next_y < 1 or next_y > n:
            continue
        dist = (target_x - next_x) ** 2 + (target_y - next_y) ** 2
        if min_dist > dist:
            min_dist = dist
            min_dir = d

    # 목표 산타와 가장 가까워지는 방향으로 이동
    rudolf.move(min_dir)

    # 이동을 했는데, 산타와 충돌한 경우
    if graph[rudolf.x][rudolf.y] != 0:
        santa_num = graph[rudolf.x][rudolf.y]

        # 산타 기절
        santas[santa_num].shock_turn = turn

        santas[santa_num].score += c

        conflict(0, c, santa_num, santas[santa_num].x, santas[santa_num].y, min_dir)


def move_santa(turn, idx):

    ####### KEY POINT) min_dist 를 int(1e9) 로 설정하니까, 원래 위치에서 어느 위치로 가든 더 가까워질 수밖에 없음!!!!!!!!!!!!!!
    ####### -> 움직이기 전의 위치에서 산타와의 거리를 min_dist 값으로 초기 설정해야 함!!!!!!!
    ####### -> ~에게 거리가 가장 가까워지는 방향으로 이동할 때 체크할 점!!!!!
    # min_dist = int(1e9)
    init_dist = (santas[idx].x - rudolf.x) ** 2 + (santas[idx].y - rudolf.y) ** 2
    min_dist = init_dist

    # # 가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위에 맞춰 움직임
    min_dir_list = []
    for i in range(4):
        santa_next_x = santas[idx].x + dx_santa[i]
        santa_next_y = santas[idx].y + dy_santa[i]

        # 범위 벗어나면 X
        if santa_next_x < 1 or santa_next_x > n or santa_next_y < 1 or santa_next_y > n:
            continue

        #### 산타는 루돌프 or 다른 산타가 있는 경우 이동 불가!!
        # 루돌프가 있다면 X

        # 다른 산타가 있으면 X
        if graph[santa_next_x][santa_next_y] != 0:
            continue

        dist = (santa_next_x - rudolf.x) ** 2 + (santa_next_y - rudolf.y) ** 2
        min_dir_list.append((dist, i))
        if min_dist > dist:
            min_dist = dist

    # 움직일 수 있는 칸이 있더라도, 루돌프로부터 가까워질 수 있는 방법 X -> 산타 움직이지 X

    if min_dist == init_dist:
        return

    min_dir_list = sorted(min_dir_list, key=lambda x: (x[0], x[1]))
    target_min_dir = min_dir_list[0]
    next_dir = target_min_dir[1]
    next_x, next_y = (
        santas[idx].x + dx_santa[next_dir],
        santas[idx].y + dy_santa[next_dir],
    )
    santas[idx].move(next_x, next_y, next_dir)

    # 이동을 했는데, 루돌프와 충돌한 경우
    if (rudolf.x, rudolf.y) == (santas[idx].x, santas[idx].y):
        santas[idx].shock_turn = turn

        ### 위에서 방향 d 의 값이 들어가게 됨!!!!!

        santas[idx].score += d
        conflict(1, d, idx, santas[idx].x, santas[idx].y, next_dir ^ 2)


for turn in range(1, m + 1):

    # 1. 루돌프 움직임
    move_rudolf(turn)

    # 2. 산타 움직임
    for idx in range(1, p + 1):

        # 기절한 턴의 다음 턴이거나, 탈락한 경우 X
        santa = santas[idx]

        if turn == santa.shock_turn or turn == santa.shock_turn + 1 or santa.die:
            continue

        move_santa(turn, idx)

    # 4. 살아남은 산타의 점수 증가
    alive_cnt = 0
    for i in range(1, p + 1):
        if not santas[i].die:
            santas[i].score += 1
            alive_cnt += 1

    # 5. 모든 산타가 탈락했다면, 즉시 게임 종료
    if alive_cnt == 0:
        break

total_score = 0
for i in range(1, p + 1):
    print(santas[i].score, end=" ")