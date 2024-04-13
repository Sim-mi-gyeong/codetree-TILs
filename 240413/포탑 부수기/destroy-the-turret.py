from collections import deque


class Tower:
    def __init__(self, num, x, y, power, last_attack):
        self.num = num
        self.x = x
        self.y = y
        self.power = power
        self.last_attack = last_attack
        # self.effect_attack = effect_attack

    def minus_power(self, minus):
        self.power -= minus


# 최초에 부서지지 않은 포탑은 최소 2개 이상 존재
n, m, k = map(int, input().split())
graph = [[0] * (m + 1) for _ in range(n + 1)]
towers = [0]
for i in range(1, n + 1):
    lst = list(map(int, input().split()))
    for j in range(1, m + 1):
        tower = Tower(4 * (i - 1) + j, i, j, lst[j - 1], 0)
        # graph[i][j] = lst[j - 1]
        graph[i][j] = tower


def find_fighter():
    # 매번 n * m 크기의 격자를 돌면서 체크 가능?! (10 * 10 * 1000)
    min_power_list = []
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            tower = graph[i][j]
            if tower.power > 0:
                min_power_list.append(
                    (tower.x, tower.y, tower.power, tower.last_attack)
                )

    min_power_list = sorted(
        min_power_list, key=lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[2])
    )

    return graph[min_power_list[0][0]][min_power_list[0][1]]


def find_target(fighter):
    max_power_list = []
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            tower = graph[i][j]
            #### 공격자 본인 제외!!!!!!!!!!!
            if tower.power > 0 and (i, j) != (fighter.x, fighter.y):
                max_power_list.append(
                    (tower.x, tower.y, tower.power, tower.last_attack)
                )

    max_power_list = sorted(
        max_power_list, key=lambda x: (-x[2], x[3], (x[0] + x[1]), x[2])
    )

    return graph[max_power_list[0][0]][max_power_list[0][1]]


# fighter 부터 target 까지 최단 경로 먼저 찾기
def raser(fighter, target):

    visited = [[0] * (m + 1) for _ in range(n + 1)]
    q = deque()

    # 경로 추적을 위한 역추적 배열!!!
    come = [[None] * (m + 1) for _ in range(n + 1)]

    visited[fighter.x][fighter.y] = 1
    q.append((fighter.x, fighter.y, 0))

    while q:
        x, y, dist = q.popleft()
        # 공격 대상까지 가는 이동 경로는 저장해야 하나?!?!?!?!
        if (x, y) == (
            target.x,
            target.y,
        ):

            break

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if nx < 1:
                nx = n
            elif nx > n:
                nx = 1

            elif ny < 1:
                ny = m
            elif ny > m:
                ny = 1

            # 무너진 포탑은 이동 불가
            if graph[nx][ny].power <= 0:
                continue
            if visited[nx][ny]:
                continue

            visited[nx][ny] = 1
            q.append((nx, ny, dist + 1))
            come[nx][ny] = (x, y)

    # 레이저 공격이 불가능한 경우(공격 대상까지 도달 불가) -> BFS 과정에서 공격 대상까지 방문했는지!
    if visited[target.x][target.y] != 1:
        return False

    # 공격 대상 위치부터 ~> 공격자 역추적 배열 통해서 이동
    x, y = target.x, target.y
    while x != fighter.x or y != fighter.y:
        minus_power = fighter.power // 2

        if (x, y) == (target.x, target.y):
            minus_power = fighter.power

        # 공격처리
        tar = graph[x][y]
        tar.power -= minus_power
        isEffect[x][y] = True

        # come[target.x][target.y] 칸에는, 해당 칸에 오기 전 어떤 위치에서 왔는지가 기록 되어 있음!
        x, y = come[x][y]

    # 레이저 공격이 가능한 경우, 레이저 공격을 하고 True 리턴
    return True


### 포탄 공격
# - 공격 대상에 포탄 던지기
# - 공격 대상-> - 공격자 공격력
# - 주위 8방향에 피해 -> - 공격자 공격력 // 2 (격자가 이어진 상태!!)
def bomb(fighter, target):
    target.power -= fighter.power

    minus_power = fighter.power // 2

    for d in range(8):
        nx = target.x + dir_x[d]
        ny = target.y + dir_y[d]

        if nx < 1:
            nx = n
        elif nx > n:
            nx = 1

        elif ny < 1:
            ny = m
        elif ny > m:
            ny = 1

        if graph[nx][ny].power > 0:
            graph[nx][ny].power -= minus_power
            isEffect[nx][ny] = True


# 최단 경로 찾는 방향 순서
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

# 8방향(위 / 오른쪽 위 / 오른쪽 / 오른쪽 아래 / 아래 / 왼쪽 아래 / 왼쪽 / 왼쪽 위)
dir_x = [-1, -1, 0, 1, 1, 1, 0, -1]
dir_y = [0, 1, 1, 1, 0, -1, -1, -1]


def choose_best():
    max_power = graph[1][1].power
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if max_power < graph[i][j].power:
                max_power = graph[i][j].power
    return max_power


# 부서지지 않은 포탑이 1개가 되는 경우 즉시 종료 -> 0개가 되어도?
def is_finish():
    alive_cnt = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if graph[i][j].power > 0:
                alive_cnt += 1

    # if alive_cnt == 1:
    if alive_cnt <= 1:
        return True
    return False


for turn in range(1, k + 1):
    isEffect = [[False] * (m + 1) for _ in range(n + 1)]

    # 1. 공격자 찾기
    fighter = find_fighter()
    # 공격자 핸디캡
    fighter.power += n + m

    # 공격자 마지막 공격 턴 최신화
    fighter.last_attack = turn

    # 공격자 공격 관여 check
    isEffect[fighter.x][fighter.y] = True

    # 2. 공격 대상 찾기
    target = find_target(fighter)
    # isEffect[target.x][target.y] = True

    # 3. 공격 - 레이저 공격이 가능한 경우 레이저 공격, 그게 아니면 포탄 공격
    if not raser(fighter, target):
        bomb(fighter, target)

    # 4. 포탑 부서짐

    # 5. 포탑 정비

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if not isEffect[i][j] and graph[i][j].power > 0:
                graph[i][j].power += 1

    # 6. 종료 체크 -  시작과 동시에? -> 처음에는 부서지지 않은 포탑은 최소 2개 이상 존재
    if is_finish():
        break

# 종료한 경우 가장 공격력 큰 포탑 공격력 출력
print(choose_best())