#include <iostream>
#include <queue>
using namespace std;
int N, M, Q;  // 지도의 크기, 기사의 수, 명령의 수
int original_map[55][55];  // 벽, 함정 등을 표현하는 지도
int dirs[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
struct Knight {
    int idx;            // 이 기사의 번호
    int r, c, h, w, k;  // 위치, 크기, 체력
    int damage;         // 받은 총 데미지
    void fill(int map[][55]) {
        if (k <= 0)
            return;
        // 기사가 차지하는 공간에 기사의 번호 채우기
        for (int i = r; i < r + h; i++) {
            for (int j = c; j < c + w; j++) {
                map[i][j] = idx;
            }
        }
    }
    void move(int d) {
        // 기사를 d번 방향으로 한 칸 이동시키기
        r += dirs[d][0];
        c += dirs[d][1];
    }
    void hurt() {
        for (int i = r; i < r + h; i++) {
            for (int j = c; j < c + w; j++) {
                if (original_map[i][j] == 1) {
                    k --;
                    damage ++;
                }
            }
        }
    }
}knights[40];
void input() {
    cin >> N >> M >> Q;
    for (int i=1;i<=N;i++) {
        for (int j=1;j<=N;j++){
            cin >> original_map[i][j];
        }
    }
    for (int i=1;i<=M;i++){
        int r, c, h, w, k;
        cin >> r >> c >> h >> w >> k;
        knights[i] = {i, r, c, h, w, k, 0};
    }
}
void move(int k, int d) {  // k번 기사를 d번 방향으로 이동시켜주는 함수. 벽을 만나는 이동이라면 무효 처리
    int knights_map[55][55] = {0, };
    // 각 기사가 차지하는 공간을 새로이 그려냄
    for (int i = 1; i <= M; i++) {
        knights[i].fill(knights_map);
    }
    // 이동할 친구들을 찾자
    bool moving[55] = {0, };  // moving[i] := i번 기사가 이동 여부
    queue<int> Q;  // 이동하는 친구들을 담는 큐
    Q.push(k);
    moving[k] = true;
    while (!Q.empty()) {
        int k = Q.front(); Q.pop();
        
        for (int i = knights[k].r; i < knights[k].r + knights[k].h; i++) {
            for (int j = knights[k].c; j < knights[k].c + knights[k].w; j++) {
                // (r, c)는 기사에 포함된 격자 중 하나
                int r = i, c = j;
                for (;;) {
                    r += dirs[d][0];
                    c += dirs[d][1];
                    if (r < 1 || c < 1 || r > N || c > N)  // 격자를 벗어나도 벽임
                        return;
                    if (knights_map[r][c] == 0){  // d 번 방향으로 이동했더니, 기사가 존재하지 않음
                        if (original_map[r][c] == 2) {  // 근데 벽이 존재한다.
                            return;
                        }
                        break;
                    }
                    // 기사가 존재하는 칸을 의미하므로, 이동 여부 갱신
                    if (!moving[knights_map[r][c]]) {  // 새롭게 이동하는 친구를 찾음!
                        moving[knights_map[r][c]] = true;
                        Q.push(knights_map[r][c]);
                    }
                }
            }
        }
    }
    // 이동해야 하는 친구들 이동 시키고, 체력 감소
    for (int i = 1;i <= M; i++){
        if (!moving[i]) continue;  // 이동하지 않는 친구는 무시하기
        knights[i].move(d);
        if (i != k) {  // 명령을 받지 않은 기사가 이동
            knights[i].hurt();
        }
    }
}
void pro() {
    while (Q--){
        // 1. 입력 받기 (기사 k 가 d 번 방향으로 이동한다.)
        int k, d;
        cin >> k >> d;
        // 2. 기사의 생존 여부 확인
        if (knights[k].k <= 0){
            continue;
        }
        // 3. 기사를 이동시키는 명령 수행
        move(k, d);
    }
    int ans = 0;
    for (int i=1;i<=M;i++){
        if (knights[i].k >= 1){
            ans += knights[i].damage;
        }
    }
    cout << ans;
}
int main() {
    input();
    pro();
    return 0;
}